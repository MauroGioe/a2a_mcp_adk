import asyncio
import os

from google.adk import Runner
from google.genai import types
from dotenv import load_dotenv, find_dotenv
from google.adk.models.lite_llm import LiteLlm
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool import McpToolset
from mcp import StdioServerParameters
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.agents import Agent,LlmAgent
load_dotenv(find_dotenv())

#quanto valgono 10 euro in yen?

async def get_agent_async():
  """Creates an ADK Agent equipped with tools from the MCP Server."""
  print("Attempting to connect to MCP Filesystem server...")
  exchange_tool =[ McpToolset(
      connection_params=StdioConnectionParams(server_params=StdioServerParameters(
                  command= "python.exe",
                  # Make sure to update to the full absolute path to your math_server.py file
                  args= ["mcp_server.py"])
  ))
  ]
  math_tool = [
      McpToolset(
          connection_params=StdioConnectionParams(server_params=StdioServerParameters(
              command="python.exe",
              # Make sure to update to the full absolute path to your math_server.py file
              args=["math_server.py"])
          ))
  ]
  print("MCP Toolset created successfully.")
  exchange_agent = Agent(
      model=LiteLlm('ollama_chat/qwen2.5:1.5b'), # Adjust model name if needed based on availability
      name='currency_exchange_agent',
      description="Agent to convert currencies",
      instruction="",
      tools=exchange_tool, # Provide the MCP tools to the ADK agent
  )
  math_agent = Agent(
      model=LiteLlm('ollama_chat/qwen2.5:1.5b'), # Adjust model name if needed based on availability
      name='math_exchange_agent',
      description="Agent to execute mathematical functions",
      instruction="",
      tools=math_tool, # Provide the MCP tools to the ADK agent
  )
  coordinator = LlmAgent(
      name="Coordinator",
      model=LiteLlm('ollama_chat/qwen2.5:1.5b'),
      description="I coordinate greetings and tasks.",
      sub_agents=[  # Assign sub_agents here
          exchange_agent,
          math_agent
      ]
  )

  return coordinator
# async def get_agent_async():
#   """Creates an ADK Agent equipped with tools from the MCP Server."""
#   print("Attempting to connect to MCP Filesystem server...")
#   tools =[ McpToolset(
#           connection_params=StdioConnectionParams(server_params=StdioServerParameters(
#               command="python.exe",
#               # Make sure to update to the full absolute path to your math_server.py file
#               args=["math_server.py"])
#           ))
#   ]
#   print("MCP Toolset created successfully.")
#   root_agent = Agent(
#       model=LiteLlm('ollama_chat/qwen2.5:1.5b'), # Adjust model name if needed based on availability
#       name='currency_exchange_agent',
#       description="Agent to convert currencies",
#       instruction="",
#       tools=tools, # Provide the MCP tools to the ADK agent
#   )
#   return root_agent, tools


async def async_main():
    session_service = InMemorySessionService()
    artifacts_service = InMemoryArtifactService()
    print("Creating session...")
    session = await session_service.create_session(
        state={}, app_name='mcp_exchane_app', user_id='exchanger_usr')
    print(session.id)
    query = input("Digita la domanda:")
    print(f"User Query: '{query}'")
    content = types.Content(role='user', parts=[types.Part(text=query)])
    coordinator = await get_agent_async()

    runner = Runner(
        app_name='mcp_exchane_app',
        agent=coordinator,
        artifact_service=artifacts_service,
        session_service=session_service,
    )

    print("Running agent...")
    events_async = runner.run_async(
        session_id=session.id, user_id=session.user_id, new_message=content
    )

    async for event in events_async:
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:  # Handle potential errors/escalations
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            print(f"############# Final Response #############\n\n{final_response_text}")
            break

    #Cleanup is handled automatically by the agent framework
    # print("Closing MCP server connection...")
    # for tool in tools:
    #     print(tool)
    #     await tool.close()
    #this works for one tool
    # print("Cleanup complete.")
    await runner.close()

if __name__ == '__main__':
    asyncio.run(async_main())