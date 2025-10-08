from google.adk.tools.mcp_tool import MCPToolset
from mcp import StdioServerParameters
from google.adk.tools.mcp_tool.mcp_toolset import StreamableHTTPConnectionParams


# def return_mcp_tools_exchange():
#     print("Attempting to connect to MCP server for exchange rate...")
#     tools = MCPToolset(
#         connection_params=StdioServerParameters(
#             command="python",
#             args=[
#                 "C:\\Users\\mauro\\PycharmProjects\\a2a_agent\\adk_a2a_mcp\\exchange_server.py"
#             ]
#         )
#     )
#     print("MCP Toolset created successfully.")
#     return [tools]
#
def return_http_mcp_tools_search():
    print("Attempting to connect to MCP server for math functions...")
    server_params = StreamableHTTPConnectionParams(
        url="http://localhost:8001/mcp",
    )
    tools = MCPToolset(connection_params=server_params)
    print("MCP Toolset created successfully.")
    return [tools]