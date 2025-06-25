from google.adk.agents import LlmAgent
from .prompts import EXECUTION_FLOW_INSTRUCTION_STR

# LLM Agent for generating final answer
execution_flow_determiner = LlmAgent(
    name = "execution_flow_determiner",
    model = "gemini-2.5-flash",
    description = f"This agent is responsible for assessing whether answering user queries requires access to company data or not.",
    instruction = EXECUTION_FLOW_INSTRUCTION_STR,
    output_key = "execution_flow_output"
)