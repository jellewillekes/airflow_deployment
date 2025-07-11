from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def hello_world_minio():
    print("Hello World from Minio!")

with DAG(
    dag_id="hello_world_minio",
    start_date=datetime(2025, 6, 1),
    schedule_interval="@hourly",
    catchup=False,
    tags=["minio", "airflow"],
) as dag:
    task1 = PythonOperator(
        task_id="print_hello_minio",
        python_callable=hello_world_minio
    )
