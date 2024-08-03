from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'engin',
    'start_date': datetime(2024, 7, 30)
}

with DAG('scrape_dag',
    default_args=default_args,
    schedule_interval='* * * * *',
    catchup=False) as dag:

    scraping_task = BashOperator(
        task_id='scraping_task',
        bash_command='scrapy crawl newspider -a tag=bitcoin',
        dag=dag
    )