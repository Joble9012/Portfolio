import psycopg2

def connect_to_db(db_config):
    """
    Establishes a connection to the database and returns the connection and cursor.
    """
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        print("Connected to the database")
        return conn, cursor
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None, None

def create_tables(cursor):
    """
    Creates the PokemonData and PokemonTypeDamageTaken tables in the database.
    """
    table_queries = [
        """
        CREATE TABLE IF NOT EXISTS PokemonData (
            pokemon_id INT UNIQUE PRIMARY KEY,
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
        """,
        """
        CREATE TABLE IF NOT EXISTS PokemonTypeDamageTaken (
            pokemon_id INT PRIMARY KEY,
            normal FLOAT, fire FLOAT, water FLOAT, electric FLOAT,
            grass FLOAT, ice FLOAT, fighting FLOAT, poison FLOAT,
            ground FLOAT, flying FLOAT, psychic FLOAT, bug FLOAT,
            rock FLOAT, ghost FLOAT, dragon FLOAT, dark FLOAT,
            steel FLOAT
        );
        """
    ]
    try:
        for query in table_queries:
            cursor.execute(query)
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")


def create_damage_taken_multipliers_table(cursor):
    """
    Creates the DamageTakenMultipliers table and inserts data into it.
    """
    drop_table_query = "DROP TABLE IF EXISTS DamageTakenMultipliers;"
    create_table_query = """
        CREATE TABLE DamageTakenMultipliers (
            Defender VARCHAR(20),
            Attacker VARCHAR(20),
            Multiplier FLOAT
        );
    """
    insert_data_query = """
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
        cursor.execute(drop_table_query)
        cursor.execute(create_table_query)
        cursor.execute(insert_data_query)
        print("DamageTakenMultipliers table created and data inserted successfully.")
    except Exception as e:
        print(f"Error creating table or inserting data: {e}")