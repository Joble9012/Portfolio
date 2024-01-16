-- How many records (entries) are there in the dataset?

SELECT COUNT(Name) AS '# of Records'
FROM healthcare.patients_info;

-- What are the unique values for the columns?

SELECT DISTINCT `Blood Type`
FROM healthcare.patients_info;

SELECT DISTINCT `Medical Condition`
FROM healthcare.patients_info;
    
SELECT DISTINCT `Admission Type`
FROM healthcare.patients_info;
    
SELECT DISTINCT `Medication`
FROM healthcare.patients_info;
    
SELECT DISTINCT `Test Results`
FROM healthcare.patients_info;
    
SELECT DISTINCT `Insurance Provider`
FROM healthcare.patients_info;
    
-- What is the range of ages for the patients?

SELECT Min(Age), Max(Age)
FROM healthcare.patients_info;

-- How many different hospitals are included in the dataset?

SELECT COUNT(DISTINCT `Hospital`)
FROM healthcare.patients_info;

-- What is the distribution of different medical conditions among the patients?

SELECT `Medical Condition`, COUNT(`Medical Condition`)
FROM healthcare.patients_info
GROUP BY `Medical Condition`
ORDER BY COUNT(`Medical Condition`) DESC;

-- How many patients have been admitted with each type of admission (Emergency, Elective, Urgent)?

SELECT `Admission Type`, COUNT(`Admission Type`)
FROM healthcare.patients_info
GROUP BY `Admission Type`
ORDER BY COUNT(`Admission Type`) DESC;

-- Can you find the average age of patients admitted under different types of admissions?

SElECT`Admission Type`, ROUND(AVG(`AGE`))
FROM healthcare.patients_info
GROUP BY `Admission Type`;

-- What is the total billing amount for healthcare services provided?

SELECT CONCAT('$', FORMAT(SUM(`Billing Amount`),2)) AS 'Total Billing Amount'
FROM healthcare.patients_info;

-- Is there any correlation between the billing amount and the type of admission?

SELECT CONCAT('$', FORMAT(AVG(`Billing Amount`),2)) AS 'Total Billing Amount', `Admission Type`
FROM healthcare.patients_info
GROUP BY `Admission Type`;

-- Which insurance provider appears most frequently in the dataset?

SELECT `Insurance Provider`, COUNT(`Insurance Provider`)
FROM healthcare.patients_info
GROUP BY `Insurance Provider`
ORDER BY COUNT(`Insurance Provider`) DESC;

-- What is the average length of stay for patients in the hospital?

SELECT ROUND(AVG(DATEDIFF(`Discharge Date`,`Date of Admission`)),1) AS 'AVG Length of Stay in Days'
FROM healthcare.patients_info;

-- How many patients were admitted each month/year?

SELECT
	MONTH(`Date of Admission`) AS 'Month #', COUNT(MONTH(`Date of Admission`)) AS 'Monthly Admissions'
FROM healthcare.patients_info
GROUP BY MONTH(`Date of Admission`)
ORDER BY 
	MONTH(`Date of Admission`) ASC;
    
SELECT YEAR(`Date of Admission`) AS 'Year', COUNT(YEAR(`Date of Admission`)) AS 'Yearly Admissions'
FROM healthcare.patients_info
GROUP BY YEAR(`Date of Admission`)
ORDER BY YEAR(`Date of Admission`) ASC;

-- How many different types of medications were administered during admissions?

SELECT DISTINCT `Medication`, COUNT(`Medication`) AS 'Count'
FROM healthcare.patients_info
GROUP BY `Medication`
ORDER BY COUNT(`Medication`) DESC;

-- What are the most common test results observed among patients?

SELECT DISTINCT `Test Results`, COUNT(`Test Results`) AS 'Count'
FROM healthcare.patients_info
GROUP BY `Test Results`
ORDER BY COUNT(`Test Results`) DESC;
