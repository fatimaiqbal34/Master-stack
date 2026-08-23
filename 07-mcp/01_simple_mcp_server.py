# 01_simple_mcp_server.py
# A simple MCP server that exposes a "tool" any MCP-compatible AI can use

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("MyFirstServer")

# Define a tool — this becomes available to any MCP client (like an AI assistant)
@mcp.tool()
def get_word_count(text: str) -> str:
    """Counts the number of words in the given text."""
    count = len(text.split())
    return f"The text contains {count} words."

@mcp.tool()
def reverse_text(text: str) -> str:
    """Reverses the given text."""
    return text[::-1]

if __name__ == "__main__":
    mcp.run()