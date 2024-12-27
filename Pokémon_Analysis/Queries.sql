----------------------------------------------------------
-- Basic Analysis
----------------------------------------------------------

-- Find the number of Pokémon for each primary and secondary type

-- Identify the top 5 Pokémon with the highest total base stats

-- Calculate the average stats for Pokémon in each generation

-- List Pokémon whose total base stats exceed the average across all Pokémon

-- Retrieve the names and weights of the lightest and heaviest Pokémon

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