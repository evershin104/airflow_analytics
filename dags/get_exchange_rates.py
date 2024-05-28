from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from dotenv import load_dotenv
import os
import requests
from sqlalchemy import create_engine, MetaData

# TODO
load_dotenv()
url = 'https://www.cbr-xml-daily.ru/latest.js'

def fetch_and_store_data():
    response = requests.get(url)
    if response.status_code == 200:
        response_data = response.json().get('rates')
        print(response)
    engine = create_engine(f'{os.getenv('AIRFLOW_DS_SQL_ALCHEMY_CONN')}')
    metadata = MetaData()



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
}

dag = DAG(
    'get_exchange_rates',
    default_args=default_args,
    description='Fetch data from API and store in DB',
    schedule_interval=timedelta(minutes=1),
    catchup=False
)

fetch_and_store_task = PythonOperator(
    task_id='fetch_and_store_data',
    python_callable=fetch_and_store_data,
    dag=dag,
)

fetch_and_store_task