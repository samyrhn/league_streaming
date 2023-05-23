from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import boto3

def invoke_lambda_function():
    lambda_client = boto3.client('lambda', region_name='us-east-2')  # Change the region name if needed
    response = lambda_client.invoke(
        FunctionName='LambdaFunctionLeagueStreaming',  # Replace with your Lambda function's name
        InvocationType='Event'
    )
    return response['StatusCode']

dag = DAG(
    'lambda_invoker', 
    description='DAG to invoke a Lambda function every minute', 
    schedule_interval='* * * * *',
    start_date=datetime(2023, 5, 21),  # Replace with your desired start date
    catchup=False
)

invoke_lambda_task = PythonOperator(
    task_id='invoke_lambda', 
    python_callable=invoke_lambda_function, 
    dag=dag
)
