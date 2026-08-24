-- ============================================================
-- SEED DATA — dados reais das 5 vagas já analisadas no processo
-- seletivo do Felipe (estágio em Dados)
-- ============================================================

-- ------------------------------------------------------------
-- EMPRESAS
-- ------------------------------------------------------------
INSERT INTO empresas (nome, setor) VALUES
    ('Na Prática', 'Educação / EdTech'),
    ('Syngenta',   'Agro / Inovação Agrícola'),
    ('Goop',       'Tecnologia / TI'),
    ('SYOS',       'IoT / Cadeia do Frio'),
    ('Red Bull',   'Bebidas / Bens de Consumo');

-- ------------------------------------------------------------
-- VAGAS
-- ------------------------------------------------------------
INSERT INTO vagas (id_empresa, titulo, localizacao, modalidade, tipo_vaga, data_analise) VALUES
    ((SELECT id_empresa FROM empresas WHERE nome = 'Na Prática'),
        'Estágio - Tecnologia, Dados & BI', 'São Paulo', 'Não informado', 'Estágio', '2026-08-24'),
    ((SELECT id_empresa FROM empresas WHERE nome = 'Syngenta'),
        'Programa de Estágio | 2º semestre 2026', 'São Paulo', 'Não informado', 'Estágio', '2026-08-24'),
    ((SELECT id_empresa FROM empresas WHERE nome = 'Goop'),
        'Estágio em TI – Foco em Dados', 'São Paulo', 'Presencial', 'Estágio', '2026-08-24'),
    ((SELECT id_empresa FROM empresas WHERE nome = 'SYOS'),
        'Estagiário de Ciência de Dados', 'São Paulo', 'Não informado', 'Estágio', '2026-08-24'),
    ((SELECT id_empresa FROM empresas WHERE nome = 'Red Bull'),
        'Estágio em Data & Analytics (Sistemas)', 'São Paulo e Região', 'Presencial', 'Estágio', '2026-08-24');

-- ------------------------------------------------------------
-- COMPETÊNCIAS (catálogo único — evita repetir texto solto)
-- ------------------------------------------------------------
INSERT INTO competencias (nome, categoria) VALUES
    ('SQL', 'Técnica'),
    ('Power BI', 'Técnica'),
    ('Looker Studio', 'Técnica'),
    ('Metabase', 'Técnica'),
    ('Excel', 'Técnica'),
    ('Python', 'Técnica'),
    ('JavaScript', 'Técnica'),
    ('Pacote Office', 'Técnica'),
    ('PowerPoint', 'Técnica'),
    ('Inglês Intermediário', 'Técnica'),
    ('Apresentações Gerenciais', 'Técnica'),
    ('Git / Versionamento', 'Técnica'),
    ('AWS', 'Técnica'),
    ('Machine Learning', 'Técnica'),
    ('Comunicação', 'Comportamental'),
    ('Organização', 'Comportamental'),
    ('Perfil Colaborativo', 'Comportamental'),
    ('Curiosidade', 'Comportamental'),
    ('Autorresponsabilidade', 'Comportamental'),
    ('Proatividade', 'Comportamental');

-- ------------------------------------------------------------
-- VAGA_COMPETENCIAS — o que cada vaga pede, e se é obrigatório
-- (padrão: SELECT ... UNION ALL SELECT ..., portável entre bancos)
-- ------------------------------------------------------------

-- Na Prática (Estágio - Tecnologia, Dados & BI)
INSERT INTO vaga_competencias (id_vaga, id_competencia, exigencia)
SELECT v.id_vaga, c.id_competencia, x.exigencia
FROM (
    SELECT 'Power BI' AS competencia, 'Desejável' AS exigencia
    UNION ALL SELECT 'Looker Studio', 'Desejável'
    UNION ALL SELECT 'Metabase', 'Desejável'
    UNION ALL SELECT 'SQL', 'Desejável'
    UNION ALL SELECT 'Excel', 'Desejável'
    UNION ALL SELECT 'Python', 'Desejável'
    UNION ALL SELECT 'JavaScript', 'Desejável'
    UNION ALL SELECT 'Comunicação', 'Obrigatório'
    UNION ALL SELECT 'Organização', 'Obrigatório'
) AS x
JOIN vagas v ON v.titulo = 'Estágio - Tecnologia, Dados & BI'
JOIN competencias c ON c.nome = x.competencia;

-- Syngenta (Programa de Estágio)
INSERT INTO vaga_competencias (id_vaga, id_competencia, exigencia)
SELECT v.id_vaga, c.id_competencia, x.exigencia
FROM (
    SELECT 'Pacote Office' AS competencia, 'Desejável' AS exigencia
    UNION ALL SELECT 'Inglês Intermediário', 'Desejável'
    UNION ALL SELECT 'Apresentações Gerenciais', 'Desejável'
    UNION ALL SELECT 'Perfil Colaborativo', 'Obrigatório'
    UNION ALL SELECT 'Curiosidade', 'Obrigatório'
    UNION ALL SELECT 'Autorresponsabilidade', 'Obrigatório'
) AS x
JOIN vagas v ON v.titulo = 'Programa de Estágio | 2º semestre 2026'
JOIN competencias c ON c.nome = x.competencia;

-- Goop (Estágio em TI – Foco em Dados)
INSERT INTO vaga_competencias (id_vaga, id_competencia, exigencia)
SELECT v.id_vaga, c.id_competencia, x.exigencia
FROM (
    SELECT 'SQL' AS competencia, 'Obrigatório' AS exigencia
    UNION ALL SELECT 'Power BI', 'Obrigatório'
    UNION ALL SELECT 'Excel', 'Obrigatório'
    UNION ALL SELECT 'Python', 'Desejável'
    UNION ALL SELECT 'Git / Versionamento', 'Desejável'
    UNION ALL SELECT 'Curiosidade', 'Obrigatório'
    UNION ALL SELECT 'Comunicação', 'Obrigatório'
) AS x
JOIN vagas v ON v.titulo = 'Estágio em TI – Foco em Dados'
JOIN competencias c ON c.nome = x.competencia;

-- SYOS (Estagiário de Ciência de Dados)
INSERT INTO vaga_competencias (id_vaga, id_competencia, exigencia)
SELECT v.id_vaga, c.id_competencia, x.exigencia
FROM (
    SELECT 'Python' AS competencia, 'Obrigatório' AS exigencia
    UNION ALL SELECT 'SQL', 'Obrigatório'
    UNION ALL SELECT 'AWS', 'Obrigatório'
    UNION ALL SELECT 'Pacote Office', 'Obrigatório'
    UNION ALL SELECT 'Machine Learning', 'Obrigatório'
) AS x
JOIN vagas v ON v.titulo = 'Estagiário de Ciência de Dados'
JOIN competencias c ON c.nome = x.competencia;

-- Red Bull (Estágio em Data & Analytics - Sistemas)
INSERT INTO vaga_competencias (id_vaga, id_competencia, exigencia)
SELECT v.id_vaga, c.id_competencia, x.exigencia
FROM (
    SELECT 'Excel' AS competencia, 'Obrigatório' AS exigencia
    UNION ALL SELECT 'PowerPoint', 'Obrigatório'
    UNION ALL SELECT 'Inglês Intermediário', 'Obrigatório'
    UNION ALL SELECT 'Comunicação', 'Obrigatório'
    UNION ALL SELECT 'Proatividade', 'Obrigatório'
    UNION ALL SELECT 'Curiosidade', 'Obrigatório'
) AS x
JOIN vagas v ON v.titulo = 'Estágio em Data & Analytics (Sistemas)'
JOIN competencias c ON c.nome = x.competencia;

-- ------------------------------------------------------------
-- MINHAS_COMPETENCIAS — o que o Felipe já tem hoje, de forma
-- honesta (só o que está comprovado no CV, sem inflar)
-- ------------------------------------------------------------
INSERT INTO minhas_competencias (id_competencia, nivel)
SELECT c.id_competencia, x.nivel
FROM (
    SELECT 'SQL' AS competencia, 'Em desenvolvimento' AS nivel
    UNION ALL SELECT 'Excel', 'Avançado'
    UNION ALL SELECT 'Comunicação', 'Avançado'
    UNION ALL SELECT 'Organização', 'Avançado'
    UNION ALL SELECT 'Perfil Colaborativo', 'Avançado'
    UNION ALL SELECT 'Curiosidade', 'Avançado'
    UNION ALL SELECT 'Proatividade', 'Avançado'
    UNION ALL SELECT 'Autorresponsabilidade', 'Avançado'
) AS x
JOIN competencias c ON c.nome = x.competencia;

-- ------------------------------------------------------------
-- CANDIDATURAS — status atual de cada processo
-- ------------------------------------------------------------
INSERT INTO candidaturas (id_vaga, data_candidatura, status, versao_cv)
SELECT v.id_vaga, NULL, 'CV ajustado', x.versao_cv
FROM (
    SELECT 'Estágio - Tecnologia, Dados & BI' AS titulo, 'CV_Felipe_Lima_Dados_BI_NaPratica.docx' AS versao_cv
    UNION ALL SELECT 'Programa de Estágio | 2º semestre 2026', 'CV_Felipe_Lima_Syngenta_Estagio.docx'
    UNION ALL SELECT 'Estágio em TI – Foco em Dados', 'CV_Felipe_Lima_Goop_TI_Dados.docx'
    UNION ALL SELECT 'Estagiário de Ciência de Dados', 'CV_Felipe_Lima_SYOS_Ciencia_Dados.docx'
    UNION ALL SELECT 'Estágio em Data & Analytics (Sistemas)', 'CV_Felipe_Lima_RedBull_Data_Analytics.docx'
) AS x
JOIN vagas v ON v.titulo = x.titulo;
