from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo", port=8001)



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



# Add a prompt
@mcp.tool()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."

def main():
    # Initialize and run the server
    mcp.run(transport='stdio')
#fastmcp install mcp-json mcp_server_prova.py
if __name__ == "__main__":
    main()