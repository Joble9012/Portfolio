-- Count for each medical condition.
SELECT
	medical_condition, COUNT(medical_condition) AS count
FROM
	healthcare.patient_dataset
GROUP BY
	medical_condition;
    
-- Distribution of medical conditions within each gender category.
SELECT
	medical_condition, gender, COUNT(gender) AS number_of_patients
FROM
	healthcare.patient_dataset
GROUP BY
	medical_condition, gender
ORDER BY
	medical_condition ASC, gender ASC;

-- Average age of patients for each medical condition.
SELECT
	medical_condition, ROUND(AVG(age)) AS avg_age
FROM
	healthcare.patient_dataset
GROUP BY
	medical_condition;
  
-- Average bill of patients for each medical condition.
SELECT
	medical_condition, ROUND(AVG(billing_amount)) AS avg_billing
FROM
	healthcare.patient_dataset
GROUP BY
	medical_condition;
    
-- Distribution of medical conditions within each admission type.
SELECT
	medical_condition, admission_type, COUNT(medical_condition)
FROM
	healthcare.patient_dataset
GROUP BY
	medical_condition, admission_type;

-- The most common medication use for each medical condition.
WITH ranked_medications AS (
    SELECT
        medical_condition,
        medication,
        COUNT(medication) AS medication_count,
        ROW_NUMBER() OVER (PARTITION BY medical_condition ORDER BY COUNT(medication) DESC) AS rnk
    FROM
        healthcare.patient_dataset
    GROUP BY
        medical_condition, medication
)
SELECT
    medical_condition,
    medication,
    medication_count
FROM
    ranked_medications
WHERE
    rnk = 1;


