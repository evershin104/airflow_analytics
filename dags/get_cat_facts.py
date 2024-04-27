from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import requests
import psycopg2

def get_api_data():
    response = requests.get('https://catfact.ninja/fact')
    data = response.json()
    return data

def insert_into_db(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='get_api_data')

    conn = psycopg2.connect(
        dbname="your_dbname",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )

    cur = conn.cursor()
    cur.execute("INSERT INTO your_table (fact) VALUES (%s)", (data['fact'],))
    conn.commit()
    cur.close()
    conn.close()

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(2),
}

dag = DAG(
    'cat_fact_dag',
    default_args=default_args,
    description='A simple DAG to fetch cat facts from an API and insert into a PostgreSQL database',
    schedule_interval='@daily',
)

t1 = PythonOperator(
    task_id='get_api_data',
    python_callable=get_api_data,
    dag=dag,
)

t2 = PythonOperator(
    task_id='insert_into_db',
    python_callable=insert_into_db,
    provide_context=True,
    dag=dag,
)

t1 >> t2