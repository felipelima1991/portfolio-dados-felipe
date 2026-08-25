# Portfólio de Dados — Felipe Oliveira de Lima

Estudante de Ciência de Dados (UNIVESP), em transição de carreira de
Qualidade e Segurança dos Alimentos para Dados e BI.

📍 São Paulo, SP · [linkedin.com/in/felipelima1991](https://linkedin.com/in/felipelima1991)

## A ideia por trás desse repositório

Enquanto eu analisava vagas de estágio em Dados e ajustava meu currículo
pra cada uma, percebi que estava acumulando um problema de dados de
verdade: várias vagas, cada uma com requisitos diferentes, e nenhuma forma
estruturada de comparar meu perfil com o que cada uma pedia.

Em vez de resolver isso numa planilha, decidi transformar o próprio
problema em um projeto de portfólio — construindo, fase a fase, o
pipeline completo que uma pessoa de dados usaria: banco de dados → ETL →
dashboard → (em breve) machine learning.

## Arquitetura do projeto

```mermaid
flowchart LR
    A["Texto bruto da vaga (.txt)"] -->|ETL Python| B[("vagas.db — SQLite")]
    B -->|10 queries SQL| C["Análise de aderência"]
    B -->|exportar_csv.py| D["Arquivos CSV"]
    D -->|Power BI| E["Dashboard interativo"]
```

## As fases

| Fase | O que é | Principais skills |
|---|---|---|
| [1 — Banco de Dados](./fase1-banco-vagas/README.md) | Modelagem relacional das vagas analisadas, com 10 queries SQL | SQL (`JOIN`, `GROUP BY`, `HAVING`), modelagem de dados |
| [2 — ETL em Python](./fase2-etl-python/README.md) | Script que automatiza a inserção de vagas novas no banco | Python, `sqlite3`, Extract/Transform/Load |
| [3 — Dashboard em Power BI](./fase3-dashboard-powerbi/README.md) | Painel interativo replicando a análise de aderência via DAX | Power Query, relacionamentos, DAX, visualização de dados |

Cada pasta tem seu próprio README explicando o problema, as decisões que
tomei e — sempre que apareceu — o bug real que encontrei e como corrigi.
Prefiro documentar os erros do processo a esconder que eles aconteceram.

## Um insight que saiu do projeto

A mesma pergunta — "em qual vaga meu perfil já é mais forte?" — foi
respondida de duas formas independentes (SQL na Fase 1, DAX na Fase 3) e
bateu exatamente:

| Vaga | % Aderência |
|---|---:|
| Estágio em Data & Analytics (Sistemas) | 66,7% |
| Estágio em Analytics | 60,0% |
| Estágio em TI – Foco em Dados | 57,1% |
| Programa de Estágio (2º sem. 2026) | 50,0% |
| Estágio - Tecnologia, Dados & BI | 44,4% |
| Estagiário de Ciência de Dados | 20,0% |

## Próximos passos

- **Fase 4** — um modelo simples de Machine Learning que estima a
  aderência de uma vaga nova automaticamente a partir do texto.
- **Fase 5** — subir o banco de dados pra nuvem (AWS).

## Stack

`Python` · `SQL (SQLite)` · `Power BI` · `Git/GitHub`
