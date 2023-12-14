#World Life Expectancy Project (Data Cleaning)


-- -- Displaying the data -- --

SELECT 
	*
FROM 
	world_life_expectancy;
;


-- -- Identifing duplicate data -- --

SELECT 
	Country, 
    Year, 
    CONCAT(Country,Year), 
    COUNT(CONCAT(Country, Year))
FROM 
	world_life_expectancy
GROUP BY
	Country, Year, 
    CONCAT(Country, Year)
Having
	COUNT(CONCAT(Country, Year)) > 1
;


-- -- Identifing all the rows that have duplicates -- --

SELECT 
	*
FROM (
SELECT
	Row_ID,
    CONCAT(Country,Year), 
    ROW_NUMBER() OVER( PARTITION BY CONCAT(Country,Year) ORDER BY CONCAT(Country,Year)) as Row_Num
FROM 
	world_life_expectancy
) AS Row_table
WHERE 
	Row_Num > 1
;


-- -- Deleteing the duplicates from the dataset -- --

DELETE FROM 
	world_life_expectancy
WHERE
	Row_ID IN (
	SELECT 
		Row_ID
FROM (
SELECT
    CONCAT(Country,Year), 
    ROW_NUMBER() OVER( PARTITION BY CONCAT(Country,Year) ORDER BY CONCAT(Country,Year)) as Row_Num
FROM 
	world_life_expectancy
) AS Row_table
WHERE 
	Row_Num > 1
)
;


-- -- Indentifying missing data -- --

SELECT 
	*
FROM 
	world_life_expectancy
WHERE 
	Status = ' '
;


-- -- Filling in missing data -- --

UPDATE
	world_life_expectancy t1
JOIN
	world_life_expectancy t2
    ON t1.Country = t2.Country
SET
	t1.Satus = 'Developing'
WHERE
	t1.Status = ' '
AND t2.Status <> ' '
AND t2.Status = 'Developing'
;

UPDATE
	world_life_expectancy t1
JOIN
	world_life_expectancy t2
    ON t1.Country = t2.Country
SET
	t1.Satus = 'Developed'
WHERE
	t1.Status = ' '
AND t2.Status <> ' '
AND t2.Status = 'Developed'
;



;





