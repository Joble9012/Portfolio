import requests
import pandas as pd
import psycopg2

base_url = "https://pokeapi.co/api/v2/"

# Function to get all Pokémon names
def get_all_pokemon_names():
    url = f"{base_url}pokemon"
    all_pokemon = []
    
    while url:  # Continue until there are no more pages
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            # Add the names of Pokémon from the current page
            all_pokemon.extend(p['name'] for p in data['results'])
            # Update the URL to the next page, or None if there are no more pages
            url = data['next']
        else:
            print(f"Failed to retrieve data {response.status_code}")
            break

    return all_pokemon

# Function to get detailed information about a single Pokémon
def get_pokemon_info(name):
    url = f"{base_url}pokemon/{name}"
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        print(f"Failed to retrieve data {response.status_code}")
        return None

# Function to determine the generation based on the Pokémon's ID
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

# Main logic to collect Pokémon data
all_pokemon_names = get_all_pokemon_names()
pokemon_data_list = []

for pokemon_name in all_pokemon_names[100:105]:  # Limit for testing
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

# Convert Weight and Height to lb and inches
pokemon_df['Weight(lb)'] = ((pokemon_df['Weight(lb)'] * 0.1) * 2.2).round().astype(int)
pokemon_df['Height(in)'] = ((pokemon_df['Height(in)'] * 0.1) * 39.3701).round().astype(int)

# Reorder columns to match the database table's structure
pokemon_df = pokemon_df[
    ["ID", "Name", "Type_1", "Type_2", "HP", "Attack", "Defense",
     "Special_Attack", "Special_Defense", "Speed", "Weight(lb)", "Height(in)", "Generation"]
]

damage_taken_multipliers = {
    "Normal": {"Normal": 1.0, "Fire": 1.0, "Water": 1.0, "Electric": 1.0, "Grass": 1.0, "Ice": 1.0, "Fighting": 2.0, "Poison": 1.0, "Ground": 1.0, "Flying": 1.0, "Psychic": 1.0, "Bug": 1.0, "Rock": 1.0, "Ghost": 0, "Dragon": 1.0, "Dark": 1.0, "Steel": 1.0},
    "Fire": {"Normal": 1.0, "Fire": 0.5, "Water": 2.0, "Electric": 1.0, "Grass": 0.5, "Ice": 0.5, "Fighting": 1.0, "Poison": 1.0, "Ground": 2.0, "Flying": 1.0, "Psychic": 1.0, "Bug": 0.5, "Rock": 2.0, "Ghost": 1.0, "Dragon": 1.0, "Dark": 1.0, "Steel": 0.5},
    "Water": {"Normal": 1.0, "Fire": 0.5, "Water": 1.0, "Electric": 2.0, "Grass": 2.0, "Ice": 1.0, "Fighting": 1.0, "Poison": 1.0, "Ground": 1.0, "Flying": 1.0, "Psychic": 1.0, "Bug": 1.0, "Rock": 0.5, "Ghost": 1.0, "Dragon": 1.0, "Dark": 1.0, "Steel": 1.0},
    "Electric": {"Normal": 1.0, "Fire": 1.0, "Water": 1.0, "Electric": 0.5, "Grass": 2.0, "Ice": 1.0, "Fighting": 1.0, "Poison": 1.0, "Ground": 2.0, "Flying": 1.0, "Psychic": 1.0, "Bug": 1.0, "Rock": 1.0, "Ghost": 1.0, "Dragon": 1.0, "Dark": 1.0, "Steel": 1.0},
    "Grass": {"Normal": 1.0, "Fire": 2.0, "Water": 0.5, "Electric": 1.0, "Grass": 1.0, "Ice": 2.0, "Fighting": 1.0, "Poison": 2.0, "Ground": 0.5, "Flying": 2.0, "Psychic": 1.0, "Bug": 2.0, "Rock": 1.0, "Ghost": 1.0, "Dragon": 1.0, "Dark": 1.0, "Steel": 1.0},
    "Ice": {"Normal": 1.0, "Fire": 2.0, "Water": 2.0, "Electric": 2.0, "Grass": 0.5, "Ice": 1.0, "Fighting": 2.0, "Poison": 1.0, "Ground": 0.5, "Flying": 1.0, "Psychic": 1.0, "Bug": 1.0, "Rock": 1.0, "Ghost": 1.0, "Dragon": 0.5, "Dark": 1.0, "Steel": 2.0},
    "Fighting": {"Normal": 1.0, "Fire": 1.0, "Water": 1.0, "Electric": 1.0, "Grass": 1.0, "Ice": 1.0, "Fighting": 1.0, "Poison": 1.0, "Ground": 1.0, "Flying": 2.0, "Psychic": 2.0, "Bug": 1.0, "Rock": 0.5, "Ghost": 1.0, "Dragon": 1.0, "Dark": 0.5, "Steel": 1.0},
    "Poison": {"Normal": 1.0, "Fire": 1.0, "Water": 1.0, "Electric": 1.0, "Grass": 0.5, "Ice": 1.0, "Fighting": 1.0, "Poison": 0.5, "Ground": 2.0, "Flying": 1.0, "Psychic": 1.0, "Bug": 1.0, "Rock": 1.0, "Ghost": 1.0, "Dragon": 1.0, "Dark": 1.0, "Steel": 1.0},
    "Ground": {"Normal": 1.0, "Fire": 1.0, "Water": 1.0, "Electric": 0.0, "Grass": 2.0, "Ice": 2.0, "Fighting": 1.0, "Poison": 1.0, "Ground": 1.0, "Flying": 2.0, "Psychic": 1.0, "Bug": 1.0, "Rock": 0.5, "Ghost": 1.0, "Dragon": 1.0, "Dark": 1.0, "Steel": 1.0},
    "Flying": {"Normal": 1.0, "Fire": 1.0, "Water": 1.0, "Electric": 2.0, "Grass": 1.0, "Ice": 1.0, "Fighting": 1.0, "Poison": 1.0, "Ground": 1.0, "Flying": 1.0, "Psychic": 1.0, "Bug": 1.0, "Rock": 2.0, "Ghost": 1.0, "Dragon": 1.0, "Dark": 1.0, "Steel": 1.0},
    "Psychic": {"Normal": 1.0, "Fire": 1.0, "Water": 1.0, "Electric": 1.0, "Grass": 1.0, "Ice": 1.0, "Fighting": 1.0, "Poison": 1.0, "Ground": 1.0, "Flying": 1.0, "Psychic": 1.0, "Bug": 2.0, "Rock": 1.0, "Ghost": 1.0, "Dragon": 1.0, "Dark": 2.0, "Steel": 1.0},
    "Bug": {"Normal": 1.0, "Fire": 2.0, "Water": 1.0, "Electric": 1.0, "Grass": 1.0, "Ice": 1.0, "Fighting": 1.0, "Poison": 1.0, "Ground": 1.0, "Flying": 2.0, "Psychic": 1.0, "Bug": 0.5, "Rock": 1.0, "Ghost": 1.0, "Dragon": 1.0, "Dark": 1.0, "Steel": 2.0},
    "Rock": {"Normal": 1.0, "Fire": 1.0, "Water": 1.0, "Electric": 1.0, "Grass": 1.0, "Ice": 1.0, "Fighting": 2.0, "Poison": 1.0, "Ground": 2.0, "Flying": 1.0, "Psychic": 1.0, "Bug": 1.0, "Rock": 1.0, "Ghost": 1.0, "Dragon": 1.0, "Dark": 1.0, "Steel": 2.0},
    "Ghost": {"Normal": 0.0, "Fire": 1.0, "Water": 1.0, "Electric": 1.0, "Grass": 1.0, "Ice": 1.0, "Fighting": 1.0, "Poison": 1.0, "Ground": 1.0, "Flying": 1.0, "Psychic": 1.0, "Bug": 1.0, "Rock": 1.0, "Ghost": 2.0, "Dragon": 1.0, "Dark": 1.0, "Steel": 1.0},
    "Dragon": {"Normal": 1.0, "Fire": 1.0, "Water": 1.0, "Electric": 1.0, "Grass": 1.0, "Ice": 2.0, "Fighting": 1.0, "Poison": 1.0, "Ground": 1.0, "Flying": 1.0, "Psychic": 1.0, "Bug": 1.0, "Rock": 1.0, "Ghost": 1.0, "Dragon": 2.0, "Dark": 1.0, "Steel": 1.0},
    "Dark": {"Normal": 1.0, "Fire": 1.0, "Water": 1.0, "Electric": 1.0, "Grass": 1.0, "Ice": 1.0, "Fighting": 2.0, "Poison": 1.0, "Ground": 1.0, "Flying": 1.0, "Psychic": 1.0, "Bug": 1.0, "Rock": 1.0, "Ghost": 1.0, "Dragon": 1.0, "Dark": 0.5, "Steel": 1.0},
    "Steel": {"Normal": 1.0, "Fire": 2.0, "Water": 2.0, "Electric": 2.0, "Grass": 1.0, "Ice": 1.0, "Fighting": 1.0, "Poison": 1.0, "Ground": 1.0, "Flying": 1.0, "Psychic": 1.0, "Bug": 1.0, "Rock": 1.0, "Ghost": 1.0, "Dragon": 1.0, "Dark": 1.0, "Steel": 0.5}
}


print(pokemon_df)





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

    # Create the Pokémon table if not exists
    create_table_query = """
    CREATE TABLE IF NOT EXISTS pokemon (
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
        cursor.execute("SELECT 1 FROM pokemon WHERE pokemon_id = %s", (pokemon_id,))
        return cursor.fetchone() is not None

    # Prepare the data for insertion
    insert_query = """
    INSERT INTO pokemon (
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

    # Create a new table for Pokémon types and damage multipliers
    create_types_table_query = """
    CREATE TABLE IF NOT EXISTS pokemon_types (
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

    # Insert only new IDs into the pokemon_types table
    Insert_Id_to_type = """
    INSERT INTO pokemon_types (pokemon_id)
    SELECT pokemon_id
    FROM pokemon
    WHERE NOT EXISTS (
        SELECT 1
        FROM pokemon_types
        WHERE pokemon_types.pokemon_id = pokemon.pokemon_id
    );
    """

    try:
        cursor.execute(Insert_Id_to_type)
        conn.commit()
        print("New IDs inserted into pokemon_types successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Insert multipliers for each pokemon
    Insert_multi = """
    WITH type_multipliers AS (
        -- Get damage multipliers for both type_1 and type_2
        SELECT
            p.pokemon_id,
            dm1.type_1 AS type_1,
            dm2.type_1 AS type_2,
            -- Multiply the multipliers for type_1 and type_2 against each damage type
            (dm1.Normal * dm2.Normal) AS normal,
            (dm1.Fire * dm2.Fire) AS fire,
            (dm1.Water * dm2.Water) AS water,
            (dm1.Electric * dm2.Electric) AS electric,
            (dm1.Grass * dm2.Grass) AS grass,
            (dm1.Ice * dm2.Ice) AS ice,
            (dm1.Fighting * dm2.Fighting) AS fighting,
            (dm1.Poison * dm2.Poison) AS poison,
            (dm1.Ground * dm2.Ground) AS ground,
            (dm1.Flying * dm2.Flying) AS flying,
            (dm1.Psychic * dm2.Psychic) AS psychic,
            (dm1.Bug * dm2.Bug) AS bug,
            (dm1.Rock * dm2.Rock) AS rock,
            (dm1.Ghost * dm2.Ghost) AS ghost,
            (dm1.Dragon * dm2.Dragon) AS dragon,
            (dm1.Dark * dm2.Dark) AS dark,
            (dm1.Steel * dm2.Steel) AS steel
        FROM pokemon p
        -- Get the damage multipliers for type_1
        INNER JOIN damage_taken_multipliers dm1 ON p.type_1 = dm1.type_1
        -- Get the damage multipliers for type_2
        LEFT JOIN damage_taken_multipliers dm2 ON p.type_2 = dm2.type_1
    )
    -- Insert the results into the pokemon_types table
    INSERT INTO pokemon_types (
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
    SELECT
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
    FROM type_multipliers;
    """

    try:
        cursor.execute(Insert_multi)
        conn.commit()
        print("Multipliers added successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
