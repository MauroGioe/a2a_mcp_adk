from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import StreamableHTTPConnectionParams
from mcp import StdioServerParameters

#
# async def return_mcp_tools_search():
#     print("Attempting to connect to MCP server for search and page read...")
#     tools = await MCPToolset(
#         connection_params=StdioServerParameters(
#             command="/opt/homebrew/bin/uv",
#             args=[
#                 "--directory",
#                 "/Users/tsadoq/gits/a2a-mcp-tutorial/mcp_server",
#                 "run",
#                 "search_server.py"
#             ],
#             env={
#                 "MCP_PORT":"8000",
#                 "PYTHONPATH": "/Users/tsadoq/gits/a2a-mcp-tutorial:${PYTHONPATH}"
#             },
#         )
#     )
#     print("MCP Toolset created successfully.")
#     return tools


def return_http_mcp_tools_search():
    print("Attempting to connect to MCP server for math functions...")
    server_params = StreamableHTTPConnectionParams(
        url="http://localhost:7001/mcp",
    )
    tools = MCPToolset(connection_params=server_params)
    print("MCP Toolset created successfully.")
    return [tools]
