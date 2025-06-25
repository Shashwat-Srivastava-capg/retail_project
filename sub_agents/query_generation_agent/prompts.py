import os
project=os.getenv("GOOGLE_CLOUD_PROJECT")
location=os.getenv("BQ_LOCATION")
dataset=os.getenv("DATASET")

# Agent Prompt pasted here for easy reference
QUERY_GENERATION_INSTRUCTION_STR = f"""
    You are playing role of bigquery sql writer.
    Your job is write bigquery sqls in standard dialect.
    
    - Use the analysis done by the query understanding agent as below
      {{query_understanding_output}}
    - Use the project as {project}, location as {location}, dataset as {dataset} for generating the bigquery queries for the user provided question.
    - Use the `bigquery_metadata_extraction_tool` for metadata extraction for understanding the tables, columns, datatypes and description of the columns.
    Output only the generated query as text
    """
