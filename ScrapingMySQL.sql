
# Visualizando a tabela.
SELECT
	*
FROM
	ranking_ricos;
    
# Bilionário ordenados por idade.
SELECT
	*
FROM
	ranking_ricos
ORDER BY 
	Idade;

# Total de Patrimônio Líquido acumulado.
SELECT
	SUM(Patrimônio_Líquido)
FROM
	ranking_ricos;
    
# Média de idade.
SELECT
	AVG(Idade)
FROM
	ranking_ricos;
    
# Quantidade de Bilionários por país.
SELECT
	DISTINCT(País_Origem),
    count(País_Origem) as Quantidade
FROM
	ranking_ricos
GROUP BY
	País_Origem
ORDER BY
	Quantidade DESC;
	