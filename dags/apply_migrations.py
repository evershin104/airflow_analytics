from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime
# TODO
# Определение аргументов по умолчанию
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 1),
}

# Определение DAG
dag = DAG(
    'create_table_dag',
    default_args=default_args,
    description='A DAG that creates a table in the database upon deployment',
    schedule_interval=None,  # Установка None для триггера once
    start_date=datetime.now(),  # Текущая дата и время
)

# Определение задачи для создания таблицы
create_table_task = PostgresOperator(
    task_id='create_table',
    sql='''
        CREATE TABLE IF NOT EXISTS ai_attention_level_partitions (
            id SERIAL PRIMARY KEY,
            high FLOAT,
            medium FLOAT,
            green FLOAT,
            date DATE
        );
    ''',
    postgres_conn_id='postgres',  
    # Идентификатор соединения с PostgreSQL
    dag=dag,
)

# Задача будет выполнена один раз после создания DAG
create_table_task