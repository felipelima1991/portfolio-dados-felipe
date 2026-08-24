# Fase 2 — ETL em Python (automação de inserção de vagas)

**Parte de:** [Trilha de Projetos Práticos — Ciência de Dados](../Trilha_Projetos_Ciencia_Dados_Felipe.md)
**Depende de:** [Fase 1 — Banco de Dados de Vagas](../fase1-banco-vagas/README.md)
**Autor:** Felipe Oliveira de Lima

## Problema

Na Fase 1, toda vez que eu queria adicionar uma vaga nova ao banco, eu tinha
que editar `02_seed_data.sql` na mão — escrever o `INSERT` certo, lembrar os
nomes exatos das competências já cadastradas, não esquecer de nenhuma
vírgula. Fazer isso manualmente não escala e é fácil de errar.

## O que eu fiz

Um script Python que automatiza as 3 etapas clássicas de um pipeline de
dados:

- **Extract** — lê um arquivo `.txt` com o texto da vaga.
- **Transform** — identifica empresa, título, localização e modalidade a
  partir de campos estruturados, e varre a descrição da vaga procurando
  quais competências do catálogo (as mesmas 20 competências cadastradas na
  Fase 1) aparecem no texto, classificando cada uma como Obrigatório ou
  Desejável.
- **Load** — insere tudo no `vagas.db`, sem duplicar empresa nem vaga se o
  script rodar de novo por engano.

## Formato de entrada (por que não é 100% texto livre)

Eu decidi pedir um cabeçalho estruturado (`EMPRESA:`, `TITULO:`,
`LOCALIZACAO:`, `MODALIDADE:`) em vez de tentar adivinhar tudo a partir de
texto corrido. Isso é uma escolha de engenharia, não preguiça: extrair
"qual é o nome da empresa" de um texto qualquer exigiria um modelo de NLP de
verdade (isso é assunto pra Fase 4). Pedir 4 campos estruturados no topo do
arquivo é barato, confiável, e resolve 90% do problema com 10% do esforço.

## Bug real que apareceu no primeiro teste (e o que aprendi)

Na primeira versão, eu classificava Obrigatório/Desejável olhando uma
"janela" de 80 caracteres ao redor de cada competência encontrada no texto.
Isso pareceu razoável — até eu testar com uma lista de bullets:

```
- SQL (obrigatório)
- Excel avançado (obrigatório)
- Power BI (desejável)
- Python (desejável)
```

Como as linhas são curtas, a janela de 80 caracteres ao redor de "Python"
também pegava o "(obrigatório)" da linha do Excel logo acima — e como meu
código checava "obrigatório" antes de "desejável", tudo virava Obrigatório
por engano. Corrigi trocando a janela de caracteres por uma checagem
**linha a linha**: agora só considero o texto da mesma linha onde a
competência foi encontrada. Isso é mais preciso pra descrições em formato
de lista (o mais comum) e assume "Desejável" como padrão quando a vaga não
deixa claro — uma limitação honesta, não uma promessa de 100% de acerto.

## Como rodar

```bash
python3 etl_vagas.py vagas_brutas/exemplo_vaga.txt
```

Pra adicionar uma vaga sua, de verdade: copie `vagas_brutas/modelo_vaga.txt`,
preencha os campos e cole a descrição da vaga depois do separador `---`,
depois rode:

```bash
python3 etl_vagas.py vagas_brutas/nome-do-seu-arquivo.txt
```

## Testes que fiz antes de entregar

- Rodei com o arquivo de exemplo e conferi manualmente cada competência
  encontrada contra o que o texto realmente dizia.
- Rodei o **mesmo arquivo duas vezes** de propósito, pra confirmar que a
  segunda vez não duplica a vaga (o script detecta e avisa).
- Depois de inserir a vaga de teste, rodei de novo as 10 queries da Fase 1
  pra confirmar que elas continuam funcionando com o dado novo — inclusive
  a query de % de aderência já incluiu a vaga nova automaticamente, sem eu
  precisar mudar nada nas queries.

## Próximos passos (Fase 3 da trilha)

Conectar esse banco (agora alimentado automaticamente) a um dashboard de
verdade em Power BI ou Looker Studio, substituindo qualquer conferência
manual por um painel visual.
