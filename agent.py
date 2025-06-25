"""
MIT License

Copyright (c) 2024 Ngoga Alexis

This is an educational example demonstrating how to integrate Google ADK with Chainlit.
Feel free to use, modify, and share this code for learning purposes.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so.

See the LICENSE file for the full license text.
"""
import os
import requests
import vertexai
from langchain_google_vertexai import VertexAIEmbeddings
from google.adk.agents import Agent
from os import getenv
from dotenv import load_dotenv
from google.adk.agents import SequentialAgent

#from .sub_agents.sales_agent import sales_agent
#from .sub_agents.inventory_agent import inventory_agent
#from .sub_agents.campaign_performance_agent import campaign_performance_agent
#from .sub_agents.recommendations_agent import recommendations_agent
#from .prompts import GLOBAL_INSTRUCTION, INSTRUCTION

# Load environment variables
load_dotenv()


EMBEDDING_MODEL = "text-embedding-005"
LLM_LOCATION = "global"
LOCATION = "us-central1"
LLM = "gemini-2.5-flash"
project_id=os.getenv("GOOGLE_CLOUD_PROJECT")

vertexai.init(project=project_id, location=LOCATION)
embedding = VertexAIEmbeddings(
    project=project_id, location=LOCATION, model_name=EMBEDDING_MODEL
)

EMBEDDING_COLUMN = "embedding"
TOP_K = 5

data_store_region = os.getenv("DATA_STORE_REGION", "global")
data_store_id = os.getenv("DATA_STORE_ID", "sales-data-store_1750426506579")

retriever = get_retriever(
    project_id=project_id,
    data_store_id=data_store_id,
    data_store_region=data_store_region,
    embedding=embedding,
    embedding_column=EMBEDDING_COLUMN,
    max_documents=10,
)

compressor = get_compressor(
    project_id=project_id,
)


def retrieve_docs(query: str) -> str:
    """
    Useful for retrieving relevant data based on a query.
    Use this when you need sales data to answer a question.

    Args:
        query (str): The user's question or search query.

    Returns:
        str: Formatted string containing relevant document content retrieved and ranked based on the query.
    """
    try:
        # Use the retriever to fetch relevant documents based on the query
        retrieved_docs = retriever.invoke(query)
        # Re-rank docs with Vertex AI Rank for better relevance
        ranked_docs = compressor.compress_documents(
            documents=retrieved_docs, query=query
        )
        # Format ranked documents into a consistent structure for LLM consumption
        formatted_docs = format_docs.format(docs=ranked_docs)
    except Exception as e:
        return f"Calling retrieval tool with query:\n\n{query}\n\nraised the following error:\n\n{type(e)}: {e}"

    return formatted_docs


instruction = """You are an AI assistant for finding insights related to sales data of company Carrefour.
You have a tool - 'retrieve_docs', which can retrieve relevant data from the week on week 5 year sales data for the company.
The sales data has the following fields and data types:
Date: dd-mm-yyyy
SKU_ID: str
Product_Name: str
Category: str
Customer_Segment: str
Store_ID: str
Region: str
Units_Sold: int
Revenue: float
Price_per_Unit: float
Cost_per_Unit: float
Margin_per_Unit: float
Stock_Level: int
Promotion_Flag: int (0 or 1) - 1 denotes that the item was purchased as a part of a promotion
Bundle_Flag: int (0 or 1) - 1 denotes that the item was purchased as a part of a bundle
Holiday_Indicator: int (0 or 1) - 1 denotes that the item was purchased on a holiday
Cultural_Event_Flag: int (0 or 1) - 1 denotes that the item was purchased on a cultural event

Approach for resolving the user query:
1. Based on the user query, determine an approach to solve the problem using sales data.
2. Identify what data will be required out of the fields of sales data. Fetch the data using the get_sales_data tool.
3. Analyze the data to create insights for the user based on the approach decided in step 1. For example: The sale of Category 'Dairy' has reduced by 10% over the last 30 days
4. Verify if the insight would help resolve the query of the user.
5. If not satisfied with the insight, refine the existing approach and again fetch more data from the tool.
 """

def get_sales_data(fields: str) -> str:
    """
    Useful for retrieving relevant sales data based on defined parameters.
    Use this when you need sales data to answer a question.

    Args:
        fields (str): list of all required columns concatenated in a comma-separated string
        category: Optional product category filter.
        region: Optional region filter.
        customer_segment: Optional customer segment filter.
        promotion_flag: 0 or 1 to filter promotional sales.
        bundle_flag: 0 or 1 to filter bundled sales.
        holiday_indicator: 0 or 1 to filter holiday sales.
        cultural_event_flag: 0 or 1 to filter cultural event sales.
        date_range: Optional tuple of (start_date, end_date) in 'dd-mm-yyyy' format.
        tool_context: Provided by ADK for session state tracking.


    Returns:
        
        dict: A dictionary with:
            - "status": "success" or "error"
            - If success: "records": list of matching records
            - If error: "error_message": explanation

    """
    data_source=

root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash",
    instruction=instruction,
    tools=[retrieve_docs],
)

OPENCAGE_API_KEY = getenv("OPENCAGE_API_KEY")

def get_location(latitude: str, longitude: str) -> dict:
    """Returns the place name based on latitude and longitude."""
    try:
        params = {
            'q': f"{latitude},{longitude}",
            'key': OPENCAGE_API_KEY,
            'language': 'en',
            'pretty': 1
        }
        response = requests.get("https://api.opencagedata.com/geocode/v1/json", params=params)
        response.raise_for_status()
        data = response.json()

        if data['results']:
            place_name = data['results'][0]['formatted']
            return {"status": "success", "report": f"The location is: {place_name}"}
        else:
            return {"status": "error", "error_message": "No results found for the given coordinates."}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}



#retail_manager_agent = SequentialAgent(
#    name='retail_manager_agent',
#    model='gemini-2.5-flash',
#    description=(
#        'Understands user query in the context of Carrefour Spain,  '
#        ' an international retail chain, and supports category managers and leadership to improve their'
#        ' performance.'
#    ),
#    instruction=INSTRUCTION,
#    sub_agents=[sales_agent, inventory_agent, campaign_performance_agent, recommendations_agent],
#)

#root_agent = retail_manager_agent
