from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime,timedelta
from kafka_producer import kafka_producer  # Import producer script
from kafka_consumer import kafka_to_postgres  # Import consumer script

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 12, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='kafka_postgres_pipeline',
    default_args=default_args,
    description='ETL pipeline to send data from Kafka to PostgreSQL',
    schedule=None,
    catchup=False,
    tags=['kafka', 'postgres', 'etl']
) as dag:
    
    # Task to start Kafka broker container
    start_kafka_broker = BashOperator(
        task_id='start_kafka_broker',
        bash_command='docker start broker || docker run -d -p 9092:9092 --name broker apache/kafka:latest',
    )

    # Task to run the Kafka producer
    producer_task = PythonOperator(
        task_id='run_kafka_producer',
        python_callable=kafka_producer,
    )

    # Task to run the Kafka consumer
    consumer_task = PythonOperator(
        task_id='run_kafka_consumer',
        python_callable=kafka_to_postgres,
    )

    # Set task dependencies
    start_kafka_broker >> producer_task >> consumer_task
