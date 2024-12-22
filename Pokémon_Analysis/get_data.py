import requests
import pandas as pd

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

# Main logic to collect Pokémon data
all_pokemon_names = get_all_pokemon_names()
pokemon_data_list = []

for pokemon_name in all_pokemon_names[:10]:  # Limit for testing. Set to 649
    pokemon_info = get_pokemon_info(pokemon_name)
    if pokemon_info:
        pokemon_data = {
            "Name": pokemon_info['name'].capitalize(),
            "ID": pokemon_info['id'],
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
        }
        pokemon_data_list.append(pokemon_data)

# Convert the data to a pandas DataFrame
pokemon_df = pd.DataFrame(pokemon_data_list)
# Function to determine generation based on ID
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
    else:
        return None  # Optional for IDs outside defined generations

# Add a Generation column to the DataFrame
pokemon_df['Generation'] = pokemon_df['ID'].apply(get_generation)

# Convert Weight and Height to lb and feet

pokemon_df['Weight(lb)'] = ((pokemon_df['Weight(lb)'] * .1) *2.2).round().astype(int)

pokemon_df['Height(in)'] = ((pokemon_df['Height(in)'] * .1) *39.3701).round().astype(int)

# Display the DataFrame
print(pokemon_df)




import psycopg2
from psycopg2 import sql

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

    # Create the Pokémon table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS pokemon (
        id SERIAL PRIMARY KEY,
        pokemon_id INT,
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

    # Prepare the data for insertion
    insert_query = """
    INSERT INTO pokemon (
        pokemon_id, name, type_1, type_2, hp, attack, defense,
        special_attack, special_defense, speed, weight_lb, height_in, generation
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    data_to_insert = pokemon_df.to_records(index=False).tolist()

    # Execute the insert query
    cursor.executemany(insert_query, data_to_insert)
    conn.commit()
    print("Data inserted successfully!")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()

