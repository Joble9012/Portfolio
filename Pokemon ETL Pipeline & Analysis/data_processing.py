import pandas as pd

def get_generation(pokemon_id):
    """
    Determine the generation of a Pokémon based on its ID.
    Returns the generation number or None if ID is invalid.
    """
    generation_ranges = {
        1: range(1, 152),
        2: range(152, 252),
        3: range(252, 387),
        4: range(387, 494),
        5: range(494, 650),
        6: range(650, 722),
        7: range(722, 810),
        8: range(810, 899)
    }

    for gen, gen_range in generation_ranges.items():
        if pokemon_id in gen_range:
            return gen
    return None

def process_pokemon_data(all_pokemon_names, get_pokemon_info):
    """
    Process Pokémon data for a list of Pokémon names.
    Fetches detailed information for each Pokémon and organizes the data into a list of dictionaries.
    """
    pokemon_data_list = []

    # Iterate over the first 10 Pokémon names
    for pokemon_name in all_pokemon_names[:649]:
        pokemon_info = get_pokemon_info(pokemon_name)
        
        if pokemon_info:
            # Extract necessary data from the Pokémon information
            pokemon_data = {
                "ID": pokemon_info['id'],
                "Name": pokemon_info['name'].capitalize(),
                "Type_1": pokemon_info['types'][0]['type']['name'].capitalize(),
                "Type_2": pokemon_info['types'][1]['type']['name'].capitalize() if len(pokemon_info['types']) > 1 else None,
                "HP": pokemon_info['stats'][0]['base_stat'],
                "Attack": pokemon_info['stats'][1]['base_stat'],
                "Defense": pokemon_info['stats'][2]['base_stat'],
                "Special_Attack": pokemon_info['stats'][3]['base_stat'],
                "Special_Defense": pokemon_info['stats'][4]['base_stat'],
                "Speed": pokemon_info['stats'][5]['base_stat'],
                "Weight(lb)": round(pokemon_info['weight'] * 0.1 * 2.2),  # Convert weight to pounds
                "Height(in)": round(pokemon_info['height'] * 0.1 * 39.3701),  # Convert height to inches
                "Generation": get_generation(pokemon_info['id'])
            }
            pokemon_data_list.append(pokemon_data)

    return pokemon_data_list
