import asyncio
from dotenv import load_dotenv, find_dotenv

from utils import generate_agent_card, generate_agent_task_manager
from agents.adk_agent import ADKAgent
from common.server.server import A2AServer
from common.types import (
    AgentSkill,
)
from google.adk.models.lite_llm import LiteLlm

load_dotenv(find_dotenv())

async def run_agent():
    AGENT_NAME = "host_agent"
    AGENT_DESCRIPTION = "An agent orchestrates the decomposition of the user request into tasks that can be performed by the child agents."
    PORT = 12000
    HOST = "0.0.0.0"
    AGENT_URL = f"http://{HOST}:{PORT}"
    AGENT_VERSION = "1.0.0"
    MODEL = LiteLlm('ollama_chat/llama3.2:latest')
    AGENT_SKILLS = [
        AgentSkill(
            id="COORDINATE_AGENT_TASKS",
            name="coordinate_tasks",
            description="call different agents to execute queries.",
        ),
    ]

    list_urls = [
        "http://localhost:8002/exchange_agent",
        "http://localhost:7002/math_agent",
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

    host_agent = ADKAgent(
        model=MODEL,
        name="host_agent",
        description="",
        tools=[],
        instructions="",
        is_host_agent=True,
        remote_agent_addresses=list_urls,
    )

    task_manager = generate_agent_task_manager(
        agent=host_agent,
    )
    server = A2AServer(
        host=HOST,
        port=PORT,
        endpoint="/host_agent",
        agent_card=AGENT_CARD,
        task_manager=task_manager
    )
    print(f"Starting {AGENT_NAME} A2A Server on {AGENT_URL}")
    await server.astart()


if __name__ == "__main__":
    asyncio.run(
        run_agent()
    )
