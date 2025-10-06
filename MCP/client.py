import asyncio

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_ollama import ChatOllama
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

model = ChatOllama(model="llama3.2:latest",temperature=0)
#server_params = StdioServerParameters(command="python", args=["mcp_server_prova.py"])

client = MultiServerMCPClient(
    {
        "Demo": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["mcp_server_prova.py"],
            "transport": "stdio",
        },
        "CSV Editor": {
            # Make sure you start your weather server on port 8000
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["csv_editor_server.py"],
            "transport": "stdio"
        }
    }
)





def get_prompt():
    return input()


async def run_agent():
    context=""
    tools = await client.get_tools()
    print(tools)
    agent = create_react_agent(model, tools)
    while True:
        prompt = get_prompt()
        prompt_context = context + "\n User:"+prompt
        if prompt in ["quit","exit"]:
            break
        agent_response = await agent.ainvoke({"messages":prompt_context} )
        agent_response = agent_response["messages"][-1].content
        print(agent_response)
        context += f"Context:\nUser:{prompt}\nAI: {agent_response}"
        #print(context)





# async def run_agent():
#     context=""
#     async with stdio_client(server_params) as (read, write):
#         async with ClientSession(read, write) as session:
#             await session.initialize()
#             tools = await load_mcp_tools(session)
#             agent = create_react_agent(model, tools)
#             while True:
#                 prompt = get_prompt()
#                 prompt_context = context + "\n User:"+prompt
#                 if prompt in ["quit","exit"]:
#                     break
#                 agent_response = await agent.ainvoke({"messages":prompt_context}, )
#                 agent_response = agent_response["messages"][-1].content
#                 print(agent_response)
#                 context += f"Context:\nUser:{prompt}\nAI: {agent_response}"
#                 #print(context)
if __name__ ==  "__main__":
    asyncio.run(run_agent())


