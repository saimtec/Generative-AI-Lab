from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Calculator Server")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers and return their sum."""
    return a + b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return their product."""
    return a * b


if __name__ == "__main__":
    mcp.run(transport="stdio")
