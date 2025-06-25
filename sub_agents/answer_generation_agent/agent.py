from google.adk.agents import LlmAgent
from .prompts import ANSWER_GENERATION_INSTRUCTION_STR
from tools.visualization import visualization_execution_tool

# LLM Agent for generating final answer
answer_generation_agent = LlmAgent(
    name = "answer_generation_agent",
    model = "gemini-2.5-flash",
    description = f"This agent is responsible for converting data into final answer to the user query.",
    instruction = ANSWER_GENERATION_INSTRUCTION_STR,
    output_key = "answer_generation_output"
)