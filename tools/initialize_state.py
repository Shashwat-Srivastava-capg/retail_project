from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext
import os
from tools.bigquery_tools import bigquery_metdata_extraction_tool

def initialize_state_var(callback_context: CallbackContext):
    PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")
    BQ_LOCATION = os.environ.get("BQ_LOCATION")
    DATASET =  os.environ.get("DATASET")

    callback_context.state["PROJECT"] = PROJECT
    callback_context.state["BQ_LOCATION"] = BQ_LOCATION
    callback_context.state["DATASET"] =DATASET

    bigquery_metadata = bigquery_metdata_extraction_tool(PROJECT=PROJECT,
        BQ_LOCATION=BQ_LOCATION,
        DATASET=DATASET)

    callback_context.state["bigquery_metadata"] = bigquery_metadata
    callback_context.state["query_execution_output"] = None