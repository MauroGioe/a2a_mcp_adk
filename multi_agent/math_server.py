from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("math", port=8002)



# Add a multiplication tool
@mcp.tool()
def multiplication(a: int, b: int) -> int:
    """multipicate two numbers"""
    return a * b


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def main():
    # Initialize and run the server
    mcp.run(transport='stdio')
#fastmcp install mcp-json mcp_server_prova.py
if __name__ == "__main__":
    main()