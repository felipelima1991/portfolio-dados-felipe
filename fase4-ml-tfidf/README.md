# Fase 4 — Estimativa de aderência com TF-IDF + similaridade de cosseno

**Parte de:** [Trilha de Projetos Práticos — Ciência de Dados](../Trilha_Projetos_Ciencia_Dados_Felipe.md)
**Depende de:** [Fase 1](../fase1-banco-vagas/README.md), [Fase 2](../fase2-etl-python/README.md), [Fase 3](../fase3-dashboard-powerbi/README.md)
**Autor:** Felipe Oliveira de Lima

## Problema

A Fase 2 só reconhece uma competência se o texto da vaga usar exatamente
a mesma palavra do catálogo fixo de 20 competências já cadastradas. Se
uma vaga nova pedir "Business Intelligence" em vez de "Power BI", ou
"planilhas eletrônicas avançadas" em vez de "Excel", o script simplesmente
não vê nada ali.

## Por que não um classificador supervisionado "de verdade"

Eu tenho **6 vagas** no banco. Treinar um modelo supervisionado (que
aprende um padrão geral a partir de exemplos rotulados) com 6 linhas não
geraria nada estatisticamente confiável — é dado de menos pra qualquer
coisa generalizar. Optei por uma técnica que funciona mesmo com poucos
documentos: **TF-IDF + similaridade de cosseno**, que mede o quão
parecido o texto do meu perfil é do texto de cada vaga, sem precisar
"aprender" com muitos exemplos rotulados.

## O que o TF-IDF resolve — e o que ele NÃO resolve (correção honesta)

Achei importante testar minha própria hipótese antes de documentar isso
como se funcionasse perfeitamente. Fiz um teste real com uma vaga fictícia
usando sinônimos de propósito:

```
"...conhecimento em ferramentas de Business Intelligence e planilhas
eletrônicas avançadas... Perfil com bastante curiosidade... boa
comunicação com times não técnicos."
```

Resultado: **7,4%** de similaridade — bem baixo. Investigando, descobri
que **TF-IDF não entende sinônimos**. Ele só compara palavras que
aparecem literalmente nos dois textos — "Business Intelligence" e "Power
BI" são, pra ele, duas sequências de caracteres completamente diferentes,
sem nenhuma relação. Só "curiosidade" e "comunicação" contribuíram pro
score, porque essas palavras aparecem literalmente no meu perfil também.

**O que o TF-IDF de fato melhora em relação à Fase 2:**
- Não fica preso ao catálogo fixo de 20 competências — qualquer palavra
  do texto conta, não só as pré-cadastradas.
- Dá um placar contínuo (0% a 100%), não um "achou/não achou" binário.
- Pondera por raridade da palavra (uma competência rara pesa mais que
  uma que aparece em toda vaga).

**O que ele não resolve** (e eu quase prometi que resolvia, até testar):
reconhecer que dois termos diferentes significam a mesma coisa. Isso
exigiria uma técnica de **embeddings semânticos** (word2vec, ou modelos
tipo Sentence-Transformers), que fica como ideia pra uma fase futura.

## Por que o ranking do TF-IDF ficou diferente do SQL/DAX

Comparando os dois métodos, a ordem das vagas muda bastante — a vaga da
Syngenta, que era a 4ª colocada no SQL (50%), virou a 1ª no TF-IDF
(65,9%). Não é bug: são duas perguntas diferentes.

- **SQL/DAX (Fase 1 e 3)** pergunta: *"Das competências que essa vaga
  exige, quantas eu já tenho?"* — uma fração direta de cobertura.
- **TF-IDF (Fase 4)** pergunta: *"O quão parecido é, no geral, o texto do
  meu perfil do texto dessa vaga?"* — e penaliza palavras que aparecem em
  muitas vagas (como "Curiosidade", que quase toda vaga pede), dando mais
  peso pras raras.

A vaga da Syngenta é quase inteira feita de competências comportamentais
que batem exatamente com o que tenho classificado como "Avançado" no meu
perfil (peso maior no documento) — por isso a similaridade alta, mesmo
sem cobrir 100% dos requisitos técnicos da vaga.

## Como rodar

```bash
# Reavaliar as 6 vagas que já estão no banco
python3 estimar_aderencia.py

# Avaliar uma vaga nova (mesmo formato de arquivo da Fase 2)
python3 estimar_aderencia.py caminho/para/vaga_nova.txt
```

## Próximos passos

- Trocar TF-IDF por embeddings semânticos (ex: Sentence-Transformers),
  pra resolver de verdade o problema dos sinônimos que documentei aqui.
- Continuar alimentando o banco com mais vagas via Fase 2 — com uma base
  maior, um classificador supervisionado de verdade passa a fazer sentido.
