import os
from llama_index.core.llms import ChatMessage
from llama_index.core.agent import ReActAgent, ReActChatFormatter
from llama_index.core.agent.react.prompts import REACT_CHAT_SYSTEM_HEADER
from llama_index.llms.azure_openai import AzureOpenAI

from llamaindex_mcp_adapter import MCPToolAdapter
from mcp_client import MCPClient
import anyio
import dotenv
import argparse

dotenv.load_dotenv()

SYSTEM_PROMPT = """\
You are an AI assistant.

Before you answer the user's question, you need to fetch the ip info first, to help you follow the laws of the country.

- When user ask about current ip info, location, city, country or timezone, use the 'fetch_ipinfo' tool to provide the answer.
"""


async def get_agent(adapter: MCPToolAdapter):
    tools = await adapter.list_tools()
    llm = AzureOpenAI(
        model=os.environ.get("AZURE_OPENAI_MODEL", "your-model-name"),
        max_tokens=int(os.environ.get("AZURE_OPENAI_MAX_TOKENS", 4096)),
        azure_endpoint=os.environ.get(
            "AZURE_OPENAI_ENDPOINT", "https://your-azure-endpoint.openai.azure.com"
        ),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY", "your-api-key"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "your-api-version"),
        engine=os.environ.get("AZURE_OPENAI_ENGINE", "your-deployment-name"),
    )
    agent = ReActAgent.from_tools(
        llm=llm,
        tools=list(tools),
        react_chat_formatter=ReActChatFormatter(
            system_header=SYSTEM_PROMPT + "\n" + REACT_CHAT_SYSTEM_HEADER,
        ),
        max_iterations=20,
        verbose=True,
    )
    return agent


async def handle_user_message(message_content: str, agent: ReActAgent):
    user_message = ChatMessage.from_str(role="user", content=message_content)
    response = await agent.achat(message=user_message.content)
    print(response.response)


if __name__ == "__main__":

    async def main():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--client_type", type=str, default="sse", choices=["sse", "stdio"]
        )
        args = parser.parse_args()

        if args.client_type == "sse":
            client = MCPClient("http://0.0.0.0:8000/sse")
        else:
            client = MCPClient(
                "./venv/bin/python", ["mcp_server.py", "--server_type", "stdio"]
            )

        adapter = MCPToolAdapter(client)

        agent = await get_agent(adapter)

        await handle_user_message("What's the city of my current ip?", agent)
        await handle_user_message("Is it legal to hold drugs in my country?", agent)

    anyio.run(main)
