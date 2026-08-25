# Fase 3 — Dashboard em Power BI

**Parte de:** [Trilha de Projetos Práticos — Ciência de Dados](../Trilha_Projetos_Ciencia_Dados_Felipe.md)
**Depende de:** [Fase 1](../fase1-banco-vagas/README.md) e [Fase 2](../fase2-etl-python/README.md)
**Autor:** Felipe Oliveira de Lima

## Problema

Até aqui, pra saber "em qual vaga meu perfil é mais forte", eu precisava
rodar uma query SQL manualmente. Isso funciona, mas não é visual, não
atualiza sozinho quando entra vaga nova, e não é o formato que a maioria
das empresas usa no dia a dia pra acompanhar indicadores.

## O que eu fiz

Exportei as 6 tabelas do banco (`vagas.db`) para CSV com um script Python
(`exportar_csv.py`) e montei um dashboard no Power BI Desktop em cima
desses arquivos — recriando visualmente a mesma análise de aderência que
já fazíamos por SQL, além de outros indicadores.

## Por que CSV em vez de conectar direto no banco

Power BI não tem conector nativo pra SQLite (exigiria instalar um driver
ODBC extra, complicado pra um primeiro contato com a ferramenta).
Exportar pra CSV é mais simples e, na prática, é assim que muitos
pipelines reais funcionam mesmo: um sistema gera CSV, o time de BI
consome CSV.

## Passo 1 — Exportar os dados

```bash
python3 exportar_csv.py
```

Isso cria a pasta `csv_export/` com 6 arquivos: `empresas.csv`,
`vagas.csv`, `competencias.csv`, `vaga_competencias.csv`,
`minhas_competencias.csv`, `candidaturas.csv`.

## Passo 2 — Importar no Power BI Desktop

Baixe o Power BI Desktop (gratuito) em
`powerbi.microsoft.com/desktop`. Depois de instalar:

1. Abra o Power BI Desktop.
2. Clique em **Obter dados** > **Texto/CSV**.
3. Selecione `empresas.csv` e clique em **Carregar**.
4. Repita para os outros 5 arquivos (`vagas.csv`, `competencias.csv`,
   `vaga_competencias.csv`, `minhas_competencias.csv`,
   `candidaturas.csv`).

Ao final, você deve ter 6 tabelas carregadas — confira no painel **Dados**
à direita.

## Passo 3 — Criar os relacionamentos

Clique no ícone de **Modelo** (barra lateral esquerda, parece um
diagrama). Arraste uma linha conectando os seguintes pares de campos
(mesma lógica do diagrama ER da Fase 1):

| De (tabela.campo) | Para (tabela.campo) |
|---|---|
| `empresas.id_empresa` | `vagas.id_empresa` |
| `vagas.id_vaga` | `vaga_competencias.id_vaga` |
| `competencias.id_competencia` | `vaga_competencias.id_competencia` |
| `competencias.id_competencia` | `minhas_competencias.id_competencia` |
| `vagas.id_vaga` | `candidaturas.id_vaga` |

O Power BI costuma detectar e sugerir esses relacionamentos sozinho pelos
nomes das colunas — mas vale conferir cada um manualmente.

## Passo 4 — Criar as medidas DAX (o cálculo de aderência)

No painel **Dados**, clique com o botão direito na tabela `vaga_competencias`
e escolha **Nova medida**. Cole cada fórmula abaixo, uma de cada vez:

```dax
Total Exigido = COUNTROWS(vaga_competencias)
```

```dax
Ja Possuo =
CALCULATE(
    COUNTROWS(vaga_competencias),
    FILTER(
        vaga_competencias,
        NOT ISBLANK(RELATED(minhas_competencias[nivel]))
    )
)
```

```dax
% Aderencia = DIVIDE([Ja Possuo], [Total Exigido], 0)
```

A terceira fórmula é a mesma lógica da Query 10 do SQL — só que calculada
pelo Power BI em vez do SQLite.

## Passo 5 — Montar as visualizações

Na aba **Relatório**, monte pelo menos:

1. **Tabela**: `vagas[titulo]` + as medidas `Total Exigido`, `Ja Possuo`,
   `% Aderência` — ordenada do maior pro menor % Aderência.
2. **Gráfico de barras**: `competencias[nome]` no eixo, contagem de
   `vaga_competencias` como valor — mostra quais competências mais se
   repetem entre as vagas.
3. **Cartão (card)**: `% Aderência` média geral.
4. **Segmentação de dados (slicer)**: `empresas[nome]`, pra filtrar o
   painel inteiro por empresa com um clique.

## Próximos passos (Fase 4 da trilha)

Um modelo simples de Machine Learning que estima, a partir do texto de
uma vaga nova, quão aderente ela é ao meu perfil — uma versão automática
do que hoje calculamos manualmente com SQL e DAX.
