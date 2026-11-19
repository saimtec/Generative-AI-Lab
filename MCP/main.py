
import asyncio
import os
import sys

from pathlib import Path
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent


# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


async def main():

    # 1. Configure MCP servers
    client = MultiServerMCPClient({

        "calculator": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [
                str(BASE_DIR / "math_server.py")
            ]
        },

        "weather": {
            "transport": "streamable_http",
            "url": "http://127.0.0.1:8000/mcp"
        }

    })

    # 2. Discover tools from both servers
    tools = await client.get_tools()

    print("\nAvailable MCP Tools:")

    for tool in tools:
        print(f"- {tool.name}: {tool.description}")

    # 3. Initialize Gemini
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    # 4. Create an AI agent with MCP tools
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=(
            "You are a helpful AI assistant. "
            "Use the available tools when needed. "
            "For calculations, use the calculator tools. "
            "For weather questions, use the weather tool. "
            "Explain the results clearly."
        )
    )

    print("\nGemini MCP Assistant Ready!")
    print("Type 'exit' to quit.\n")

    # 5. Chat loop
    while True:

        question = input("You: ")

        if question.lower() in ["exit", "quit"]:
            break

        try:

            response = await agent.ainvoke({
                "messages": [
                    {"role": "user", "content": question}
                ]
            })

            final_message = response["messages"][-1]

            print("\nAssistant:", final_message.content)
            print()

        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
