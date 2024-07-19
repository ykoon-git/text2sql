import boto3
import os

# Initialize Athena client
athena_client = boto3.client('athena')

# Athena query input parameters
DATABASE_NAME = 'your_database_name'
QUERY = 'YOUR SQL QUERY HERE'

# Function handler
def lambda_handler(event, context):
    
    # Get the Athena query execution response
    response = athena_client.start_query_execution(
        QueryString=QUERY,
        QueryExecutionContext={'Database': DATABASE_NAME},
        ResultConfiguration={'OutputLocation': 's3://your-athena-output-bucket/'}
    )
    
    # Get the query execution ID
    query_execution_id = response['QueryExecutionId']
    
    # Get the query execution status
    while True:
        query_status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        query_execution_status = query_status['QueryExecution']['Status']['State']
        
        if query_execution_status == 'SUCCEEDED':
            print("Query execution succeeded")
            break
        
        elif query_execution_status == 'FAILED':
            print("Query execution failed")
            break
        
        else:
            print(f"Query is still running with status: {query_execution_status}")
    
    # Get the query results
    result_response = athena_client.get_query_results(QueryExecutionId=query_execution_id)
    
    # Process the query results
    results = result_response['ResultSet']['Rows']
    
    # Return the query results
    return results
