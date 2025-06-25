from google.cloud import bigquery
from typing import List, Dict, Any
import pandas as pd

def bigquery_metdata_extraction_tool(PROJECT: str,
    BQ_LOCATION: str,
    DATASET: str) -> List[Dict[str, Any]]:
    """
        This is python program that extracts the bigquery tables and columns 
        for the given dataset provides the information in the form of list of dictionary.
        
        Args:
        `PROJECT`: GCP Project to execute the query on
        `BQ_LOCATION`: Bigquery Location
        `DATASET`: Name of the dataset
        
        Returns:
        List of dictionaries, Each dictionary in list contains the keys table_name, column_name, data_type and description of the column
    """
    client = bigquery.Client(project=PROJECT)

    query = f"""
        select table_name, column_name, data_type, description
        from `region-{BQ_LOCATION}.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS`
        where table_catalog = "{PROJECT}"
        and table_schema = "{DATASET}"
    """

    query_job = client.query(query)
    query_list = []

    for row in query_job:
        query_list.append(dict(row.items()))
    return query_list


def bigquery_execution_tool(PROJECT:str, BQ_LOCATION:str, DATASET:str, TABLE:str, SQL_QUERY:str):
    """
        This is python program that executes sql queries on given bigquery tables
        for the given dataset and returns data in the form of a markdown table.
        
        Args:
        `PROJECT`: GCP Project to execute the query on
        `BQ_LOCATION`: Bigquery Location
        `DATASET`: Name of the dataset
        'TABLE': Name of the table in the dataset for executing the query
        'SQL_QUERY': SQL query to be executed. The query should already contain the dataset and table name for execution
        
        Returns:
        Data fetched using the query in the form of a markdown table
    """
    # Initialize the BigQuery client
    client = bigquery.Client(project=PROJECT)

    # Execute the query
    query_job = client.query(SQL_QUERY, location=BQ_LOCATION)

    # Wait for the job to complete and get the results
    results = query_job.result()

    # Convert results to a DataFrame
    df = results.to_dataframe()

    # Convert DataFrame to markdown table
    markdown_table = df.to_markdown(index=False)
    
    return markdown_table
