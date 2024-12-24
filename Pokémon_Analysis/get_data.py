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

for pokemon_name in all_pokemon_names[:3]:  # Limit for testing
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
    # Insert_Id_to_type = """
    # INSERT INTO pokemon_types (pokemon_id)
    # SELECT pokemon_id
    # FROM pokemon
    # WHERE NOT EXISTS (
    #     SELECT 1
    #     FROM pokemon_types
    #     WHERE pokemon_types.pokemon_id = pokemon.pokemon_id
    # );
    # """

    # try:
    #     cursor.execute(Insert_Id_to_type)
    #     conn.commit()
    #     print("New IDs inserted into pokemon_types successfully.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")


# Create a new table for types e multipliers
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
('Water', 'Water', 1.0),
('Water', 'Electric', 2.0),
('Water', 'Grass', 2.0),
('Water', 'Ice', 1.0),
('Water', 'Fighting', 1.0),
('Water', 'Poison', 1.0),
('Water', 'Ground', 1.0),
('Water', 'Flying', 1.0),
('Water', 'Psychic', 1.0),
('Water', 'Bug', 1.0),
('Water', 'Rock', 0.5),
('Water', 'Ghost', 1.0),
('Water', 'Dragon', 1.0),
('Water', 'Dark', 1.0),
('Water', 'Steel', 1.0),
('Electric', 'Normal', 1.0),
('Electric', 'Fire', 1.0),
('Electric', 'Water', 1.0),
('Electric', 'Electric', 0.5),
('Electric', 'Grass', 2.0),
('Electric', 'Ice', 1.0),
('Electric', 'Fighting', 1.0),
('Electric', 'Poison', 1.0),
('Electric', 'Ground', 2.0),
('Electric', 'Flying', 1.0),
('Electric', 'Psychic', 1.0),
('Electric', 'Bug', 1.0),
('Electric', 'Rock', 1.0),
('Electric', 'Ghost', 1.0),
('Electric', 'Dragon', 1.0),
('Electric', 'Dark', 1.0),
('Electric', 'Steel', 1.0),
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
('Ice', 'Water', 2.0),
('Ice', 'Electric', 2.0),
('Ice', 'Grass', 0.5),
('Ice', 'Ice', 1.0),
('Ice', 'Fighting', 2.0),
('Ice', 'Poison', 1.0),
('Ice', 'Ground', 0.5),
('Ice', 'Flying', 1.0),
('Ice', 'Psychic', 1.0),
('Ice', 'Bug', 1.0),
('Ice', 'Rock', 1.0),
('Ice', 'Ghost', 1.0),
('Ice', 'Dragon', 0.5),
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
('Fighting', 'Bug', 1.0),
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
('Ground', 'Poison', 1.0),
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
('Flying', 'Grass', 1.0),
('Flying', 'Ice', 1.0),
('Flying', 'Fighting', 1.0),
('Flying', 'Poison', 1.0),
('Flying', 'Ground', 1.0),
('Flying', 'Flying', 1.0),
('Flying', 'Psychic', 1.0),
('Flying', 'Bug', 1.0),
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
('Psychic', 'Fighting', 1.0),
('Psychic', 'Poison', 1.0),
('Psychic', 'Ground', 1.0),
('Psychic', 'Flying', 1.0),
('Psychic', 'Psychic', 1.0),
('Psychic', 'Bug', 2.0),
('Psychic', 'Rock', 1.0),
('Psychic', 'Ghost', 1.0),
('Psychic', 'Dragon', 1.0),
('Psychic', 'Dark', 2.0),
('Psychic', 'Steel', 1.0),
('Bug', 'Normal', 1.0),
('Bug', 'Fire', 2.0),
('Bug', 'Water', 1.0),
('Bug', 'Electric', 1.0),
('Bug', 'Grass', 1.0),
('Bug', 'Ice', 1.0),
('Bug', 'Fighting', 1.0),
('Bug', 'Poison', 1.0),
('Bug', 'Ground', 1.0),
('Bug', 'Flying', 2.0),
('Bug', 'Psychic', 1.0),
('Bug', 'Bug', 0.5),
('Bug', 'Rock', 1.0),
('Bug', 'Ghost', 1.0),
('Bug', 'Dragon', 1.0),
('Bug', 'Dark', 1.0),
('Bug', 'Steel', 2.0),
('Rock', 'Normal', 1.0),
('Rock', 'Fire', 1.0),
('Rock', 'Water', 1.0),
('Rock', 'Electric', 1.0),
('Rock', 'Grass', 1.0),
('Rock', 'Ice', 1.0),
('Rock', 'Fighting', 2.0),
('Rock', 'Poison', 1.0),
('Rock', 'Ground', 2.0),
('Rock', 'Flying', 1.0),
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
('Ghost', 'Fighting', 1.0),
('Ghost', 'Poison', 1.0),
('Ghost', 'Ground', 1.0),
('Ghost', 'Flying', 1.0),
('Ghost', 'Psychic', 1.0),
('Ghost', 'Bug', 1.0),
('Ghost', 'Rock', 1.0),
('Ghost', 'Ghost', 2.0),
('Ghost', 'Dragon', 1.0),
('Ghost', 'Dark', 1.0),
('Ghost', 'Steel', 1.0),
('Dragon', 'Normal', 1.0),
('Dragon', 'Fire', 1.0),
('Dragon', 'Water', 1.0),
('Dragon', 'Electric', 1.0),
('Dragon', 'Grass', 1.0),
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
('Dark', 'Psychic', 1.0),
('Dark', 'Bug', 1.0),
('Dark', 'Rock', 1.0),
('Dark', 'Ghost', 1.0),
('Dark', 'Dragon', 1.0),
('Dark', 'Dark', 0.5),
('Dark', 'Steel', 1.0),
('Steel', 'Normal', 1.0),
('Steel', 'Fire', 2.0),
('Steel', 'Water', 2.0),
('Steel', 'Electric', 2.0),
('Steel', 'Grass', 1.0),
('Steel', 'Ice', 1.0),
('Steel', 'Fighting', 1.0),
('Steel', 'Poison', 1.0),
('Steel', 'Ground', 1.0),
('Steel', 'Flying', 1.0),
('Steel', 'Psychic', 1.0),
('Steel', 'Bug', 1.0),
('Steel', 'Rock', 1.0),
('Steel', 'Ghost', 1.0),
('Steel', 'Dragon', 1.0),
('Steel', 'Dark', 1.0),
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
WITH type_multipliers AS (
    -- Get damage multipliers for both type_1 and type_2
    SELECT
        p.pokemon_id,
        -- Join the DamageTakenMultipliers table for each damage type
        COALESCE(dm1.Multiplier, 1) AS normal,
        COALESCE(dm2.Multiplier, 1) AS fire,
        COALESCE(dm3.Multiplier, 1) AS water,
        COALESCE(dm4.Multiplier, 1) AS electric,
        COALESCE(dm5.Multiplier, 1) AS grass,
        COALESCE(dm6.Multiplier, 1) AS ice,
        COALESCE(dm7.Multiplier, 1) AS fighting,
        COALESCE(dm8.Multiplier, 1) AS poison,
        COALESCE(dm9.Multiplier, 1) AS ground,
        COALESCE(dm10.Multiplier, 1) AS flying,
        COALESCE(dm11.Multiplier, 1) AS psychic,
        COALESCE(dm12.Multiplier, 1) AS bug,
        COALESCE(dm13.Multiplier, 1) AS rock,
        COALESCE(dm14.Multiplier, 1) AS ghost,
        COALESCE(dm15.Multiplier, 1) AS dragon,
        COALESCE(dm16.Multiplier, 1) AS dark,
        COALESCE(dm17.Multiplier, 1) AS steel
    FROM pokemon p
    LEFT JOIN DamageTakenMultipliers dm1 
        ON p.type_1 = dm1.Defender AND dm1.Attacker = 'Normal'
    LEFT JOIN DamageTakenMultipliers dm2 
        ON p.type_1 = dm2.Defender AND dm2.Attacker = 'Fire'
    LEFT JOIN DamageTakenMultipliers dm3 
        ON p.type_1 = dm3.Defender AND dm3.Attacker = 'Water'
    LEFT JOIN DamageTakenMultipliers dm4 
        ON p.type_1 = dm4.Defender AND dm4.Attacker = 'Electric'
    LEFT JOIN DamageTakenMultipliers dm5 
        ON p.type_1 = dm5.Defender AND dm5.Attacker = 'Grass'
    LEFT JOIN DamageTakenMultipliers dm6 
        ON p.type_1 = dm6.Defender AND dm6.Attacker = 'Ice'
    LEFT JOIN DamageTakenMultipliers dm7 
        ON p.type_1 = dm7.Defender AND dm7.Attacker = 'Fighting'
    LEFT JOIN DamageTakenMultipliers dm8 
        ON p.type_1 = dm8.Defender AND dm8.Attacker = 'Poison'
    LEFT JOIN DamageTakenMultipliers dm9 
        ON p.type_1 = dm9.Defender AND dm9.Attacker = 'Ground'
    LEFT JOIN DamageTakenMultipliers dm10 
        ON p.type_1 = dm10.Defender AND dm10.Attacker = 'Flying'
    LEFT JOIN DamageTakenMultipliers dm11 
        ON p.type_1 = dm11.Defender AND dm11.Attacker = 'Psychic'
    LEFT JOIN DamageTakenMultipliers dm12 
        ON p.type_1 = dm12.Defender AND dm12.Attacker = 'Bug'
    LEFT JOIN DamageTakenMultipliers dm13 
        ON p.type_1 = dm13.Defender AND dm13.Attacker = 'Rock'
    LEFT JOIN DamageTakenMultipliers dm14 
        ON p.type_1 = dm14.Defender AND dm14.Attacker = 'Ghost'
    LEFT JOIN DamageTakenMultipliers dm15 
        ON p.type_1 = dm15.Defender AND dm15.Attacker = 'Dragon'
    LEFT JOIN DamageTakenMultipliers dm16 
        ON p.type_1 = dm16.Defender AND dm16.Attacker = 'Dark'
    LEFT JOIN DamageTakenMultipliers dm17 
        ON p.type_1 = dm17.Defender AND dm17.Attacker = 'Steel'
    LEFT JOIN DamageTakenMultipliers dm18
        ON p.type_2 = dm18.Defender AND dm18.Attacker = 'Normal'
    LEFT JOIN DamageTakenMultipliers dm19 
        ON p.type_2 = dm19.Defender AND dm19.Attacker = 'Fire'
    LEFT JOIN DamageTakenMultipliers dm20 
        ON p.type_2 = dm20.Defender AND dm20.Attacker = 'Water'
    LEFT JOIN DamageTakenMultipliers dm21 
        ON p.type_2 = dm21.Defender AND dm21.Attacker = 'Electric'
    LEFT JOIN DamageTakenMultipliers dm22 
        ON p.type_2 = dm22.Defender AND dm22.Attacker = 'Grass'
    LEFT JOIN DamageTakenMultipliers dm23 
        ON p.type_2 = dm23.Defender AND dm23.Attacker = 'Ice'
    LEFT JOIN DamageTakenMultipliers dm24 
        ON p.type_2 = dm24.Defender AND dm24.Attacker = 'Fighting'
    LEFT JOIN DamageTakenMultipliers dm25 
        ON p.type_2 = dm25.Defender AND dm25.Attacker = 'Poison'
    LEFT JOIN DamageTakenMultipliers dm26 
        ON p.type_2 = dm26.Defender AND dm26.Attacker = 'Ground'
    LEFT JOIN DamageTakenMultipliers dm27 
        ON p.type_2 = dm27.Defender AND dm27.Attacker = 'Flying'
    LEFT JOIN DamageTakenMultipliers dm28 
        ON p.type_2 = dm28.Defender AND dm28.Attacker = 'Psychic'
    LEFT JOIN DamageTakenMultipliers dm29 
        ON p.type_2 = dm29.Defender AND dm29.Attacker = 'Bug'
    LEFT JOIN DamageTakenMultipliers dm30 
        ON p.type_2 = dm30.Defender AND dm30.Attacker = 'Rock'
    LEFT JOIN DamageTakenMultipliers dm31 
        ON p.type_2 = dm31.Defender AND dm31.Attacker = 'Ghost'
    LEFT JOIN DamageTakenMultipliers dm32 
        ON p.type_2 = dm32.Defender AND dm32.Attacker = 'Dragon'
    LEFT JOIN DamageTakenMultipliers dm33 
        ON p.type_2 = dm33.Defender AND dm33.Attacker = 'Dark'
    LEFT JOIN DamageTakenMultipliers dm34 
        ON p.type_2 = dm34.Defender AND dm34.Attacker = 'Steel'
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
FROM type_multipliers
WHERE NOT EXISTS (
        SELECT 1
        FROM pokemon_types
        WHERE pokemon_types.pokemon_id = type_multipliers.pokemon_id);
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
