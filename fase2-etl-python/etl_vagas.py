"""
FASE 2 — ETL simples para inserir vagas novas no banco de dados.

EXTRACT : lê um arquivo de texto estruturado dentro de vagas_brutas/
TRANSFORM: identifica empresa, título, localização, modalidade e
           varre a descrição procurando quais competências do
           catálogo (tabela `competencias`) aparecem no texto,
           classificando cada uma como Obrigatório ou Desejável.
LOAD     : insere empresa (se for nova), a vaga e as competências
           encontradas no banco vagas.db — sem duplicar nada.

Como usar:
    python3 etl_vagas.py vagas_brutas/exemplo_vaga.txt
"""

import sqlite3
import sys
import re
import unicodedata
from datetime import date

DB_FILE = "vagas.db"


# ------------------------------------------------------------------
# EXTRACT
# ------------------------------------------------------------------
def extract(filepath: str) -> str:
    """Lê o arquivo bruto da vaga e devolve o texto completo."""
    with open(filepath, encoding="utf-8") as f:
        return f.read()


# ------------------------------------------------------------------
# TRANSFORM
# ------------------------------------------------------------------
def _normalizar(texto: str) -> str:
    """Remove acentos e deixa em minúsculo, pra comparar texto sem
    se importar com 'É' vs 'e', 'ç' vs 'c', etc."""
    nfkd = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in nfkd if not unicodedata.combining(c))
    return sem_acento.lower()


_SEPARADOR = re.compile(r"^\s*-{3,}\s*$", flags=re.MULTILINE)


def _dividir_cabecalho_corpo(texto: str) -> tuple[str, str]:
    """Divide o texto em (cabeçalho, corpo) usando como separador uma
    LINHA que contém só hífens (---). Isso evita confundir com um
    '---' que apareça solto dentro de um comentário ou da descrição."""
    m = _SEPARADOR.search(texto)
    if not m:
        return texto, ""
    return texto[: m.start()], texto[m.end():]


def _parse_cabecalho(texto: str) -> dict:
    """Extrai EMPRESA, TITULO, LOCALIZACAO, MODALIDADE das linhas
    'CAMPO: valor' que vêm antes do separador '---'."""
    cabecalho_bruto, _ = _dividir_cabecalho_corpo(texto)

    campos = {"empresa": None, "titulo": None, "localizacao": None, "modalidade": "Não informado"}
    padrao = {
        "empresa": r"^EMPRESA:\s*(.+)$",
        "titulo": r"^TITULO:\s*(.+)$",
        "localizacao": r"^LOCALIZACAO:\s*(.+)$",
        "modalidade": r"^MODALIDADE:\s*(.+)$",
    }

    for linha in cabecalho_bruto.splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        for campo, regex in padrao.items():
            m = re.match(regex, linha, flags=re.IGNORECASE)
            if m:
                campos[campo] = m.group(1).strip()

    return campos


def _extrair_corpo(texto: str) -> str:
    """Tudo que vem depois da linha separadora '---' é a descrição
    livre da vaga, onde vamos procurar as competências."""
    _, corpo = _dividir_cabecalho_corpo(texto)
    return corpo


def _identificar_competencias(corpo: str, competencias_catalogo: list[tuple[int, str]]) -> list[tuple[int, str, str]]:
    """
    Para cada competência já cadastrada no banco, verifica se ela
    aparece no texto da vaga. Se aparecer, olha SÓ A LINHA onde essa
    menção está pra decidir se é Obrigatório ou Desejável.

    Importante: usar a linha inteira (não uma janela de caracteres)
    evita que a marcação "(obrigatório)" de um item vizinho vaze pra
    outro item na linha de baixo/cima — bug real que apareceu no
    primeiro teste deste script, com listas de bullets muito juntas.

    Quando a vaga não tem a marcação explícita na mesma linha (comum
    em descrições corridas, sem bullets), o padrão é 'Desejável' —
    é uma limitação honesta desse ETL simples; classificar aderência
    a partir de texto corrido de verdade é tarefa pra Fase 4 (ML).

    Retorna lista de tuplas: (id_competencia, nome, exigencia)
    """
    linhas = corpo.split("\n")
    linhas_normalizadas = [_normalizar(l) for l in linhas]
    encontradas = []

    for id_competencia, nome in competencias_catalogo:
        nome_normalizado = _normalizar(nome)

        linha_encontrada = None
        for linha_norm in linhas_normalizadas:
            if nome_normalizado in linha_norm:
                linha_encontrada = linha_norm
                break

        if linha_encontrada is None:
            continue  # essa competência não aparece em nenhuma linha

        if "obrigator" in linha_encontrada:
            exigencia = "Obrigatório"
        elif "desej" in linha_encontrada:
            exigencia = "Desejável"
        else:
            exigencia = "Desejável"  # padrão conservador quando a linha não diz

        encontradas.append((id_competencia, nome, exigencia))

    return encontradas


def transform(texto: str, competencias_catalogo: list[tuple[int, str]]) -> dict:
    cabecalho = _parse_cabecalho(texto)
    corpo = _extrair_corpo(texto)
    competencias_encontradas = _identificar_competencias(corpo, competencias_catalogo)

    return {
        "empresa": cabecalho["empresa"],
        "titulo": cabecalho["titulo"],
        "localizacao": cabecalho["localizacao"],
        "modalidade": cabecalho["modalidade"],
        "competencias": competencias_encontradas,
    }


# ------------------------------------------------------------------
# LOAD
# ------------------------------------------------------------------
def _obter_ou_criar_empresa(conn: sqlite3.Connection, nome_empresa: str) -> int:
    cur = conn.cursor()
    cur.execute("SELECT id_empresa FROM empresas WHERE nome = ?", (nome_empresa,))
    linha = cur.fetchone()
    if linha:
        return linha[0]

    cur.execute(
        "INSERT INTO empresas (nome, setor) VALUES (?, ?)",
        (nome_empresa, "Não informado"),
    )
    conn.commit()
    print(f"  + Nova empresa cadastrada: {nome_empresa}")
    return cur.lastrowid


def load(dados: dict, conn: sqlite3.Connection) -> None:
    if not dados["empresa"] or not dados["titulo"]:
        raise ValueError(
            "O arquivo precisa ter as linhas 'EMPRESA:' e 'TITULO:' preenchidas."
        )

    cur = conn.cursor()

    id_empresa = _obter_ou_criar_empresa(conn, dados["empresa"])

    # evita duplicar a mesma vaga se o script rodar de novo
    cur.execute(
        "SELECT id_vaga FROM vagas WHERE titulo = ? AND id_empresa = ?",
        (dados["titulo"], id_empresa),
    )
    if cur.fetchone():
        print(f"  ! Vaga '{dados['titulo']}' já existe no banco — nada foi inserido.")
        return

    cur.execute(
        """INSERT INTO vagas (id_empresa, titulo, localizacao, modalidade, tipo_vaga, data_analise)
           VALUES (?, ?, ?, ?, 'Estágio', ?)""",
        (id_empresa, dados["titulo"], dados["localizacao"], dados["modalidade"], date.today().isoformat()),
    )
    id_vaga = cur.lastrowid
    print(f"  + Vaga inserida: {dados['titulo']} (id {id_vaga})")

    for id_competencia, nome, exigencia in dados["competencias"]:
        cur.execute(
            """INSERT OR IGNORE INTO vaga_competencias (id_vaga, id_competencia, exigencia)
               VALUES (?, ?, ?)""",
            (id_vaga, id_competencia, exigencia),
        )
        print(f"    - {nome}: {exigencia}")

    conn.commit()
    print(f"  ✔ {len(dados['competencias'])} competência(s) associada(s) à vaga.")


# ------------------------------------------------------------------
# ORQUESTRAÇÃO (junta Extract + Transform + Load)
# ------------------------------------------------------------------
def main():
    if len(sys.argv) != 2:
        print("Uso: python3 etl_vagas.py caminho/para/arquivo_da_vaga.txt")
        sys.exit(1)

    caminho_arquivo = sys.argv[1]

    print(f"[EXTRACT] Lendo {caminho_arquivo} ...")
    texto_bruto = extract(caminho_arquivo)

    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")

    cur = conn.cursor()
    cur.execute("SELECT id_competencia, nome FROM competencias")
    catalogo = cur.fetchall()

    print("[TRANSFORM] Identificando empresa, vaga e competências ...")
    dados = transform(texto_bruto, catalogo)

    print("[LOAD] Inserindo no banco de dados ...")
    load(dados, conn)

    conn.close()
    print("\nPronto! Rode 'python3 run_queries.py' pra ver essa vaga nova nas consultas.")


if __name__ == "__main__":
    main()
