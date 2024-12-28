import pandas as pd
from api_client import insert_pokemon_data, get_pokemon_info, get_all_pokemon_names
from data_processing import process_pokemon_data
from database_manager import connect_to_db, create_tables, DamageTakenMultipliers_create_tables
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta




def connect_to_database():
    import psycopg2
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="your_password",
        host="localhost",
        port=5432
    )
    print("Connected to the database")
    # Return only serializable data, such as connection details
    return {"dbname": "postgres", "host": "localhost", "port": 5432}


def setup_tables(cursor):
    create_tables(cursor)
    DamageTakenMultipliers_create_tables(cursor)

def get_batch_index(dag_run, **kwargs):
    # Use the 'dag_run' to track which batch to process
    batch_index = kwargs['dag_run'].conf.get('batch_index', 0)  # Default to batch 0 if not set
    return batch_index

def process_and_insert_pokemon_data(cursor):
    pokemon_data_list = process_pokemon_data(get_all_pokemon_names(), get_pokemon_info)
    insert_pokemon_data(cursor, pokemon_data_list)


def insert_multipliers(cursor):
    insert_Multipliers = """
        CREATE TEMP TABLE DamageTakenAggregated AS
        SELECT
        Defender,
        MAX(CASE WHEN Attacker = 'Normal' THEN Multiplier END) AS normal,
        -- (Other columns truncated for brevity)
        FROM DamageTakenMultipliers
        GROUP BY Defender;

        WITH type_multipliers AS (
        -- (Insert query here)
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
    cursor.execute(insert_Multipliers)


def close_connection(conn, cursor):
    cursor.close()
    conn.close()


# Define the Airflow DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 12, 28),
    'retries': 1,
}

dag = DAG(
    'pokemon_data_pipeline',
    default_args=default_args,
    description='A DAG for processing Pokemon data in batches',
    schedule_interval=timedelta(minutes=1),  # Runs every minute
    catchup=False,  # Prevent running backlogged tasks
)

# Define Airflow tasks
connect_task = PythonOperator(
    task_id='connect_to_database',
    python_callable=connect_to_database,
    dag=dag,
)

setup_tables_task = PythonOperator(
    task_id='setup_tables',
    python_callable=setup_tables,
    op_kwargs={'cursor': '{{ task_instance.xcom_pull(task_ids="connect_to_database")[1] }}'},
    dag=dag,
)

process_and_insert_pokemon_task = PythonOperator(
    task_id='process_and_insert_pokemon_data',
    python_callable=process_and_insert_pokemon_data,
    op_kwargs={'cursor': '{{ task_instance.xcom_pull(task_ids="connect_to_database")[1] }}'},
    dag=dag,
)

insert_multipliers_task = PythonOperator(
    task_id='insert_multipliers',
    python_callable=insert_multipliers,
    op_kwargs={'cursor': '{{ task_instance.xcom_pull(task_ids="connect_to_database")[1] }}'},
    dag=dag,
)

close_connection_task = PythonOperator(
    task_id='close_connection',
    python_callable=close_connection,
    op_kwargs={
        'conn': '{{ task_instance.xcom_pull(task_ids="connect_to_database")[0] }}',
        'cursor': '{{ task_instance.xcom_pull(task_ids="connect_to_database")[1] }}',
    },
    dag=dag,
)

# Define the task to process the next batch of Pokémon
def process_batch_pokemon_data(batch_index, **kwargs):
    all_pokemon_names = get_all_pokemon_names()  # Fetch all Pokémon names
    pokemon_data_list = process_pokemon_data(all_pokemon_names, get_pokemon_info, batch_index * 10)
    # Insert processed data into the database or perform other tasks here
    insert_pokemon_data(pokemon_data_list)

process_batch_task = PythonOperator(
    task_id='process_batch_pokemon_data',
    python_callable=process_batch_pokemon_data,
    op_kwargs={'batch_index': '{{ task_instance.xcom_pull(task_ids="get_batch_index") }}'},  # Pull the current batch index from XCom
    dag=dag,
)

# Set task dependencies
connect_task >> setup_tables_task >> process_batch_task >> process_and_insert_pokemon_task >> insert_multipliers_task >> close_connection_task