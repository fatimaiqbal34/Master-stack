# 02_mcp_client_test.py
# A simple client that connects to our MCP server and calls its tools

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="py",
        args=["01_simple_mcp_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Call a tool
            result = await session.call_tool(
                "get_word_count", 
                arguments={"text": "This is a test sentence for MCP"}
            )
            print("\nResult:", result.content[0].text)

            result2 = await session.call_tool(
                "reverse_text",
                arguments={"text": "Hello MCP"}
            )
            print("Result:", result2.content[0].text)

asyncio.run(main())