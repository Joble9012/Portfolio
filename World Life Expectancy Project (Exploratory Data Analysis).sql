#World Life Expectancy Project (Exploratory Data Analysis)


-- -- Displaying the data -- --

SELECT 
	*
FROM 
	world_life_expectancy
;


-- -- Looking at min, max, and life increase -- --

SELECT 
	Country, 
    MIN(Life_expectancy),
    MAX(Life_expectancy),
    ROUND(MAX(Life_expectancy) - MIN(Life_expectancy),1) AS Life_Increase_15_Years
FROM 
	world_life_expectancy
GROUP BY
	Country
HAVING MIN(Life_expectancy) <> 0
	AND MAX(Life_expectancy) <> 0 
ORDER BY
	Life_Increase_15_Years DESC
;


-- -- Looking at the average life expectancy -- --

SELECT 
	Year, ROUND(AVG(Life_expectancy),2)
FROM 
	world_life_expectancy
WHERE 
	Life_expectancy <> 0
GROUP BY
	Year
ORDER BY
	Year
;


-- -- Displaying the data -- --

SELECT 
	*
FROM 
	world_life_expectancy
;


-- -- Comparing life expectancy with GDP -- --

SELECT 
	Country,
    ROUND(AVG(Life_expectancy),1) AS Life_Exp,
    ROUND(AVG(GDP_per_capita),1) AS GDP
FROM 
	world_life_expectancy
GROUP BY
	Country
HAVING
	Life_Exp > 0
    AND GDP > 0
ORDER BY
	GDP DESC
;


-- -- Comparing the lowest and highest GDP and life expectancy -- --

SELECT
	SUM(CASE
		WHEN GDP_per_capita >= 2000 THEN 1
        ELSE 0
	END) AS High_GDP_COUNT,
    AVG(CASE
		WHEN GDP_per_capita >= 2000 THEN Life_expectancy
        ELSE NULL
	END) AS High_GDP_Life_Expectancy,
    SUM(CASE
		WHEN GDP_per_capita <= 2000 THEN 1
        ELSE 0
	END) AS Low_GDP_COUNT,
    AVG(CASE
		WHEN GDP_per_capita <= 2000 THEN Life_expectancy
        ELSE NULL
	END) AS Low_GDP_Life_Expectancy
FROM
	world_life_expectancy
;



-- -- Comparing life expectancy with BMI -- --

SELECT 
	Country,
    ROUND(AVG(Life_expectancy),1) AS Life_Exp,
    ROUND(AVG(BMI),1) AS BMI
FROM 
	world_life_expectancy
GROUP BY
	Country
HAVING
	Life_Exp > 0
    AND BMI > 0
ORDER BY
	BMI ASC
;


-- -- Looking at the rolling total of deaths -- -- 

SELECT 
	Country,
    Year,
    ROUND(AVG(Life_expectancy),1),
    Adult_mortality,
    SUM(Adult_mortality) OVER(PARTITION BY Country ORDER BY Year) AS Rolling_Total
FROM 
	world_life_expectancy
;





