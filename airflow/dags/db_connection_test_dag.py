from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook
from airflow.utils.dates import days_ago
from datetime import datetime
import os

# Function to test the connection to the PostgreSQL container
def test_postgres_connection():
    # Setup the connection to the PostgreSQL database
    postgres_hook = PostgresHook(postgres_conn_id='postgres_weather_conn')
    
    # Run a simple query to test the connection
    connection = postgres_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute('SELECT 1;')  # A simple query to test the connection
    result = cursor.fetchone()
    
    if result:
        print("Connection successful! Query result:", result)
    else:
        print("Connection failed!")

    cursor.close()
    connection.close()

# Define the DAG
dag = DAG(
    'test_postgres_connection',
    description='Test connection to PostgreSQL container',
    schedule_interval=None,  # Trigger manually for testing
    start_date=datetime(2025, 3, 1),
    catchup=False,
)

# Add PostgreSQL connection programmatically (if not already set in Airflow UI)
def add_postgres_connection():
    conn_id = 'postgres_weather_conn'
    conn_type = 'Postgres'
    host = 'postgres_weather_container'  # Host from Docker container
    schema = 'weather'  # Database name
    login = 'weather_user'  # PostgreSQL user
    password = 'weather_user'  # PostgreSQL password
    port = 5432  # PostgreSQL default port

    # Check if the connection already exists
    conn = BaseHook.get_connection(conn_id)
    if not conn:
        # Create a new connection
        from airflow.models import Connection
        new_conn = Connection(
            conn_id=conn_id,
            conn_type=conn_type,
            host=host,
            schema=schema,
            login=login,
            password=password,
            port=port,
        )
        new_conn.set_upstream(None)
        new_conn.save()

# Add the connection before running the tasks
add_postgres_connection()

# Define the task to test the connection
test_connection_task = PythonOperator(
    task_id='test_postgres_connection_task',
    python_callable=test_postgres_connection,
    dag=dag,
)

# Set task dependencies
test_connection_task
