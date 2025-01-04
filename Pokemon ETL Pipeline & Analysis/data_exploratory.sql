-- 1. Top 3 strongest Pokémon (by attack) in each generation
SELECT generation, name, attack
FROM 
    (SELECT *, RANK() OVER (PARTITION BY generation ORDER BY attack DESC) AS rank
     FROM PokemonData) ranked
WHERE rank <= 3;

-- 2. Top 3 fastest Pokémon in each generation
SELECT generation, name, speed
FROM 
    (SELECT *, RANK() OVER (PARTITION BY generation ORDER BY speed DESC) AS rank
     FROM PokemonData) ranked
WHERE rank <= 3;

-- 3. Top 3 heaviest Pokémon in each generation
SELECT generation, name, weight_lb
FROM 
    (SELECT *, RANK() OVER (PARTITION BY generation ORDER BY weight_lb DESC) AS rank
     FROM PokemonData) ranked
WHERE rank <= 3;

-- 4. Top 3 tallest Pokémon in each generation
SELECT generation, name, height_in
FROM 
    (SELECT *, RANK() OVER (PARTITION BY generation ORDER BY height_in DESC) AS rank
    FROM PokemonData) ranked
WHERE rank <= 3;

-- 5. Top 3 Pokémon with the highest HP in each generation
SELECT generation, name, hp
FROM 
    (SELECT *, RANK() OVER (PARTITION BY generation ORDER BY hp DESC) AS rank
    FROM PokemonData) ranked
WHERE rank <= 3;

-- 6. Top 3 Pokémon with the highest defense in each generation
SELECT generation, name, defense
FROM 
    (SELECT *, RANK() OVER (PARTITION BY generation ORDER BY defense DESC) AS rank
    FROM PokemonData) ranked
WHERE rank <= 3;

-- 7. Pokémon with the highest total stats in each generation
SELECT generation, name, (hp + attack + defense + special_attack + special_defense + speed) AS total_stats
FROM PokemonData
ORDER BY generation, total_stats DESC;

-- 8. Pokémon with the lowest total stats in each generation
SELECT generation, name, (hp + attack + defense + special_attack + special_defense + speed) AS total_stats
FROM PokemonData
ORDER BY generation, total_stats ASC;

-- 9. Pokémon with the highest attack-to-weight ratio
SELECT name, attack, weight_lb, attack / weight_lb AS attack_to_weight
FROM PokemonData
ORDER BY attack_to_weight DESC
LIMIT 10;

-- 10. Pokémon with the highest HP-to-weight ratio
SELECT name, hp, weight_lb, hp / weight_lb AS hp_to_weight
FROM PokemonData
ORDER BY hp_to_weight DESC
LIMIT 10;


-- 11. Pokémon with the best offensive stats (attack + special_attack) compared to its generation average
SELECT name, generation, attack + special_attack AS offensive_power, 
       AVG(attack + special_attack) OVER (PARTITION BY generation) AS gen_avg_offense
FROM pokemon
WHERE (attack + special_attack) > (SELECT AVG(attack + special_attack) FROM pokemon WHERE generation = pokemon.generation);

-- 12. Pokémon whose stats (hp, attack, etc.) are all above the generation average
WITH GenAverages AS (
    SELECT generation,
           AVG(hp) AS avg_hp,
           AVG(attack) AS avg_attack,
           AVG(defense) AS avg_defense,
           AVG(special_attack) AS avg_special_attack,
           AVG(special_defense) AS avg_special_defense,
           AVG(speed) AS avg_speed
    FROM pokemon
    GROUP BY generation
)
SELECT p.name, p.generation
FROM PokemonData p
JOIN GenAverages g ON p.generation = g.generation
WHERE p.hp > g.avg_hp AND p.attack > g.avg_attack AND p.defense > g.avg_defense
  AND p.special_attack > g.avg_special_attack AND p.special_defense > g.avg_special_defense
  AND p.speed > g.avg_speed;