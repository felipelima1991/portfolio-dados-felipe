-- ============================================================
-- PROJETO: Banco de Dados de Vagas — Fase 1 (SQL)
-- Autor: Felipe Oliveira de Lima
-- Descrição: Modelagem relacional das vagas de estágio em
-- Dados analisadas, para praticar SELECT, JOIN, GROUP BY e
-- chaves primárias/estrangeiras.
-- ============================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- Tabela: empresas
-- Uma linha por empresa que publicou vaga.
-- ------------------------------------------------------------
CREATE TABLE empresas (
    id_empresa      INTEGER PRIMARY KEY AUTOINCREMENT,
    nome            TEXT NOT NULL UNIQUE,
    setor           TEXT NOT NULL
);

-- ------------------------------------------------------------
-- Tabela: vagas
-- Uma linha por vaga. Cada vaga pertence a uma empresa (1:N).
-- ------------------------------------------------------------
CREATE TABLE vagas (
    id_vaga         INTEGER PRIMARY KEY AUTOINCREMENT,
    id_empresa      INTEGER NOT NULL,
    titulo          TEXT NOT NULL,
    localizacao     TEXT,
    modalidade      TEXT CHECK (modalidade IN ('Presencial', 'Híbrido', 'Remoto', 'Não informado')),
    tipo_vaga       TEXT NOT NULL DEFAULT 'Estágio',
    data_analise    DATE NOT NULL,
    FOREIGN KEY (id_empresa) REFERENCES empresas (id_empresa)
);

-- ------------------------------------------------------------
-- Tabela: competencias
-- Catálogo único de competências (técnicas ou comportamentais)
-- que aparecem nas vagas. Evita repetir texto solto.
-- ------------------------------------------------------------
CREATE TABLE competencias (
    id_competencia  INTEGER PRIMARY KEY AUTOINCREMENT,
    nome            TEXT NOT NULL UNIQUE,
    categoria       TEXT NOT NULL CHECK (categoria IN ('Técnica', 'Comportamental'))
);

-- ------------------------------------------------------------
-- Tabela associativa: vaga_competencias
-- Resolve o relacionamento N:N entre vagas e competências.
-- Uma vaga tem várias competências; uma competência aparece em
-- várias vagas.
-- ------------------------------------------------------------
CREATE TABLE vaga_competencias (
    id_vaga         INTEGER NOT NULL,
    id_competencia  INTEGER NOT NULL,
    exigencia       TEXT NOT NULL CHECK (exigencia IN ('Obrigatório', 'Desejável')),
    PRIMARY KEY (id_vaga, id_competencia),
    FOREIGN KEY (id_vaga) REFERENCES vagas (id_vaga),
    FOREIGN KEY (id_competencia) REFERENCES competencias (id_competencia)
);

-- ------------------------------------------------------------
-- Tabela: minhas_competencias
-- As competências que o Felipe já possui hoje, com o nível
-- atual. Usada para calcular aderência (Fase 1, query 10) e
-- vai servir de base para o "score de aderência" da Fase 4 (ML).
-- ------------------------------------------------------------
CREATE TABLE minhas_competencias (
    id_competencia  INTEGER PRIMARY KEY,
    nivel           TEXT NOT NULL CHECK (nivel IN ('Básico', 'Intermediário', 'Avançado', 'Em desenvolvimento')),
    FOREIGN KEY (id_competencia) REFERENCES competencias (id_competencia)
);

-- ------------------------------------------------------------
-- Tabela: candidaturas
-- Uma linha por candidatura feita a uma vaga (1:1 aqui, mas
-- modelada como tabela própria porque no futuro pode haver
-- reaplicação ou histórico de status).
-- ------------------------------------------------------------
CREATE TABLE candidaturas (
    id_candidatura  INTEGER PRIMARY KEY AUTOINCREMENT,
    id_vaga         INTEGER NOT NULL,
    data_candidatura DATE,
    status          TEXT NOT NULL CHECK (
        status IN ('CV ajustado', 'Candidatura enviada', 'Em processo', 'Entrevista', 'Recusado', 'Aprovado')
    ),
    versao_cv       TEXT,
    FOREIGN KEY (id_vaga) REFERENCES vagas (id_vaga)
);
