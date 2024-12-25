import requests
import pandas as pd
import psycopg2

base_url = "https://pokeapi.co/api/v2/"

# Get all Pokémon names
def get_all_pokemon_names():
    url = f"{base_url}pokemon"
    all_pokemon = []
    
    while url:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            all_pokemon.extend(p['name'] for p in data['results'])
            url = data['next']
        else:
            print(f"Failed to retrieve data {response.status_code}")
            break

    return all_pokemon

# Get detailed information about a single Pokémon
def get_pokemon_info(name):
    url = f"{base_url}pokemon/{name}"
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        print(f"Failed to retrieve data {response.status_code}")
        return None
    
# Get generation based on the Pokémon's ID
def get_generation(pokemon_id):
    if 1 <= pokemon_id <= 151:
        return 1
    elif 152 <= pokemon_id <= 251:
        return 2
    elif 252 <= pokemon_id <= 386:
        return 3
    elif 387 <= pokemon_id <= 493:
        return 4
    elif 494 <= pokemon_id <= 649:
        return 5
    elif 650 <= pokemon_id <= 721:
        return 6
    elif 722 <= pokemon_id <= 809:
        return 7
    elif 810 <= pokemon_id <= 898:
        return 8
    else:
        return None
    
# Collect Pokémon data
all_pokemon_names = get_all_pokemon_names()
pokemon_data_list = []

for pokemon_name in all_pokemon_names[:10]:
    pokemon_info = get_pokemon_info(pokemon_name)
    if pokemon_info:
        pokemon_id = pokemon_info['id']
        pokemon_data = {
            "ID": pokemon_id,
            "Name": pokemon_info['name'].capitalize(),
            "Type_1": pokemon_info['types'][0]['type']['name'].capitalize(),
            "Type_2": pokemon_info['types'][1]['type']['name'].capitalize() if len(pokemon_info['types']) > 1 else None,
            "HP": pokemon_info['stats'][0]['base_stat'],
            "Attack": pokemon_info['stats'][1]['base_stat'],
            "Defense": pokemon_info['stats'][2]['base_stat'],
            "Special_Attack": pokemon_info['stats'][3]['base_stat'],
            "Special_Defense": pokemon_info['stats'][4]['base_stat'],
            "Speed": pokemon_info['stats'][5]['base_stat'],
            "Weight(lb)": pokemon_info['weight'],
            "Height(in)": pokemon_info['height'],
            "Generation": get_generation(pokemon_id)  # Add generation
        }
        pokemon_data_list.append(pokemon_data)

# Convert the data to a pandas DataFrame
pokemon_df = pd.DataFrame(pokemon_data_list)

# Convert weight and height to lb and inches
pokemon_df['Weight(lb)'] = ((pokemon_df['Weight(lb)'] * 0.1) * 2.2).round().astype(int)
pokemon_df['Height(in)'] = ((pokemon_df['Height(in)'] * 0.1) * 39.3701).round().astype(int)

# Database connection parameters
db_config = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": 5432
}

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("Connected to the database")

    # Create the pokemon_data table if not exists
    create_table_query = """
    CREATE TABLE IF NOT EXISTS PokemonData (
        id SERIAL PRIMARY KEY,
        pokemon_id INT UNIQUE,
        name VARCHAR(50),
        type_1 VARCHAR(50),
        type_2 VARCHAR(50),
        hp INT,
        attack INT,
        defense INT,
        special_attack INT,
        special_defense INT,
        speed INT,
        weight_lb INT,
        height_in INT,
        generation INT
    );
    """
    cursor.execute(create_table_query)
    conn.commit()

# Function to check if Pokémon exists
    def pokemon_exists(pokemon_id):
        cursor.execute("SELECT 1 FROM PokemonData WHERE pokemon_id = %s", (pokemon_id,))
        return cursor.fetchone() is not None
    
    # Prepare the data for insertion
    insert_query = """
    INSERT INTO PokemonData (
        pokemon_id, name, type_1, type_2, hp, attack, defense,
        special_attack, special_defense, speed, weight_lb, height_in, generation
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    # Insert only new Pokémon
    for pokemon_data in pokemon_data_list:
        pokemon_id = pokemon_data['ID']
        if not pokemon_exists(pokemon_id):
            cursor.execute(insert_query, (
                pokemon_data['ID'], pokemon_data['Name'], pokemon_data['Type_1'],
                pokemon_data['Type_2'], pokemon_data['HP'], pokemon_data['Attack'],
                pokemon_data['Defense'], pokemon_data['Special_Attack'],
                pokemon_data['Special_Defense'], pokemon_data['Speed'],
                pokemon_data['Weight(lb)'], pokemon_data['Height(in)'],
                pokemon_data['Generation']
            ))

    conn.commit()
    print("Data inserted successfully!")

    # Create a new table for each Pokémon type damage taken multipliers
    create_types_table_query = """
    CREATE TABLE IF NOT EXISTS PokemonTypeDamageTaken (
        pokemon_id INT PRIMARY KEY,
        normal  FLOAT,
        fire    FLOAT,
        water   FLOAT,
        electric FLOAT,
        grass   FLOAT,
        ice     FLOAT,
        fighting FLOAT,
        poison  FLOAT,
        ground  FLOAT,
        flying  FLOAT,
        psychic FLOAT,
        bug     FLOAT,
        rock    FLOAT,
        ghost   FLOAT,
        dragon  FLOAT,
        dark    FLOAT,
        steel   FLOAT
    );
    """
    cursor.execute(create_types_table_query)
    conn.commit()

# Create a new table for DamageTakenMultipliers
    create_DamageTakenMultipliers = """
    CREATE TABLE IF NOT EXISTS DamageTakenMultipliers (
        Defender VarChar(20),
        Attacker  VarChar(20),
        Multiplier    FLOAT
    );
    """
    cursor.execute(create_DamageTakenMultipliers)
    conn.commit()

   # Insert multipliers for each pokemon
    Multiplier = """
    INSERT INTO DamageTakenMultipliers (Defender, Attacker, Multiplier)
VALUES 
('Normal', 'Normal', 1.0),
('Normal', 'Fire', 1.0),
('Normal', 'Water', 1.0),
('Normal', 'Electric', 1.0),
('Normal', 'Grass', 1.0),
('Normal', 'Ice', 1.0),
('Normal', 'Fighting', 2.0),
('Normal', 'Poison', 1.0),
('Normal', 'Ground', 1.0),
('Normal', 'Flying', 1.0),
('Normal', 'Psychic', 1.0),
('Normal', 'Bug', 1.0),
('Normal', 'Rock', 1.0),
('Normal', 'Ghost', 0.0),
('Normal', 'Dragon', 1.0),
('Normal', 'Dark', 1.0),
('Normal', 'Steel', 1.0),
('Fire', 'Normal', 1.0),
('Fire', 'Fire', 0.5),
('Fire', 'Water', 2.0),
('Fire', 'Electric', 1.0),
('Fire', 'Grass', 0.5),
('Fire', 'Ice', 0.5),
('Fire', 'Fighting', 1.0),
('Fire', 'Poison', 1.0),
('Fire', 'Ground', 2.0),
('Fire', 'Flying', 1.0),
('Fire', 'Psychic', 1.0),
('Fire', 'Bug', 0.5),
('Fire', 'Rock', 2.0),
('Fire', 'Ghost', 1.0),
('Fire', 'Dragon', 1.0),
('Fire', 'Dark', 1.0),
('Fire', 'Steel', 0.5),
('Water', 'Normal', 1.0),
('Water', 'Fire', 0.5),
('Water', 'Water', 0.5),
('Water', 'Electric', 2.0),
('Water', 'Grass', 2.0),
('Water', 'Ice', 0.5),
('Water', 'Fighting', 1.0),
('Water', 'Poison', 1.0),
('Water', 'Ground', 1.0),
('Water', 'Flying', 1.0),
('Water', 'Psychic', 1.0),
('Water', 'Bug', 1.0),
('Water', 'Rock', 1.0),
('Water', 'Ghost', 1.0),
('Water', 'Dragon', 1.0),
('Water', 'Dark', 1.0),
('Water', 'Steel', 0.5),
('Electric', 'Normal', 1.0),
('Electric', 'Fire', 1.0),
('Electric', 'Water', 1.0),
('Electric', 'Electric', 0.5),
('Electric', 'Grass', 1.0),
('Electric', 'Ice', 1.0),
('Electric', 'Fighting', 1.0),
('Electric', 'Poison', 1.0),
('Electric', 'Ground', 2.0),
('Electric', 'Flying', 0.5),
('Electric', 'Psychic', 1.0),
('Electric', 'Bug', 1.0),
('Electric', 'Rock', 1.0),
('Electric', 'Ghost', 1.0),
('Electric', 'Dragon', 1.0),
('Electric', 'Dark', 1.0),
('Electric', 'Steel', 0.5),
('Grass', 'Normal', 1.0),
('Grass', 'Fire', 2.0),
('Grass', 'Water', 0.5),
('Grass', 'Electric', 0.5),
('Grass', 'Grass', 0.5),
('Grass', 'Ice', 2.0),
('Grass', 'Fighting', 1.0),
('Grass', 'Poison', 2.0),
('Grass', 'Ground', 0.5),
('Grass', 'Flying', 2.0),
('Grass', 'Psychic', 1.0),
('Grass', 'Bug', 2.0),
('Grass', 'Rock', 1.0),
('Grass', 'Ghost', 1.0),
('Grass', 'Dragon', 1.0),
('Grass', 'Dark', 1.0),
('Grass', 'Steel', 1.0),
('Ice', 'Normal', 1.0),
('Ice', 'Fire', 2.0),
('Ice', 'Water', 1.0),
('Ice', 'Electric', 2.0),
('Ice', 'Grass', 0.5),
('Ice', 'Ice', 0.5),
('Ice', 'Fighting', 2.0),
('Ice', 'Poison', 1.0),
('Ice', 'Ground', 1.0),
('Ice', 'Flying', 1.0),
('Ice', 'Psychic', 1.0),
('Ice', 'Bug', 1.0),
('Ice', 'Rock', 2.0),
('Ice', 'Ghost', 1.0),
('Ice', 'Dragon', 1.0),
('Ice', 'Dark', 1.0),
('Ice', 'Steel', 2.0),
('Fighting', 'Normal', 1.0),
('Fighting', 'Fire', 1.0),
('Fighting', 'Water', 1.0),
('Fighting', 'Electric', 1.0),
('Fighting', 'Grass', 1.0),
('Fighting', 'Ice', 1.0),
('Fighting', 'Fighting', 1.0),
('Fighting', 'Poison', 1.0),
('Fighting', 'Ground', 1.0),
('Fighting', 'Flying', 2.0),
('Fighting', 'Psychic', 2.0),
('Fighting', 'Bug', 0.5),
('Fighting', 'Rock', 0.5),
('Fighting', 'Ghost', 1.0),
('Fighting', 'Dragon', 1.0),
('Fighting', 'Dark', 0.5),
('Fighting', 'Steel', 1.0),
('Poison', 'Normal', 1.0),
('Poison', 'Fire', 1.0),
('Poison', 'Water', 1.0),
('Poison', 'Electric', 1.0),
('Poison', 'Grass', 0.5),
('Poison', 'Ice', 1.0),
('Poison', 'Fighting', 0.5),
('Poison', 'Poison', 0.5),
('Poison', 'Ground', 2.0),
('Poison', 'Flying', 1.0),
('Poison', 'Psychic', 2.0),
('Poison', 'Bug', 0.5),
('Poison', 'Rock', 1.0),
('Poison', 'Ghost', 1.0),
('Poison', 'Dragon', 1.0),
('Poison', 'Dark', 1.0),
('Poison', 'Steel', 1.0),
('Ground', 'Normal', 1.0),
('Ground', 'Fire', 1.0),
('Ground', 'Water', 1.0),
('Ground', 'Electric', 0.0),
('Ground', 'Grass', 2.0),
('Ground', 'Ice', 2.0),
('Ground', 'Fighting', 1.0),
('Ground', 'Poison', 0.5),
('Ground', 'Ground', 1.0),
('Ground', 'Flying', 2.0),
('Ground', 'Psychic', 1.0),
('Ground', 'Bug', 1.0),
('Ground', 'Rock', 0.5),
('Ground', 'Ghost', 1.0),
('Ground', 'Dragon', 1.0),
('Ground', 'Dark', 1.0),
('Ground', 'Steel', 1.0),
('Flying', 'Normal', 1.0),
('Flying', 'Fire', 1.0),
('Flying', 'Water', 1.0),
('Flying', 'Electric', 2.0),
('Flying', 'Grass', 0.5),
('Flying', 'Ice', 2.0),
('Flying', 'Fighting', 0.5),
('Flying', 'Poison', 1.0),
('Flying', 'Ground', 0.0),
('Flying', 'Flying', 1.0),
('Flying', 'Psychic', 1.0),
('Flying', 'Bug', 0.5),
('Flying', 'Rock', 2.0),
('Flying', 'Ghost', 1.0),
('Flying', 'Dragon', 1.0),
('Flying', 'Dark', 1.0),
('Flying', 'Steel', 1.0),
('Psychic', 'Normal', 1.0),
('Psychic', 'Fire', 1.0),
('Psychic', 'Water', 1.0),
('Psychic', 'Electric', 1.0),
('Psychic', 'Grass', 1.0),
('Psychic', 'Ice', 1.0),
('Psychic', 'Fighting', 0.5),
('Psychic', 'Poison', 1.0),
('Psychic', 'Ground', 1.0),
('Psychic', 'Flying', 1.0),
('Psychic', 'Psychic', 0.5),
('Psychic', 'Bug', 2.0),
('Psychic', 'Rock', 1.0),
('Psychic', 'Ghost', 2.0),
('Psychic', 'Dragon', 1.0),
('Psychic', 'Dark', 2.0),
('Psychic', 'Steel', 1.0),
('Bug', 'Normal', 1.0),
('Bug', 'Fire', 2.0),
('Bug', 'Water', 1.0),
('Bug', 'Electric', 1.0),
('Bug', 'Grass', 0.5),
('Bug', 'Ice', 1.0),
('Bug', 'Fighting', 0.5),
('Bug', 'Poison', 1.0),
('Bug', 'Ground', 0.5),
('Bug', 'Flying', 2.0),
('Bug', 'Psychic', 1.0),
('Bug', 'Bug', 1.0),
('Bug', 'Rock', 2.0),
('Bug', 'Ghost', 1.0),
('Bug', 'Dragon', 1.0),
('Bug', 'Dark', 1.0),
('Bug', 'Steel', 1.0),
('Rock', 'Normal', 0.5),
('Rock', 'Fire',0.5),
('Rock', 'Water', 2.0),
('Rock', 'Electric', 1.0),
('Rock', 'Grass', 2.0),
('Rock', 'Ice', 1.0),
('Rock', 'Fighting', 2.0),
('Rock', 'Poison', 0.5),
('Rock', 'Ground', 2.0),
('Rock', 'Flying', 0.5),
('Rock', 'Psychic', 1.0),
('Rock', 'Bug', 1.0),
('Rock', 'Rock', 1.0),
('Rock', 'Ghost', 1.0),
('Rock', 'Dragon', 1.0),
('Rock', 'Dark', 1.0),
('Rock', 'Steel', 2.0),
('Ghost', 'Normal', 0.0),
('Ghost', 'Fire', 1.0),
('Ghost', 'Water', 1.0),
('Ghost', 'Electric', 1.0),
('Ghost', 'Grass', 1.0),
('Ghost', 'Ice', 1.0),
('Ghost', 'Fighting', 0.0),
('Ghost', 'Poison', 0.5),
('Ghost', 'Ground', 1.0),
('Ghost', 'Flying', 1.0),
('Ghost', 'Psychic', 1.0),
('Ghost', 'Bug', 0.5),
('Ghost', 'Rock', 1.0),
('Ghost', 'Ghost', 2.0),
('Ghost', 'Dragon', 1.0),
('Ghost', 'Dark', 2.0),
('Ghost', 'Steel', 1.0),
('Dragon', 'Normal', 1.0),
('Dragon', 'Fire', 0.5),
('Dragon', 'Water', 0.5),
('Dragon', 'Electric', 0.5),
('Dragon', 'Grass', 0.5),
('Dragon', 'Ice', 2.0),
('Dragon', 'Fighting', 1.0),
('Dragon', 'Poison', 1.0),
('Dragon', 'Ground', 1.0),
('Dragon', 'Flying', 1.0),
('Dragon', 'Psychic', 1.0),
('Dragon', 'Bug', 1.0),
('Dragon', 'Rock', 1.0),
('Dragon', 'Ghost', 1.0),
('Dragon', 'Dragon', 2.0),
('Dragon', 'Dark', 1.0),
('Dragon', 'Steel', 1.0),
('Dark', 'Normal', 1.0),
('Dark', 'Fire', 1.0),
('Dark', 'Water', 1.0),
('Dark', 'Electric', 1.0),
('Dark', 'Grass', 1.0),
('Dark', 'Ice', 1.0),
('Dark', 'Fighting', 2.0),
('Dark', 'Poison', 1.0),
('Dark', 'Ground', 1.0),
('Dark', 'Flying', 1.0),
('Dark', 'Psychic', 0.0),
('Dark', 'Bug', 2.0),
('Dark', 'Rock', 1.0),
('Dark', 'Ghost', 0.5),
('Dark', 'Dragon', 1.0),
('Dark', 'Dark', 0.5),
('Dark', 'Steel', 1.0),
('Steel', 'Normal', 0.5),
('Steel', 'Fire', 2.0),
('Steel', 'Water', 1.0),
('Steel', 'Electric', 1.0),
('Steel', 'Grass', 0.5),
('Steel', 'Ice', 0.5),
('Steel', 'Fighting', 2.0),
('Steel', 'Poison', 0.0),
('Steel', 'Ground', 2.0),
('Steel', 'Flying', 0.5),
('Steel', 'Psychic', 0.5),
('Steel', 'Bug', 0.5),
('Steel', 'Rock', 0.5),
('Steel', 'Ghost', 0.5),
('Steel', 'Dragon', 0.5),
('Steel', 'Dark', 0.5),
('Steel', 'Steel', 0.5);
    """
    try:
        cursor.execute(Multiplier)
        conn.commit()
        print("Multipliers added successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Insert pokemon multipliers
    insert_Multipliers = """
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

    try:
        cursor.execute(insert_Multipliers)
        conn.commit()
        print("good ")
    except Exception as e:
        print(f"An error occurred: {e}")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()