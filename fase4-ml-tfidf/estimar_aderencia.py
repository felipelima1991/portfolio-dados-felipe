"""
FASE 4 — Estimando aderência com TF-IDF + similaridade de cosseno.

Por que não um classificador supervisionado "de verdade"?
Eu tenho 6 vagas no banco. Treinar um modelo supervisionado (que aprende
um padrão geral a partir de exemplos rotulados) com 6 linhas não geraria
nada confiável — é dado de menos pra "aprender" qualquer coisa que
generalize. Em vez disso, uso uma técnica de similaridade de texto, que é
válida mesmo com poucos documentos: comparo o texto do MEU PERFIL com o
texto de CADA VAGA e meço o quão parecidos eles são.

Como funciona, em 3 passos:
1. Transformo "meu perfil" (minhas competências) e cada "vaga" (as
   competências que ela exige) em um texto.
2. Uso TF-IDF pra transformar esses textos em vetores numéricos — cada
   palavra vira um número que reflete sua importância no documento.
3. Meço a similaridade de cosseno entre o vetor do meu perfil e o vetor
   de cada vaga: quanto mais próximo de 1, mais parecido.

Vantagem sobre a Fase 2: como o TF-IDF trabalha com o texto completo da
vaga (não só o catálogo fixo de 20 competências), ele pode captar
sinal mesmo quando a vaga usa um sinônimo que a Fase 2 não reconheceria.

Como usar:
    python3 estimar_aderencia.py                      # avalia as 6 vagas do banco
    python3 estimar_aderencia.py caminho/vaga_nova.txt # avalia uma vaga nova
"""

import sqlite3
import sys
import re
import unicodedata

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DB_FILE = "vagas.db"

# pesos: quanto mais avançado eu sou / quanto mais obrigatória a vaga
# exige, mais vezes a palavra se repete no "documento" — repetição é o
# jeito mais simples de dar mais peso a um termo no TF-IDF.
PESO_MEU_NIVEL = {
    "Avançado": 3,
    "Intermediário": 2,
    "Em desenvolvimento": 1,
    "Básico": 1,
}
PESO_EXIGENCIA = {
    "Obrigatório": 3,
    "Desejável": 1,
}


def _normalizar(texto: str) -> str:
    nfkd = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in nfkd if not unicodedata.combining(c))
    return sem_acento.lower()


def montar_documento_meu_perfil(conn: sqlite3.Connection) -> str:
    """Junta as competências que eu já tenho num texto só, repetindo
    cada uma de acordo com o meu nível de domínio."""
    cur = conn.cursor()
    cur.execute(
        """SELECT c.nome, mc.nivel
           FROM minhas_competencias mc
           JOIN competencias c ON c.id_competencia = mc.id_competencia"""
    )
    palavras = []
    for nome, nivel in cur.fetchall():
        peso = PESO_MEU_NIVEL.get(nivel, 1)
        palavras.extend([nome] * peso)
    return " ".join(palavras)


def montar_documentos_vagas(conn: sqlite3.Connection) -> list[tuple[int, str, str]]:
    """Pra cada vaga do banco, junta as competências exigidas num texto,
    repetindo mais as obrigatórias. Retorna (id_vaga, titulo, documento)."""
    cur = conn.cursor()
    cur.execute("SELECT id_vaga, titulo FROM vagas")
    vagas = cur.fetchall()

    documentos = []
    for id_vaga, titulo in vagas:
        cur.execute(
            """SELECT c.nome, vc.exigencia
               FROM vaga_competencias vc
               JOIN competencias c ON c.id_competencia = vc.id_competencia
               WHERE vc.id_vaga = ?""",
            (id_vaga,),
        )
        palavras = []
        for nome, exigencia in cur.fetchall():
            peso = PESO_EXIGENCIA.get(exigencia, 1)
            palavras.extend([nome] * peso)
        documentos.append((id_vaga, titulo, " ".join(palavras)))

    return documentos


def calcular_similaridades(perfil_doc: str, vagas_docs: list[tuple[int, str, str]]) -> list[tuple[str, float]]:
    """Treina o TF-IDF em cima de (perfil + todas as vagas) e calcula a
    similaridade de cosseno entre o perfil e cada vaga."""
    corpus = [perfil_doc] + [doc for _, _, doc in vagas_docs]

    vectorizer = TfidfVectorizer()
    matriz_tfidf = vectorizer.fit_transform(corpus)

    vetor_perfil = matriz_tfidf[0:1]
    vetores_vagas = matriz_tfidf[1:]

    similaridades = cosine_similarity(vetor_perfil, vetores_vagas)[0]

    resultados = [
        (vagas_docs[i][1], float(similaridades[i]))
        for i in range(len(vagas_docs))
    ]
    return sorted(resultados, key=lambda x: x[1], reverse=True)


def extrair_texto_vaga_nova(caminho_arquivo: str) -> str:
    """Reaproveita a mesma lógica de separador '---' da Fase 2 pra pegar
    só o corpo da descrição de um arquivo de vaga nova."""
    texto = open(caminho_arquivo, encoding="utf-8").read()
    separador = re.compile(r"^\s*-{3,}\s*$", flags=re.MULTILINE)
    m = separador.search(texto)
    return texto[m.end():] if m else texto


def avaliar_vaga_nova(caminho_arquivo: str, conn: sqlite3.Connection) -> None:
    perfil_doc = montar_documento_meu_perfil(conn)
    vagas_docs = montar_documentos_vagas(conn)

    corpo_novo = extrair_texto_vaga_nova(caminho_arquivo)

    corpus = [perfil_doc] + [doc for _, _, doc in vagas_docs] + [corpo_novo]
    vectorizer = TfidfVectorizer()
    matriz = vectorizer.fit_transform(corpus)

    vetor_perfil = matriz[0:1]
    vetor_novo = matriz[-1:]

    similaridade = cosine_similarity(vetor_perfil, vetor_novo)[0][0]

    print(f"\nVaga nova: {caminho_arquivo}")
    print(f"Similaridade estimada com meu perfil: {similaridade:.1%}")
    print(
        "\n(Essa é uma estimativa por similaridade de texto, não uma"
        " probabilidade — sirva como um sinal a mais, não como palavra final.)"
    )


def main():
    conn = sqlite3.connect(DB_FILE)

    if len(sys.argv) == 2:
        avaliar_vaga_nova(sys.argv[1], conn)
        conn.close()
        return

    perfil_doc = montar_documento_meu_perfil(conn)
    vagas_docs = montar_documentos_vagas(conn)
    resultados = calcular_similaridades(perfil_doc, vagas_docs)

    print("Aderência estimada por TF-IDF + similaridade de cosseno:\n")
    print(f"{'Vaga':<45} {'Similaridade':>12}")
    print("-" * 58)
    for titulo, score in resultados:
        print(f"{titulo:<45} {score:>11.1%}")

    conn.close()


if __name__ == "__main__":
    main()
