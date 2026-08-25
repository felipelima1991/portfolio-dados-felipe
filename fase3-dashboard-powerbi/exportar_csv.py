"""
FASE 3 — Exporta as tabelas do vagas.db para arquivos CSV, prontos
para importar no Power BI (ou Looker Studio, Excel, etc.)

Por que CSV em vez de conectar direto no .db?
Power BI não tem um conector nativo para SQLite — exigiria instalar
um driver ODBC extra. Exportar para CSV é mais simples pra um
primeiro contato, e é também como muitos pipelines de dados reais
funcionam: um sistema gera CSV, o BI consome CSV.

Como usar:
    python3 exportar_csv.py
"""

import sqlite3
import csv
import os

DB_FILE = "vagas.db"
PASTA_SAIDA = "csv_export"

TABELAS = [
    "empresas",
    "vagas",
    "competencias",
    "vaga_competencias",
    "minhas_competencias",
    "candidaturas",
]


def exportar_tabela(cur: sqlite3.Cursor, nome_tabela: str) -> int:
    cur.execute(f"SELECT * FROM {nome_tabela}")
    colunas = [d[0] for d in cur.description]
    linhas = cur.fetchall()

    caminho_csv = os.path.join(PASTA_SAIDA, f"{nome_tabela}.csv")
    with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as f:
        # utf-8-sig inclui um BOM no início do arquivo — sem isso,
        # o Excel e o Power BI às vezes mostram acentos quebrados
        # (ex: "Aderência" virando "AderÃªncia").
        writer = csv.writer(f)
        writer.writerow(colunas)
        writer.writerows(linhas)

    return len(linhas)


def main():
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    print(f"Exportando tabelas de '{DB_FILE}' para a pasta '{PASTA_SAIDA}/':\n")
    for tabela in TABELAS:
        qtd = exportar_tabela(cur, tabela)
        print(f"  ✔ {tabela}.csv  ({qtd} linha(s))")

    conn.close()
    print(f"\nPronto! {len(TABELAS)} arquivos CSV criados em '{PASTA_SAIDA}/'.")
    print("Agora é só importar cada um deles no Power BI.")


if __name__ == "__main__":
    main()
