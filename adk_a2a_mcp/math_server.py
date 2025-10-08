from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("math", host="127.0.0.1", port=7001)



# Add a multiplication tool
@mcp.tool()
def multiplication(a: int, b: int) -> int:
    """multipicate two numbers
    :param a: multiplying
    :param b: multiplier"""
    return a * b


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def main():
    # Initialize and run the server
    mcp.run(transport='streamable-http')
#fastmcp install mcp-json mcp_server_prova.py
if __name__ == "__main__":
    main()