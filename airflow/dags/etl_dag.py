from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import os
import sys
from utils.encodings_setup import load_env_api, load_env_cities, encoding, encodings_to_config
from utils.extract import city_weather_data_extraction, write_raw_data, write_compiled_raw_data
from utils.transform import read_raw_data, transform_data, write_to_cleaned_data



# set up process defined
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


# extract data process defined
def extract_data_process():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    ENV_PATH = os.path.join(BASE_DIR, "utils", ".env")
    CITIES_CONFIG_PATH = os.path.join(BASE_DIR, "utils", "cities_config.json")
    RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw_weather_data.json")
    RAW_COMPILED_PATH = os.path.join(BASE_DIR, "data", "raw_compiled_data.json")

    weather_data = city_weather_data_extraction(CITIES_CONFIG_PATH, ENV_PATH)
    write_raw_data(weather_data, RAW_DATA_PATH)
    write_compiled_raw_data(weather_data, RAW_COMPILED_PATH)

# transform data process defined
def transform_data_process():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw_weather_data.json")
    CLEAN_DATA_PATH = os.path.join(BASE_DIR, "data", "clean_weather_data.csv")

    data = read_raw_data(RAW_DATA_PATH)
    df = transform_data(data)
    write_to_cleaned_data(df, CLEAN_DATA_PATH)



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

# Extract Data Task
extract_data_task = PythonOperator(
    task_id="extract_write_raw_weather_data",
    python_callable=extract_data_process,
    dag=dag
)

# Transform Data Task
transform_data_task = PythonOperator(
    task_id="transform_write_data",
    python_callable=transform_data_process,
    dag=dag
)

# Load Data Task
    

# Set Task dependencies
settup_process_task >> extract_data_task >> transform_data_task