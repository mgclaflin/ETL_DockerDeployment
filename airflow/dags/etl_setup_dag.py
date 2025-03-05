from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import os
import sys
from utils.encodings_setup import load_env_api, load_env_cities, encoding, encodings_to_config




def setup_process():
    # Define the base directory explicitly
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Define file paths relative to the base directory
    ENV_PATH = os.path.join(BASE_DIR, "utils", ".env")
    CITIES_CONFIG_PATH = os.path.join(BASE_DIR, "utils", "cities_config.json")

    # Run functions from the encodings_setup.py script
    api_key = load_env_api(ENV_PATH)
    cities = load_env_cities(ENV_PATH)
    encodings = encoding(api_key, cities)
    encodings_to_config(encodings,CITIES_CONFIG_PATH)





dag = DAG(
    'etl_setup_dag',
    description='dag to initiate the setup of the env and variables',
    schedule_interval=None,  # Trigger manually for testing
    start_date=datetime(2025, 3, 1),
    catchup=False,
)

settup_process_task = PythonOperator(
    task_id="setup_env_variables",
    python_callable=setup_process,
    dag=dag

)
    

# Set Task dependencies
settup_process_task