import asyncio
from dotenv import load_dotenv, find_dotenv

from utils import generate_agent_card, generate_agent_task_manager
from agents.adk_agent import ADKAgent
from common.server.server import A2AServer
from common.types import (
    AgentSkill,
)
from google.adk.models.lite_llm import LiteLlm
from adk_agents_testing.mcp_tools.mcp_tool_exchange import return_http_mcp_tools_search

load_dotenv(find_dotenv())

async def run_agent():
    AGENT_NAME = "exchange_agent"
    AGENT_DESCRIPTION = "An agent that provides exchange rates."
    PORT = 8002
    HOST = "0.0.0.0"
    AGENT_URL = f"http://{HOST}:{PORT}"
    AGENT_VERSION = "1.0.0"
    MODEL = LiteLlm('ollama_chat/qwen2.5:1.5b')
    AGENT_SKILLS = [AgentSkill(
            id="exchange",
            name="exchange",
            description="Provides exchange rates info.",
        )]

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
    exchange_tools = return_http_mcp_tools_search()

    exchange_agent = ADKAgent(
        model=MODEL,
        name="exchange_rate_agent",
        description="Handles queries about exchange rates.",
        tools=exchange_tools,
        instructions=(
            ""
        ),
    )

    task_manager = generate_agent_task_manager(
        agent=exchange_agent,
    )
    server = A2AServer(
        host=HOST,
        port=PORT,
        endpoint="/exchange_agent",
        agent_card=AGENT_CARD,
        task_manager=task_manager
    )
    print(f"Starting {AGENT_NAME} A2A Server on {AGENT_URL}")
    await server.astart()


if __name__ == "__main__":
    asyncio.run(
        run_agent()
    )
