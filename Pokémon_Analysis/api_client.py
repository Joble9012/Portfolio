import requests

# Base URL for API
BASE_URL = "https://pokeapi.co/api/v2/"

def get_all_pokemon_names():
    """
    Fetch all Pokémon names from the API, handling pagination.
    Returns a list of Pokémon names.
    """
    url = f"{BASE_URL}pokemon"
    all_pokemon = []

    while url:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            all_pokemon.extend(pokemon['name'] for pokemon in data['results'])
            url = data['next']  # Update the URL for the next page
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            break

    return all_pokemon

def get_pokemon_info(name):
    """
    Get detailed information about a specific Pokémon.
    Returns the Pokémon data if successful, or None if failed.
    """
    url = f"{BASE_URL}pokemon/{name}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

def insert_pokemon_data(cursor, pokemon_data_list):
    """
    Insert Pokémon data into the database.
    Uses executemany for bulk insertion to improve performance.
    """
    insert_query = """
    INSERT INTO PokemonData (
        pokemon_id, name, type_1, type_2, hp, attack, defense,
        special_attack, special_defense, speed, weight_lb, height_in, generation
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (pokemon_id) DO NOTHING;
    """

    try:
        # Prepare data as a list of tuples for bulk insertion
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

        # Execute the bulk insert
        cursor.executemany(insert_query, pokemon_data_tuples)
        print("Pokemon data inserted successfully.")

    except Exception as e:
        print(f"Error inserting data: {e}")
        # Optionally, insert records individually if bulk insertion fails
        for pokemon_data in pokemon_data_list:
            try:
                cursor.execute(insert_query, (
                    pokemon_data['ID'], pokemon_data['Name'], pokemon_data['Type_1'],
                    pokemon_data['Type_2'], pokemon_data['HP'], pokemon_data['Attack'],
                    pokemon_data['Defense'], pokemon_data['Special_Attack'],
                    pokemon_data['Special_Defense'], pokemon_data['Speed'],
                    pokemon_data['Weight(lb)'], pokemon_data['Height(in)'],
                    pokemon_data['Generation']
                ))
            except Exception as inner_e:
                print(f"Error inserting individual record {pokemon_data['ID']}: {inner_e}")
