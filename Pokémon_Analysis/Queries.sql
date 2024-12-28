----------------------------------------------------------
-- Basic Analysis
----------------------------------------------------------

-- Find the number of Pokémon for each primary and secondary type
-- SELECT DISTINCT type_1, COUNT(type_1) 
-- FROM PokemonData
-- GROUP BY type_1
-- ORDER BY COUNT(type_1) DESC;

-- SELECT DISTINCT type_2, COUNT(type_2) 
-- FROM PokemonData
-- GROUP BY type_2
-- ORDER BY COUNT(type_2) DESC;

-- Identify the top 5 Pokémon with the highest total base stats
-- SELECT name, (hp + attack + defense + special_attack + special_defense + speed) AS total_base_stat
-- FROM PokemonData
-- ORDER BY total_stats DESC
-- LIMIT 5;

-- Calculate the average stats for Pokémon in each generation
-- SELECT generation, ROUND(AVG(hp),1) AS hp, ROUND(AVG(attack),1) AS attack, ROUND(AVG(defense),1) AS defense, ROUND(AVG(special_attack),1) AS special_attack, ROUND(AVG(special_defense),1) AS special_defense, ROUND(AVG(speed),1) AS speed
-- FROM PokemonData
-- GROUP BY generation;

-- List Pokémon whose total base stats exceed the average across all Pokémon
-- WITH TotalBaseStats AS (
--     SELECT name, (hp + attack + defense + special_attack + special_defense + speed) AS total_base_stat
--     FROM PokemonData
-- )
-- SELECT name, total_base_stat
-- FROM TotalBaseStats
-- WHERE total_base_stat > (SELECT AVG(total_base_stat) FROM TotalBaseStats);

-- Retrieve the names and weights of the lightest and heaviest Pokémon
-- SELECT name, weight_lb
-- FROM PokemonData
-- WHERE weight_lb = (SELECT MIN(weight_lb) FROM PokemonData);

-- SELECT name, weight_lb
-- FROM PokemonData
-- WHERE weight_lb = (SELECT MAX(weight_lb) FROM PokemonData);

----------------------------------------------------------
-- Intermediate Queries
----------------------------------------------------------

-- Find Pokémon that have both primary and secondary types defined

-- List all Pokémon with a speed greater than 100 and order them by speed descending

-- Show the average HP, Attack, and Defense for each type (both primary and secondary)

-- Find Pokémon taller than 80 inches and sort them by height descending

-- Determine the most frequent secondary type among all Pokémon

----------------------------------------------------------
-- Advanced Analysis
----------------------------------------------------------

-- Using the DamageTakenMultipliers table, calculate the total damage multiplier for Pokémon of a specific type combination (e.g., Fire/Water)

-- Identify which primary type has the lowest average damage multiplier against its weaknesses

-- Compare the average stats between Generation 1 and Generation 8 Pokémon

-- For each type, find the Pokémon with the highest Attack stat

-- Categorize Pokémon into weight classes (e.g., Light: <50 lbs, Medium: 50-150 lbs, Heavy: >150 lbs) and count how many fall into each class

----------------------------------------------------------
-- Complex Queries
----------------------------------------------------------

-- Identify Pokémon whose stats are above the average for their generation

-- Join the PokemonData and PokemonTypeDamageTaken tables to show Pokémon and their vulnerabilities

-- Find Pokémon that take the least damage across all attack types (lowest average damage multiplier)

-- Determine if there are any Pokémon with stats consistent across multiple generations

-- Calculate a custom “power index” for each Pokémon using a weighted formula: Power_Index=(2×Attack+Defense+Speed)/Weight And rank Pokémon based on this index

SELECT * FROM PokemonData;

SELECT * FROM PokemonTypeDamageTaken;

SELECT * FROM DamageTakenMultipliers;