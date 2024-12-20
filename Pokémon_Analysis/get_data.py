import requests

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

# Main logic
all_pokemon_names = get_all_pokemon_names()

# Retrieve and print information for each Pokémon (you can limit this for testing)
for pokemon_name in all_pokemon_names[:10]:  # Adjust [:10] to limit the output
    pokemon_info = get_pokemon_info(pokemon_name)
    if pokemon_info:
        print(f"Name: {pokemon_info['name'].capitalize()}")
        print(f"Id: {pokemon_info['id']}")
        print(f"HP: {pokemon_info['stats'][0]['base_stat']}")
        print(f"Attack: {pokemon_info['stats'][1]['base_stat']}")
        print(f"Defense: {pokemon_info['stats'][2]['base_stat']}")
        print(f"special-attack: {pokemon_info['stats'][3]['base_stat']}")
        print(f"special-defense: {pokemon_info['stats'][4]['base_stat']}")
        print(f"speed: {pokemon_info['stats'][5]['base_stat']}")
        print(f"Type 1: {pokemon_info['types'][0]['type']['name']}")
        
        # Check if there's a second type, if not, print "Type 2: Is null"
        if len(pokemon_info['types']) > 1:
            print(f"Type 2: {pokemon_info['types'][1]['type']['name']}")
        else:
            print("Type 2: Is null")
        print("-" * 20)
