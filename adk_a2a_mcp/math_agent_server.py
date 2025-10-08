import asyncio
from typing import List, Any

from dotenv import load_dotenv, find_dotenv
from google.adk import Agent
from google.adk.tools import google_search

from utils import generate_agent_task_manager, generate_agent_card
from agents.adk_agent import ADKAgent
from common.agent_task_manager import AgentTaskManager
from common.server.server import A2AServer
from common.types import (
    AgentCard,
    AgentCapabilities,
    AgentSkill,
)
from google.adk.models.lite_llm import LiteLlm
from adk_agents_testing.mcp_tools.mcp_tool_math import return_http_mcp_tools_search

load_dotenv(find_dotenv())

async def run_agent():
    AGENT_NAME = "math_agent"
    AGENT_DESCRIPTION = "An agent that handles mathematical queries."
    HOST = "0.0.0.0"
    PORT = 7002
    AGENT_URL = f"http://{HOST}:{PORT}"
    AGENT_VERSION = "1.0.0"
    MODEL = LiteLlm('ollama_chat/qwen2.5:1.5b')
    AGENT_SKILLS = [
        AgentSkill(
            id="math",
            name="math",
            description="Handles mathematical queries.",
        ),
    ]

    AGENT_CARD = generate_agent_card(
        agent_name=AGENT_NAME,
        agent_description=AGENT_DESCRIPTION,
        agent_url=AGENT_URL,
        agent_version=AGENT_VERSION,
        can_stream=False,
        can_push_notifications=False,
        can_state_transition_history=True,
        default_input_modes=["text"],
        default_output_modes=["text"],
        skills=AGENT_SKILLS,
    )

    math_tools = return_http_mcp_tools_search()

    google_search_agent = ADKAgent(
        model=MODEL,
        name="math_agent",
        description="Handles mathematical queries",
        tools=math_tools,
        instructions=(
            "."
        ),
    )

    task_manager = generate_agent_task_manager(
        agent=google_search_agent,
    )
    server = A2AServer(
        host=HOST,
        port=PORT,
        endpoint="/math_agent",
        agent_card=AGENT_CARD,
        task_manager=task_manager
    )
    print(f"Starting {AGENT_NAME} A2A Server on {AGENT_URL}")
    await server.astart()


if __name__ == "__main__":
    asyncio.run(
        run_agent()
    )
