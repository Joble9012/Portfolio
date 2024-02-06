USE healthcare_dataset;

-- -- Data Retrieval -- --


# Retrieve all columns from the patient_data table for patients aged 30 and above.
SELECT *
FROM patient_data
WHERE age > 30;
# Select the names and birthdates of patients who were admitted in the last three months.
SELECT name, birthdate
FROM patient_data
WHERE date_of_admission >= (SELECT DATE_SUB(MAX(date_of_admission), INTERVAL 3 MONTH) FROM patient_data);


-- -- Filtering, Sorting, and Joins -- --


# Display the patient names and the top 10 billing amounts for those who have Anthem insurance.
SELECT pd.name, pd.billing_amount
FROM patient_data pd
JOIN insurance ip 
	ON pd.insurance_provider = ip.index
WHERE ip.insurance_name = 'Anthem'
ORDER BY pd.billing_amount desc
LIMIT 10;
# List patients, their ethnicity, and thier age in descending order of age.
SELECT pd.name, pd.age,e.ethnicity_name
FROM patient_data pd
JOIN ethnicity e
	on pd.ethncity = e.index
ORDER BY age desc;


-- -- Aggregation -- --


# Calculate the average age of patients in the dataset,round to nearest interger.
SELECT ROUND(avg(age))
FROM patient_data;
# Find the total billing amount for all patients, round to 2 decimals.
SELECT ROUND(SUM(billing_amount),2)
FROM patient_data;


-- -- Subqueries -- --


# Retrieve the names of patients who have emergency contact number starting with "215" listed in the emergency_contact table.
SELECT name
FROM patient_data pd
WHERE pd.id IN (SELECT id FROM emergency_contact WHERE emergency_contact_number like '+1 215%')
;
# Identify patients with a diabetes from the medical_record table.
SELECT name, id
FROM patient_data pd
WHERE pd.id IN (SELECT id from medical_record WHERE `diagnosis_and chronic_conditions` = "Diabetes")
;


-- -- Updating Records -- --


# Update the phone number for patient id 346 in the patient_data table.
SET SQL_SAFE_UPDATES = 0;

UPDATE patient_data
SET phone_num = "+1 263-4643-6930"
WHERE id = 346;

SELECT phone_num
FROM patient_data
WHERE id = 346;
# Modify the diagnosis for patient id 1056 to Hypertension, in the medical_record table.
UPDATE medical_record
SET `diagnosis_and chronic_conditions` = "hypertension"
WHERE id = 1056;

SELECT `diagnosis_and chronic_conditions`
FROM medical_record
WHERE id = 1056;


-- -- Inserting Records -- --


# Add a new patient to the patient_data table with a name and id.
INSERT INTO patient_data (id,name)
VALUES (1001, "Joble Thomas");

# Insert a  ethnicity and insurance to the new patient.
UPDATE patient_data
SET ethnicity = 5 AND insurance_provider = 2
WHERE id = 1001;

SELECT *
FROM patient_data
WHERE id = 1001;


-- -- Deletion -- --


# Remove the previous patient's record from the patient_data table.
DELETE FROM patient_data
WHERE id=1001 and name = "Joble Thomas";

# Delete an emergency contact from the emergency_contact table.
DELETE FROM emergency_contact
WHERE id=8534;


-- -- Grouping and Aggregation -- --


# Group patients by gender and calculate the average age for each group, round to nearest age.
SELECT gender, ROUND(AVG(age))
FROM patient_data
GROUP BY gender;

# Determine the maximum billing amount for each insurance in the dataset.
SELECT i.insurance_name, ROUND(max(pd.billing_amount),2)
FROM patient_data pd
JOIN insurance i 
	ON pd.insurance_provider = i.index
GROUP BY i.insurance_name
ORDER BY ROUND(max(pd.billing_amount),2) DESC;


-- -- Conditional Logic -- --


# Display patients who have allergies using a conditional statement.
SELECT pd.id,
	CASE
		WHEN mr.allergies = "" THEN "No"
        ELSE "Yes"
	END AS "Have Allergies"
FROM patient_data pd
JOIN medical_record mr
	on pd.id = mr.id
;


# Identify patients with a body temperature above a certain threshold from the vital_signs table.
SELECT pd.id,
	CASE
		WHEN vs.body_temp >100 THEN "High"
        WHEN vs.body_temp >98 THEN "Normal"
        ELSE "Low"
    END AS "Body Temperature Level"
FROM patient_data pd
JOIN vital_signs vs
	on pd.id=vs.id

