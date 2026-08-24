-- ============================================================
-- 10 QUERIES — praticando SELECT, WHERE/HAVING, JOIN, GROUP BY
-- Cada uma responde uma pergunta real sobre o processo seletivo.
-- ============================================================

-- 1) Quais vagas exigem SQL? (JOIN simples + WHERE)
-- Pergunta: em quais processos preciso estar afiado em SQL?
SELECT v.titulo, e.nome AS empresa, vc.exigencia
FROM vagas v
JOIN empresas e ON e.id_empresa = v.id_empresa
JOIN vaga_competencias vc ON vc.id_vaga = v.id_vaga
JOIN competencias c ON c.id_competencia = vc.id_competencia
WHERE c.nome = 'SQL';


-- 2) Quantas vagas exigem cada competência técnica? (GROUP BY)
-- Pergunta: onde devo focar meus estudos primeiro?
SELECT c.nome AS competencia, COUNT(*) AS qtd_vagas
FROM vaga_competencias vc
JOIN competencias c ON c.id_competencia = vc.id_competencia
WHERE c.categoria = 'Técnica'
GROUP BY c.nome
ORDER BY qtd_vagas DESC, competencia;


-- 3) Competências que aparecem em 3 ou mais vagas (GROUP BY + HAVING)
-- Pergunta: quais são as "apostas seguras" de estudo?
SELECT c.nome AS competencia, COUNT(*) AS qtd_vagas
FROM vaga_competencias vc
JOIN competencias c ON c.id_competencia = vc.id_competencia
GROUP BY c.nome
HAVING COUNT(*) >= 3
ORDER BY qtd_vagas DESC;


-- 4) Vagas e suas empresas, ordenadas por data de análise (JOIN)
SELECT v.titulo, e.nome AS empresa, v.modalidade, v.data_analise
FROM vagas v
JOIN empresas e ON e.id_empresa = v.id_empresa
ORDER BY v.data_analise, v.titulo;


-- 5) Vagas que exigem Python E SQL ao mesmo tempo (JOIN duplo + GROUP BY + HAVING)
-- Pergunta: quais vagas são as mais "técnicas" das cinco?
SELECT v.titulo, e.nome AS empresa
FROM vagas v
JOIN empresas e ON e.id_empresa = v.id_empresa
JOIN vaga_competencias vc ON vc.id_vaga = v.id_vaga
JOIN competencias c ON c.id_competencia = vc.id_competencia
WHERE c.nome IN ('Python', 'SQL')
GROUP BY v.id_vaga
HAVING COUNT(DISTINCT c.nome) = 2;


-- 6) Competências obrigatórias por vaga (WHERE)
-- Pergunta: o que é inegociável em cada processo?
SELECT v.titulo, c.nome AS competencia
FROM vagas v
JOIN vaga_competencias vc ON vc.id_vaga = v.id_vaga
JOIN competencias c ON c.id_competencia = vc.id_competencia
WHERE vc.exigencia = 'Obrigatório'
ORDER BY v.titulo, c.nome;


-- 7) Quantidade de competências (obrigatórias vs desejáveis) por vaga (GROUP BY duplo)
-- Pergunta: qual vaga tem a barra técnica mais alta?
SELECT v.titulo, vc.exigencia, COUNT(*) AS qtd
FROM vagas v
JOIN vaga_competencias vc ON vc.id_vaga = v.id_vaga
GROUP BY v.titulo, vc.exigencia
ORDER BY v.titulo, vc.exigencia;


-- 8) Competências que a vaga pede e o Felipe AINDA NÃO TEM (LEFT JOIN)
-- Pergunta: qual é exatamente o gap de estudo por vaga?
SELECT v.titulo, c.nome AS competencia_faltante, vc.exigencia
FROM vaga_competencias vc
JOIN vagas v ON v.id_vaga = vc.id_vaga
JOIN competencias c ON c.id_competencia = vc.id_competencia
LEFT JOIN minhas_competencias mc ON mc.id_competencia = c.id_competencia
WHERE mc.id_competencia IS NULL
ORDER BY v.titulo, vc.exigencia, c.nome;


-- 9) Status atual de todas as candidaturas (JOIN simples)
SELECT e.nome AS empresa, v.titulo, cand.status, cand.versao_cv
FROM candidaturas cand
JOIN vagas v ON v.id_vaga = cand.id_vaga
JOIN empresas e ON e.id_empresa = v.id_empresa
ORDER BY e.nome;


-- 10) Percentual de aderência por vaga: quantas competências pedidas o Felipe já tem
-- (JOIN + LEFT JOIN + agregação — a query mais "completa" do conjunto)
-- Pergunta: em qual vaga meu perfil ATUAL já é mais forte?
SELECT
    v.titulo,
    COUNT(vc.id_competencia) AS total_exigido,
    SUM(CASE WHEN mc.id_competencia IS NOT NULL THEN 1 ELSE 0 END) AS ja_possuo,
    ROUND(
        100.0 * SUM(CASE WHEN mc.id_competencia IS NOT NULL THEN 1 ELSE 0 END)
        / COUNT(vc.id_competencia), 1
    ) AS percentual_aderencia
FROM vagas v
JOIN vaga_competencias vc ON vc.id_vaga = v.id_vaga
LEFT JOIN minhas_competencias mc ON mc.id_competencia = vc.id_competencia
GROUP BY v.titulo
ORDER BY percentual_aderencia DESC;
