"""
Roda as 10 queries de 03_queries.sql contra o banco vagas.db
e mostra os resultados formatados direto no terminal.

Como usar:
    python3 run_queries.py

Pré-requisito: já ter rodado o comando que cria o vagas.db
(passo 5 do tutorial) nesta mesma pasta.
"""

import sqlite3
import os

DB_FILE = "vagas.db"
QUERIES_FILE = "03_queries.sql"

if not os.path.exists(DB_FILE):
    print(f"❌ Não encontrei '{DB_FILE}' nesta pasta.")
    print("   Rode primeiro o comando do Passo 5 do tutorial para criar o banco.")
    raise SystemExit(1)

if not os.path.exists(QUERIES_FILE):
    print(f"❌ Não encontrei '{QUERIES_FILE}' nesta pasta.")
    print("   Confirme que o terminal está dentro da pasta fase1-banco-vagas.")
    raise SystemExit(1)

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

sql_text = open(QUERIES_FILE, encoding="utf-8").read()

# Separa o arquivo em blocos numerados (-- 1) ..., -- 2) ..., etc.)
import re
partes = re.split(r"-- (\d+)\)\s*", sql_text)
# partes[0] é o cabeçalho do arquivo (ignorar); depois vem: numero, texto, numero, texto...

for i in range(1, len(partes), 2):
    numero = partes[i]
    bloco = partes[i + 1]

    # primeira linha do bloco é o título da pergunta
    linhas = bloco.strip().split("\n")
    titulo = linhas[0].strip()

    # remove a linha de título e as linhas de comentário (--),
    # para sobrar só o SQL de verdade
    sql_puro = "\n".join(l for l in linhas[1:] if not l.strip().startswith("--")).strip()
    sql_puro = sql_puro.rstrip(";")

    print("=" * 70)
    print(f"QUERY {numero}: {titulo}")
    print("=" * 70)

    try:
        cur.execute(sql_puro)
        colunas = [d[0] for d in cur.description]
        linhas_resultado = cur.fetchall()

        # imprime cabeçalho
        print(" | ".join(colunas))
        print("-" * 70)
        for linha in linhas_resultado:
            print(" | ".join(str(v) for v in linha))

        print(f"\n({len(linhas_resultado)} linha(s) retornada(s))\n")
    except Exception as e:
        print(f"⚠️  Erro ao rodar esta query: {e}\n")

conn.close()
print("Pronto! Todas as queries foram executadas.")
