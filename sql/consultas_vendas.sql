SELECT
    SUM(valor_venda) AS faturamento_total
FROM vendas;

SELECT
    COUNT(*) AS quantidade_vendas
FROM vendas;

SELECT
    AVG(valor_venda) AS ticket_medio
FROM vendas;

# Faturamento por categoria
SELECT  
    categoria,
    SUM(valor_venda) AS faturamento
FROM vendas
GROUP BY categoria
ORDER BY faturamento DESC;

# Faturamento por produto
SELECT
    produto,
    SUM(valor_venda) AS faturamento
FROM vendas
GROUP BY produto
ORDER BY faturamento DESC;

# faturamento por região
SELECT
    regiao,
    SUM(valor_venda) AS faturamento
FROM vendas
GROUP BY regiao
ORDER BY faturamento DESC;

SELECT 
    pagamento,
    SUM(valor_venda) AS faturamento
FROM vendas
GROUP BY pagamento
ORDER BY faturamento  DESC;

#Classificação de vendas por valor, criando três faixas de valor
SELECT  
    pedido,
    valor_venda,
    CASE    
        WHEN valor_venda < 1000 THEN 'Baixa'
        WHEN valor_venda <= 5000 THEN 'Média'
        ELSE 'Alta'
    END AS faixa_venda      #nome para a coluna com o resultado da busca
FROM vendas
ORDER BY valor_venda DESC;

#Quantidade de vendas por faixa de valor. Cada faixa armazenada em faixa_venda, depois tem uma contagem de cada faixa que fica em quantidade vendas. Agrupa cada faixa em faixa_venda e por último organiza quantidade_vendas do maior para o menor
SELECT
    CASE
        WHEN valor_venda < 1000 THEN 'Baixa'
        WHEN valor_venda <= 5000 THEN 'Média'
        ELSE 'Alta'
    END AS faixa_venda,
    COUNT(*) AS quantidade_vendas
FROM vendas
GROUP BY faixa_venda                
ORDER BY quantidade_vendas DESC

#Faturamento por faixa de valor
SELECT  
    CASE
        WHEN valor_venda < 1000 THEN 'Baixa'
        WHEN valor_venda <= 5000 THEN 'Média'
        ELSE 'Alta'
    END AS faixa_venda,
    COUNT(*) AS quantidade_vendas,
    SUM(valor_venda) AS faturamento
FROM vendas
GROUP BY faixa_venda
ORDER BY quantidade_vendas DESC;

# CTE para classificação das vendas - CTE cria uma tabela temporaria
WITH vendas_classificadas AS (
    SELECT
        pedido,
        valor_venda,
        CASE
            WHEN valor_venda < 1000 THEN 'Baixa'
            WHEN valor_venda <= 5000 THEN 'Média'
            ELSE 'Alta'
        END AS faixa_venda
    FROM vendas
)

SELECT
    faixa_venda,
    COUNT(*) AS quantidade_vendas,
    SUM(valor_venda) AS faturamento
FROM vendas_classificadas
GROUP BY faixa_venda
ORDER BY faturamento DESC;

#CTE + média de faturamento por categoria
WITH vendas_categoria AS(
    SELECT 
        categoria,
        valor_venda
    FROM vendas
)

SELECT
    categoria,
    COUNT(*) AS quantidade_vendas,
    SUM(valor_venda) AS faturamento_total
    AVG(valor_venda) AS faturamento_medio
FROM vendas_categoria
GROUP BY categoria
ORDER BY faturamento_medio DESC;     

#Produtos com faturamento superior a 1 milhão Havi ng filtra depois de agrupar. Com Wher e procuraria apenas vendas acima de 1000 enquanto Havin g procura os grupos com fatuamento quem ultrapasse 1 milhão
SELECT 
    produto,
    SUM(valor_venda) AS faturamento
FROM vendas
GROUP BY produto
HAVING SUM(valor_venda) > 1000000
ORDER BY faturamento DESC;
    

#Ranking dos produtos por faturamento. rank fará o rank e ove r define pelo que o rank será feito, nesse caso ordenado pela soma 
SELECT
    produto,
    SUM(valor_produto) AS faturamento,
    RANK() OVER(
        ORDER BY SUM(valor_venda) DESC
    ) AS Ranking
FROM vendas
GROUP BY produto
ORDER BY ranking;

#Ranking por categoria - o pertition faz um ranking separado para cada categoria. Exemplo: eletronico - notebook, etc, logo apos moveis com mesa etc...
SELECT
    categoria,
    produto,
    SUM(valor_venda) AS faturamento,
    RANK() OVER (
        PARTITION BY categoria
        ORDER BY SUM(valor_venda) DESC
    ) AS ranking_categoria
FROM vendas
GROUP BY categoria, produto
ORDER BY categoria, ranking_categoria;

#Participação de cada produto em faturamento total. O numeri c faz com que o numero seja de fato preciso, do contrário da erro.
WITH faturamento_produto AS (
    SELECT
        produto,
        SUM(valor_venda) AS faturamento
    FROM vendas
    GROUP BY produto
)

SELECT
    produto,
    faturamento,
    ROUND(
        (
        faturamento * 100.0 /
        SUM(faturamento) OVER ()
        )::numeric,
        2
    ) AS percentual_faturamento
FROM faturamento_produto
ORDER BY faturamento DESC;

#Faturamento acumulado por produto
WITH faturamento_produto AS (
    SELECT 
        produto,
        SUM(valor_venda) AS faturamento
    FROM vendas
    GROUP BY produto
)

SELECT
    produto,
    faturamento,
    SUM(faturamento) OVER (
        ORDER BY faturamento DESC
    )   AS faturamento_acumulado
FROM faturamento_produto
ORDER BY  faturamento DESC;

#Faturamento por mês
SELECT 
    DATE_TRUNC('month', data) AS mes,
    SUM(valor_venda) AS faturamento
FROM vendas
GROUP BY mes
ORDER BY mes;

#Mês com maior faturamento limi t1 pega somente 1, o que tem mais faturamento
SELECT
    DATE_TRUNC('month', data) AS mes,
    SUM(valor_venda) AS faturamento
FROM vendas
GROUP BY mes
ORDER BY faturamento DESC
LIMIT 1;

#Crescimento ou queda em relação ao mês anterior. Vai ter coluna mes, faturamento e faturamento_mes_anterior. iamgina mes 1, 2 3. mes 1 não tem um mes anterior a ele, então aparece na terceira coluna como n ull, ja em mes 2 aparece o valor do primeiro, em terceiro aparece do mes 3 assim por diante 
WITH faturamento_mensal AS (
    SELECT
        DATE_TRUNC('month', data) AS mes,
        SUM(valor_venda)::numeric AS faturamento
    FROM vendas
    GROUP BY DATE_TRUNC('month', data)
)

SELECT
    mes,
    faturamento,
    LAG(faturamento) OVER (
        ORDER BY mes
    ) AS faturamento_mes_anterior,
    ROUND(
        (faturamento - LAG(faturamento) OVER (ORDER BY mes))
        * 100.0
        / NULLIF(LAG(faturamento) OVER (ORDER BY mes), 0),
        2 )
    AS variacao_percentual
FROM faturamento_mensal
ORDER BY mes; 

#Faturamento acumulado por mês
WITH faturamento_mensal AS (
    SELECT
        DATE_TRUNC('month', data) AS mes,
        SUM(valor_venda) AS faturamento
    FROM vendas
    GROUP BY DATE_TRUNC('month', data)
)

SELECT
    mes,
    faturamento,
    SUM(faturamento) OVER (
        ORDER BY mes
    ) AS faturamento_acumulado
FROM faturamento_mensal
ORDER BY mes;