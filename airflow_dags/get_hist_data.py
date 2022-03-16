from datetime import timedelta, datetime

from airflow import DAG

from airflow.operators.bash import BashOperator

with DAG(
    'get_hist_data',
    default_args={
        'depends_on_past': False,
        'email': ['ukarroum17@gmail.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    },
    schedule_interval="0 6 * * 2-6",
    start_date=datetime(2019, 1, 1),
    tags=['binance', 'data']
) as dag:
    get_binance_pub_data = BashOperator(
        task_id='get_public_data',
        bash_command='python3 ~/Projects/binance-public-data/python/download-trade.py -d {{ yesterday_ds }}'
    )
