# Automated Data Cleaning


-- -- Creating the procedure -- --

DELIMITER $$
DROP PROCEDURE IF EXISTS Copy_and_Clean_Data;
CREATE PROCEDURE Copy_and_Clean_Data()
BEGIN


-- -- Creating our table -- --

CREATE TABLE IF NOT EXISTS `us_household_income_Cleaned` (
  `row_id` int DEFAULT NULL,
  `id` int DEFAULT NULL,
  `State_Code` int DEFAULT NULL,
  `State_Name` text,
  `State_ab` text,
  `County` text,
  `City` text,
  `Place` text,
  `Type` text,
  `Primary` text,
  `Zip_Code` int DEFAULT NULL,
  `Area_Code` int DEFAULT NULL,
  `ALand` int DEFAULT NULL,
  `AWater` int DEFAULT NULL,
  `Lat` double DEFAULT NULL,
  `Lon` double DEFAULT NULL,
  `TimeStamp` TIMESTAMP DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- -- Copying data to new table -- --

	INSERT INTO 
		us_project.us_household_income_Cleaned
	SELECT
		*,
        CURRENT_TIMESTAMP
	FROM
		us_project.us_household_income;


-- -- Cleaning the data -- --


	-- Remove duplicates --
DELETE FROM us_household_income_Cleaned
WHERE 
	row_id IN (
	SELECT row_id
FROM (
	SELECT row_id, id,
		ROW_NUMBER() OVER (
			PARTITION BY id, `TimeStamp`
			ORDER BY id, `TimeStamp`) AS row_num
	FROM 
		us_household_income_Cleaned
) duplicates
WHERE 
	row_num > 1
);

	-- Fixing typos and general standardization --
UPDATE us_household_income_Cleaned
SET State_Name = 'Georgia'
WHERE State_Name = 'georia';

UPDATE us_household_income_Cleaned
SET County = UPPER(County);

UPDATE us_household_income_Cleaned
SET City = UPPER(City);

UPDATE us_household_income_Cleaned
SET Place = UPPER(Place);

UPDATE us_household_income_Cleaned
SET State_Name = UPPER(State_Name);

UPDATE us_household_income_Cleaned
SET `Type` = 'CDP'
WHERE `Type` = 'CPD';

UPDATE us_household_income_Cleaned
SET `Type` = 'Borough'
WHERE `Type` = 'Boroughs';
END $$
DELIMITER ;


-- -- Calling the procedure -- --

CALL Copy_and_Clean_Data();


-- -- Creating and dropping event -- --

CREATE EVENT run_data_cleaning
	ON SCHEDULE EVERY 1 MINUTE
	DO CALL Copy_and_Clean_Data();
	
DROP EVENT run_data_cleaning;


-- -- Checking timestamp -- 

SELECT DISTINCT 
	TimeStamp 
FROM 
	us_project.us_household_income_Cleaned;









