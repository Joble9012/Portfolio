import psycopg2
base_url = "https://pokeapi.co/api/v2/"
import requests

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

def insert_pokemon_data(cursor, pokemon_data_list):
    insert_query = """
    INSERT INTO PokemonData (
        pokemon_id, name, type_1, type_2, hp, attack, defense,
        special_attack, special_defense, speed, weight_lb, height_in, generation
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (pokemon_id) DO NOTHING;
    """
    
    try:
        pokemon_data_tuples = [
            (
                pokemon['ID'], pokemon['Name'], pokemon['Type_1'],
                pokemon['Type_2'], pokemon['HP'], pokemon['Attack'],
                pokemon['Defense'], pokemon['Special_Attack'],
                pokemon['Special_Defense'], pokemon['Speed'],
                pokemon['Weight(lb)'], pokemon['Height(in)'],
                pokemon['Generation']
            ) for pokemon in pokemon_data_list
        ]
        
        cursor.executemany(insert_query, pokemon_data_tuples)
        print("Pokemon data inserted successfully.")
        
    except Exception as e:
        print(f"Error inserting data: {e}")
