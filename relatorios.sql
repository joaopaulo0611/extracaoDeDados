-- CESTA MAIS BARATA (POR TIPO)

SELECT p.nome, p.preco, t.nome AS tipo
FROM produto p
JOIN tipo_produto t ON p.tipo_id = t.id
WHERE t.nome = 'arroz'
ORDER BY CAST(p.preco AS FLOAT) ASC
LIMIT 1;

SELECT p.nome, p.preco, t.nome AS tipo
FROM produto p
JOIN tipo_produto t ON p.tipo_id = t.id
WHERE t.nome = 'feijao'
ORDER BY CAST(p.preco AS FLOAT) ASC
LIMIT 1;

SELECT p.nome, p.preco, t.nome AS tipo
FROM produto p
JOIN tipo_produto t ON p.tipo_id = t.id
WHERE t.nome = 'oleo'
ORDER BY CAST(p.preco AS FLOAT) ASC
LIMIT 1;

SELECT p.nome, p.preco, t.nome AS tipo
FROM produto p
JOIN tipo_produto t ON p.tipo_id = t.id
WHERE t.nome = 'acucar'
ORDER BY CAST(p.preco AS FLOAT) ASC
LIMIT 1;

SELECT p.nome, p.preco, t.nome AS tipo
FROM produto p
JOIN tipo_produto t ON p.tipo_id = t.id
WHERE t.nome = 'cafe'
ORDER BY CAST(p.preco AS FLOAT) ASC
LIMIT 1;


-- CESTA MAIS CARA (POR TIPO)

SELECT p.nome, p.preco, t.nome AS tipo
FROM produto p
JOIN tipo_produto t ON p.tipo_id = t.id
WHERE t.nome = 'arroz'
ORDER BY CAST(p.preco AS FLOAT) DESC
LIMIT 1;

SELECT p.nome, p.preco, t.nome AS tipo
FROM produto p
JOIN tipo_produto t ON p.tipo_id = t.id
WHERE t.nome = 'feijao'
ORDER BY CAST(p.preco AS FLOAT) DESC
LIMIT 1;

SELECT p.nome, p.preco, t.nome AS tipo
FROM produto p
JOIN tipo_produto t ON p.tipo_id = t.id
WHERE t.nome = 'oleo'
ORDER BY CAST(p.preco AS FLOAT) DESC
LIMIT 1;

SELECT p.nome, p.preco, t.nome AS tipo
FROM produto p
JOIN tipo_produto t ON p.tipo_id = t.id
WHERE t.nome = 'acucar'
ORDER BY CAST(p.preco AS FLOAT) DESC
LIMIT 1;

SELECT p.nome, p.preco, t.nome AS tipo
FROM produto p
JOIN tipo_produto t ON p.tipo_id = t.id
WHERE t.nome = 'cafe'
ORDER BY CAST(p.preco AS FLOAT) DESC
LIMIT 1;


-- =========================================
-- CESTA MAIS BARATA (CORRETA - 1 POR TIPO)
-- =========================================

SELECT p.nome, p.preco, t.nome AS tipo
FROM produto p
JOIN tipo_produto t ON p.tipo_id = t.id
WHERE CAST(p.preco AS FLOAT) = (
    SELECT MIN(CAST(p2.preco AS FLOAT))
    FROM produto p2
    JOIN tipo_produto t2 ON p2.tipo_id = t2.id
    WHERE t2.nome = t.nome
)
AND t.nome IN ('arroz', 'feijao', 'oleo', 'acucar', 'cafe');


-- =========================================
-- CESTA MAIS CARA (CORRETA - 1 POR TIPO)
-- =========================================

SELECT p.nome, p.preco, t.nome AS tipo
FROM produto p
JOIN tipo_produto t ON p.tipo_id = t.id
WHERE CAST(p.preco AS FLOAT) = (
    SELECT MAX(CAST(p2.preco AS FLOAT))
    FROM produto p2
    JOIN tipo_produto t2 ON p2.tipo_id = t2.id
    WHERE t2.nome = t.nome
)
AND t.nome IN ('arroz', 'feijao', 'oleo', 'acucar', 'cafe');


-- =========================================
-- TOTAL DA CESTA MAIS BARATA (COM QUANTIDADE)
-- =========================================

SELECT SUM(
    CASE 
        WHEN t.nome = 'feijao' THEN CAST(p.preco AS FLOAT) * 2
        ELSE CAST(p.preco AS FLOAT)
    END
) AS total_cesta_min
FROM produto p
JOIN tipo_produto t ON p.tipo_id = t.id
WHERE CAST(p.preco AS FLOAT) = (
    SELECT MIN(CAST(p2.preco AS FLOAT))
    FROM produto p2
    JOIN tipo_produto t2 ON p2.tipo_id = t2.id
    WHERE t2.nome = t.nome
)
AND t.nome IN ('arroz', 'feijao', 'oleo', 'acucar', 'cafe');


-- =========================================
-- TOTAL DA CESTA MAIS CARA (COM QUANTIDADE)
-- =========================================

SELECT SUM(
    CASE 
        WHEN t.nome = 'feijao' THEN CAST(p.preco AS FLOAT) * 2
        ELSE CAST(p.preco AS FLOAT)
    END
) AS total_cesta_max
FROM produto p
JOIN tipo_produto t ON p.tipo_id = t.id
WHERE CAST(p.preco AS FLOAT) = (
    SELECT MAX(CAST(p2.preco AS FLOAT))
    FROM produto p2
    JOIN tipo_produto t2 ON p2.tipo_id = t2.id
    WHERE t2.nome = t.nome
)
AND t.nome IN ('arroz', 'feijao', 'oleo', 'acucar', 'cafe');