import pandas as pd
from api_client import insert_pokemon_data, get_pokemon_info, get_all_pokemon_names
from data_processing import process_pokemon_data
from database_manager import connect_to_db, create_tables, create_damage_taken_multipliers_table
from create_damage_multipliers import create_damage_multipliers

def main():
    db_config = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "password",
        "host": "localhost",
        "port": 5432
    }

    conn, cursor = connect_to_db(db_config)
    if not conn:
        return

    try:
        # Create necessary tables
        create_tables(cursor)
        create_damage_taken_multipliers_table(cursor)

        # Process and insert Pokémon data
        pokemon_data_list = process_pokemon_data(get_all_pokemon_names(), get_pokemon_info)
        insert_pokemon_data(cursor, pokemon_data_list)
        print("Data inserted successfully!")

        # Create and insert damage multipliers
        create_damage_multipliers(cursor)
        conn.commit()
        print("Damage multipliers inserted successfully!")

    except Exception as e:
        print(f"Error in main process: {e}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
