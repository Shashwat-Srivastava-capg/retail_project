from google.adk.agents import LlmAgent, BaseAgent
from sub_agents.query_understanding_agent.agent import query_understanding_agent
from sub_agents.query_generation_agent.agent import query_generation_agent
from sub_agents.query_review_rewrite_agent.agent import query_review_rewrite_agent
from sub_agents.query_execution_agent.agent import query_execution_agent
from sub_agents.answer_generation_agent.agent import answer_generation_agent
from sub_agents.execution_flow_determiner.agent import execution_flow_determiner
from tools.initialize_state import initialize_state_var
import json
import uuid
import time
from google.genai import types

from typing import Dict, Any, List
from typing import AsyncGenerator
from typing_extensions import override
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext
from google.adk.tools import ToolContext
import logging
from PIL import Image
import io

import chainlit as cl
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
import os
from dotenv import load_dotenv

# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Orchestrator Agent
class OrchestratorAgent(BaseAgent):
    execution_flow_determiner: LlmAgent
    query_understanding_agent: LlmAgent
    query_generation_agent: LlmAgent
    query_review_rewrite_agent: LlmAgent
    query_execution_agent: LlmAgent
    answer_generation_agent: LlmAgent


    def __init__(self,
        name:str,
        execution_flow_determiner: LlmAgent,
        query_understanding_agent: LlmAgent,
        query_generation_agent: LlmAgent,
        query_review_rewrite_agent: LlmAgent,
        query_execution_agent:LlmAgent,
        answer_generation_agent: LlmAgent
        ):
        
        super().__init__(
            name = name,
            execution_flow_determiner = execution_flow_determiner,
            query_understanding_agent = query_understanding_agent,
            query_generation_agent = query_generation_agent,
            query_review_rewrite_agent = query_review_rewrite_agent,
            query_execution_agent=query_execution_agent,
            answer_generation_agent=answer_generation_agent,
            before_agent_callback=initialize_state_var,
            description = "This is a Orchestrator Agent which executes the workflow using the sub_agents provided"
        )

    @override
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        logger.info(f"[{self.name}] - Starting workflow.")

        async for event in self.execution_flow_determiner.run_async(ctx):
            logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event
        
        execution_flow_output = ctx.session.state['execution_flow_output'] 
        
        if execution_flow_output=="yes":
            async for event in self.answer_generation_agent.run_async(ctx):
                yield event
        else:
            # First call to query_understanding_agent
            async for event in self.query_understanding_agent.run_async(ctx):
                logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
                yield event
            
            query_understanding_output = ""
            if "query_understanding_output" in ctx.session.state:
                query_understanding_output = ctx.session.state['query_understanding_output']
                logger.info(f"[{self.name}] - {query_understanding_output}")

            if query_understanding_output is None or "```json" not in query_understanding_output:
                return
            
            # query generation agent call
            async for event in self.query_generation_agent.run_async(ctx):
                logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
                yield event
            
            query_generation_output = ctx.session.state['query_generation_output']
            logger.info(f"[{self.name}] - {query_generation_output}")

            if query_generation_output is None:
                return

            # query review rewrite agent call
            async for event in self.query_review_rewrite_agent.run_async(ctx):
                logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
                yield event
            
            query_review_rewrite_output = ctx.session.state['query_review_rewrite_output']
            logger.info(f"[{self.name}] - {query_review_rewrite_output}")

            if query_review_rewrite_output is None:
                return
            
            # query execution agent call
            async for event in self.query_execution_agent.run_async(ctx):
                logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
                yield event
            
            query_execution_output = ctx.session.state['query_execution_output']
            logger.info(f"[{self.name}] - {query_execution_output}")

            if query_execution_output is None:
                return
            
            #answer_generation agent
            
            async for event in self.answer_generation_agent.run_async(ctx):
                yield event
            answer_generation_output = ctx.session.state.get('answer_generation_output')
            
            if answer_generation_output is None:
                logger.warning(f"[{self.name}] - No output from answer_generation_agent.")
                return

        


orchestrator_agent = OrchestratorAgent(name="orchestrator_agent",
    execution_flow_determiner=execution_flow_determiner,
    query_understanding_agent=query_understanding_agent,
    query_generation_agent=query_generation_agent,
    query_review_rewrite_agent=query_review_rewrite_agent,
    query_execution_agent=query_execution_agent,
    answer_generation_agent=answer_generation_agent
    )

root_agent = orchestrator_agent

# Set up session service and runner
session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()
APP_NAME = "retail_app"
runner = Runner(agent=root_agent, artifact_service=artifact_service, app_name=APP_NAME, session_service=session_service)

@cl.on_chat_start
async def start():
    """Initialize the chat session."""
    # Create a new session for each chat
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id="chainlit_user",
        session_id=cl.user_session.get("session_id", "session_001")
    )
    cl.user_session.set("session_id", session.id)

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages."""
    try:
        # Create content from the message
        content = types.Content(role='user', parts=[types.Part(text=message.content)])
        
        # Get the session ID
        session_id = cl.user_session.get("session_id")
        
        # Process the message through the ADK agent using the runner
        # Run in executor since runner.run() is synchronous
        loop = asyncio.get_event_loop()
        events = await loop.run_in_executor(
            None,
            lambda: runner.run(
                user_id="chainlit_user",
                session_id=session_id,
                new_message=content
            )
        )
        
        # Process each event from the generator
        for event in events:
            if event.is_final_response():
                # Extract the text content from the event
                response_text = ""
                if hasattr(event, 'content') and event.content:
                    if hasattr(event.content, 'parts'):
                        for part in event.content.parts:
                            if hasattr(part, 'text'):
                                response_text += part.text
                    elif isinstance(event.content, str):
                        response_text = event.content
                
                if response_text:
                    await cl.Message(content=response_text).send()
                else:
                    await cl.Message(content="...").send()
            
    except Exception as e:
        await cl.Message(
            content=f"An error occurred: {str(e)}\nTrace: {type(e).__name__}"
        ).send()