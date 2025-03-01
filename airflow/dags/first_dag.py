from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'matthew',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id="first_dag",  # snake_case is recommended for dag_id
    default_args=default_args,
    description="first attempt at setting up a dag",
    start_date=datetime(2021, 7, 8, 2),
    schedule_interval='@daily',  # Fixed argument name
    catchup=False 
) as dag:
    task1 = BashOperator(  # Fixed typo here
        task_id='first_task',
        bash_command='echo hello world, this is the first task'
    )

    task1  # You can leave this or define further task dependencies if needed.
