def create_damage_multipliers(cursor):
    # SQL to create damage multipliers
    insert_multipliers = """
    CREATE TEMP TABLE DamageTakenAggregated AS
    SELECT
        Defender,
        MAX(CASE WHEN Attacker = 'Normal' THEN Multiplier END) AS normal,
        MAX(CASE WHEN Attacker = 'Fire' THEN Multiplier END) AS fire,
        MAX(CASE WHEN Attacker = 'Water' THEN Multiplier END) AS water,
        MAX(CASE WHEN Attacker = 'Electric' THEN Multiplier END) AS electric,
        MAX(CASE WHEN Attacker = 'Grass' THEN Multiplier END) AS grass,
        MAX(CASE WHEN Attacker = 'Ice' THEN Multiplier END) AS ice,
        MAX(CASE WHEN Attacker = 'Fighting' THEN Multiplier END) AS fighting,
        MAX(CASE WHEN Attacker = 'Poison' THEN Multiplier END) AS poison,
        MAX(CASE WHEN Attacker = 'Ground' THEN Multiplier END) AS ground,
        MAX(CASE WHEN Attacker = 'Flying' THEN Multiplier END) AS flying,
        MAX(CASE WHEN Attacker = 'Psychic' THEN Multiplier END) AS psychic,
        MAX(CASE WHEN Attacker = 'Bug' THEN Multiplier END) AS bug,
        MAX(CASE WHEN Attacker = 'Rock' THEN Multiplier END) AS rock,
        MAX(CASE WHEN Attacker = 'Ghost' THEN Multiplier END) AS ghost,
        MAX(CASE WHEN Attacker = 'Dragon' THEN Multiplier END) AS dragon,
        MAX(CASE WHEN Attacker = 'Dark' THEN Multiplier END) AS dark,
        MAX(CASE WHEN Attacker = 'Steel' THEN Multiplier END) AS steel
    FROM DamageTakenMultipliers
    GROUP BY Defender;

    WITH type_multipliers AS (
        SELECT
            p.pokemon_id,
            COALESCE(da1.normal, 1) * COALESCE(da2.normal, 1) AS normal,
            COALESCE(da1.fire, 1) * COALESCE(da2.fire, 1) AS fire,
            COALESCE(da1.water, 1) * COALESCE(da2.water, 1) AS water,
            COALESCE(da1.electric, 1) * COALESCE(da2.electric, 1) AS electric,
            COALESCE(da1.grass, 1) * COALESCE(da2.grass, 1) AS grass,
            COALESCE(da1.ice, 1) * COALESCE(da2.ice, 1) AS ice,
            COALESCE(da1.fighting, 1) * COALESCE(da2.fighting, 1) AS fighting,
            COALESCE(da1.poison, 1) * COALESCE(da2.poison, 1) AS poison,
            COALESCE(da1.ground, 1) * COALESCE(da2.ground, 1) AS ground,
            COALESCE(da1.flying, 1) * COALESCE(da2.flying, 1) AS flying,
            COALESCE(da1.psychic, 1) * COALESCE(da2.psychic, 1) AS psychic,
            COALESCE(da1.bug, 1) * COALESCE(da2.bug, 1) AS bug,
            COALESCE(da1.rock, 1) * COALESCE(da2.rock, 1) AS rock,
            COALESCE(da1.ghost, 1) * COALESCE(da2.ghost, 1) AS ghost,
            COALESCE(da1.dragon, 1) * COALESCE(da2.dragon, 1) AS dragon,
            COALESCE(da1.dark, 1) * COALESCE(da2.dark, 1) AS dark,
            COALESCE(da1.steel, 1) * COALESCE(da2.steel, 1) AS steel
        FROM PokemonData p
        LEFT JOIN (
            SELECT DISTINCT Defender, normal, fire, water, electric, grass, ice, fighting, poison, ground,
                            flying, psychic, bug, rock, ghost, dragon, dark, steel
            FROM DamageTakenAggregated
        ) da1 ON LOWER(p.type_1) = LOWER(da1.Defender)
        LEFT JOIN (
            SELECT DISTINCT Defender, normal, fire, water, electric, grass, ice, fighting, poison, ground,
                            flying, psychic, bug, rock, ghost, dragon, dark, steel
            FROM DamageTakenAggregated
        ) da2 ON LOWER(p.type_2) = LOWER(da2.Defender)
    )
    INSERT INTO PokemonTypeDamageTaken (
        pokemon_id,
        normal,
        fire,
        water,
        electric,
        grass,
        ice,
        fighting,
        poison,
        ground,
        flying,
        psychic,
        bug,
        rock,
        ghost,
        dragon,
        dark,
        steel
    )
    SELECT *
    FROM type_multipliers tm
    WHERE NOT EXISTS (
        SELECT 1
        FROM PokemonTypeDamageTaken ptdt
        WHERE ptdt.pokemon_id = tm.pokemon_id);
    """
    cursor.execute(insert_multipliers)