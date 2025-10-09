+++
title = "Integrate MCP tools into LlamaIndex"
description = "Learn how to integrate MCP tools into LlamaIndex, with a end-to-end demo."
date = 2025-02-11
slug = "integrate-mcp-tools-into-llamaindex"

[taxonomies]
tags = ["MCP", "LlamaIndex", "Python"]

[extra]
lang = "en"
+++

> [!NOTE]
> This work has been contributed to upstream [llama-index](https://github.com/run-llama/llama-index) as `McpToolSpec` in the [`llama-index-tools-mcp`](https://pypi.org/project/llama-index-tools-mcp/) package. You can find the pull request [llama_index#17795 feat: add mcp tool spec](https://github.com/run-llama/llama_index/pull/17795) and try out the example notebook [llama-index-tools-mcp/examples/mcp.ipynb](https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/tools/llama-index-tools-mcp/examples/mcp.ipynb) directly.

This article mainly introduces how to convert MCP (Model Context Protocol) tools into LlamaIndex tools that can be directly used, allowing [LlamaIndex](https://github.com/run-llama/llama_index) users to seamlessly integrate these services like other modern and popular AI applications like Claude and Cursor, etc.

## 1. Background

### 1.1 What is MCP?

MCP(Model Context Protocol, https://modelcontextprotocol.io) is a protocol for building services that interact with AI applications. It allows developers to build servers that expose features like data (resources), functions (tools), and prompts. For example, we can define a `fetch_ipinfo` tool that retrieves detailed information about a specified IP address (such as city and timezone). code here: [mcp_server.py](https://github.com/psiace/psiace/tree/main/demo/llamaindex-mcp-adapter/mcp_server.py)

```python
@mcp.tool()
async def fetch_ipinfo(ip: str | None = None, **kwargs) -> IPDetails:
    """Get the detailed information of a specified IP address

    Args:
        ip(str or None): The IP address to get information for. Follow the format like 192.168.1.1 .
        **kwargs: Additional keyword arguments to pass to the IPInfo handler.
    Returns:
        IPDetails: The detailed information of the specified IP address.
    """
    handler = ipinfo.getHandler(
        access_token=os.environ.get("IPINFO_API_TOKEN", None),
        headers={"user-agent": "basic-mcp-server", "custom_header": "yes"},
        **kwargs,
    )

    details = handler.getDetails(ip_address=ip)

    return IPDetails(**details.all)
```

### 1.2 What is LlamaIndex?

LlamaIndex (https://github.com/run-llama/llama_index) is a framework for building, managing, and calling index systems. It aims to bring external information into large language models in a structured way, achieving more efficient information retrieval, question answering, and dialogue generation. When using LlamaIndex, you often need to call external tools to get dynamic data, which can be considered as converting MCP tools into LlamaIndex tools.

## 2. Why do we need to convert MCP tools to LlamaIndex tools?

In actual scenarios, you may want to:

- Use the rich features exposed by the MCP servers, there is a list of MCP servers https://github.com/AlexMili/Awesome-MCP .
- Integrate MCP tools into LlamaIndex to form a unified workflow, simplifying the process of calling external APIs with large language models.
- Automatically convert MCP tools to FunctionTool objects in LlamaIndex, making it easier for LlamaIndex Agent to automatically call and manage tools.

By doing this, you can easily reuse the tools already in MCP, without having to write code again, and also use the powerful dialogue generation and context management capabilities of LlamaIndex.

## 3. Implementation

Implementing the conversion of MCP tools to LlamaIndex tools mainly includes the following steps:

- **Communicate with MCP server**:
  - Establish a connection with the MCP server using the `MCPClient` class, at least support `list_tools` and `call_tool` methods.
  - See [mcp_client.py](https://github.com/psiace/psiace/tree/main/demo/llamaindex-mcp-adapter/mcp_client.py) for reference.
- **Construct adapter**:
  - Define the `MCPToolAdapter` class, which uses the MCPClient's `list_tools` method to get the tool list and uses the `FunctionTool.from_defaults` method in LlamaIndex to wrap each MCP tool into a LlamaIndex tool.
  - See [llamaindex_mcp_adapter.py](https://github.com/psiace/psiace/tree/main/demo/llamaindex-mcp-adapter/llamaindex_mcp_adapter.py) for reference.
- **Use the adapter in LlamaIndex**:
  - In LlamaIndex, use the adapter to get tools, and then use the agent to call the tools.
  - See [llamaindex_mcp_example.py](https://github.com/psiace/psiace/tree/main/demo/llamaindex-mcp-adapter/llamaindex_mcp_example.py) for reference.

## 4. Code Example

### 4.1 MCPToolAdapter

The following code is from [llamaindex_mcp_adapter.py](https://github.com/psiace/psiace/tree/main/demo/llamaindex-mcp-adapter/llamaindex_mcp_adapter.py), which shows how to convert MCP tools to LlamaIndex tools:

```python
from typing import Any, Dict, List, Optional, Type
from llama_index.core.tools import FunctionTool
from mcp_client import MCPClient
from pydantic import BaseModel, Field, create_model

json_type_mapping: Dict[str, Type] = {
    "string": str,
    "number": float,
    "integer": int,
    "boolean": bool,
    "object": dict,
    "array": list
}

def create_model_from_json_schema(schema: Dict[str, Any], model_name: str = "DynamicModel") -> Type[BaseModel]:
    properties = schema.get("properties", {})
    required_fields = set(schema.get("required", []))
    fields = {}

    for field_name, field_schema in properties.items():
        json_type = field_schema.get("type", "string")
        field_type = json_type_mapping.get(json_type, str)

        if field_name in required_fields:
            default_value = ...
        else:
            default_value = None
            field_type = Optional[field_type]

        fields[field_name] = (field_type, Field(default_value, description=field_schema.get("description", "")))

    dynamic_model = create_model(model_name, **fields)
    return dynamic_model


class MCPToolAdapter:
    def __init__(self, client: MCPClient):
        self.client = client

    async def list_tools(self) -> List[FunctionTool]:
        response = await self.client.list_tools()
        return [
            FunctionTool.from_defaults(
                fn=self._create_tool_fn(tool.name),
                name=tool.name,
                description=tool.description,
                fn_schema=create_model_from_json_schema(tool.inputSchema),
            )
            for tool in response.tools
        ]

    def _create_tool_fn(self, tool_name: str):
        async def tool_fn(**kwargs):
            return await self.client.call_tool(tool_name, kwargs)

        return tool_fn
```

Explanation:

- **JSON Schema to Pydantic model**:

  - The function `create_model_from_json_schema` builds a dynamic Pydantic model based on the JSON Schema defined in the MCP tool, making it easier to validate tool parameters and provide auto-completion.

- **Adapter's list_tools method**:

  - This method fetches the tool list from the server using `MCPClient`, then wraps each tool with `FunctionTool.from_defaults`, and finally obtains a list of tools that can be used by the LlamaIndex Agent.

- **Dynamic call MCP tool**:

  - The helper method `_create_tool_fn` returns an asynchronous function, which internally calls `self.client.call_tool` to implement the actual tool calling logic.

> Why we need to convert MCP tool's input parameters to Pydantic model?
>
> MCP tool defines the input parameters in JSON Schema format (`inputSchema` in `Tool` object, which is `Dict[str, Any]`), and the `create_model_from_json_schema` function converts it to a Pydantic model, which is used as the `fn_schema` of the `FunctionTool` in LlamaIndex.

### 4.2 Usage in LlamaIndex

The following code is from [llamaindex_mcp_example.py](https://github.com/psiace/psiace/tree/main/demo/llamaindex-mcp-adapter/llamaindex_mcp_example.py), which shows how to use the `MCPToolAdapter` with LlamaIndex:

```python
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
```

Explanation:

- **Get MCP tools**:
  - Use `MCPToolAdapter` to get MCP tools and convert them to LlamaIndex tools.
- **Create Agent**:
  - Use `ReActAgent.from_tools` to build an Agent, which embeds Azure OpenAI's LLM.
- **Process user messages**:
  - The user's message is analyzed by the Agent, triggering the corresponding MCP tool (e.g., calling `fetch_ipinfo`).

This approach seamlessly converts MCP tools to LlamaIndex tools, greatly reducing integration complexity.

## 5. Running the Demo

You can run the demo with the following command:

```bash
python llamaindex_mcp_example.py --client_type stdio
```

The demo will start a MCP server using `stdio` mode, and then use the `MCPToolAdapter` to get MCP tools and convert them to LlamaIndex tools. Also, it will use the `AzureOpenAI` to call the tools and generate responses.

The demo also provides a `sse` mode, you can run the demo with the following command:

```bash
python mcp_server.py --server_type sse
python llamaindex_mcp_example.py --client_type sse # in another terminal session
```

The following is the output of the demo, with the `stdio` mode:

```bash
Processing request of type ListToolsRequest
> Running step ede14770-91c9-428b-a66a-d57d20e0b5d5. Step input: What's the city of my current ip?
Thought: The current language of the user is: English. I need to use a tool to help me answer the question.
Action: fetch_ipinfo
Action Input: {'kwargs': AttributedDict()}
Processing request of type CallToolRequest
Observation: meta=None content=[TextContent(type='text', text='{"ip": "183.193.123.192", "hostname": null, "city": "Shanghai", "region": "Shanghai", "country": "CN", "loc": "31.2222,121.4581", "timezone": "Asia/Shanghai"}')] isError=False
> Running step 45ea121b-9c05-431f-b409-d235409c1556. Step input: None
Thought: I can answer without using any more tools. I'll use the user's language to answer.
Answer: The city of your current IP is Shanghai.
The city of your current IP is Shanghai.
> Running step 4006f760-1070-4b0c-8446-7db886bc7c2e. Step input: Is it legal to hold drugs in my country?
Thought: The current language of the user is: English. I need to use a tool to help me answer the question.
Action: fetch_ipinfo
Action Input: {'kwargs': AttributedDict()}
Processing request of type CallToolRequest
Observation: meta=None content=[TextContent(type='text', text='{"ip": "183.193.123.192", "hostname": null, "city": "Shanghai", "region": "Shanghai", "country": "CN", "loc": "31.2222,121.4581", "timezone": "Asia/Shanghai"}')] isError=False
> Running step e728f5d0-6c0e-454a-aeb9-a654ace0e41b. Step input: None
Thought: I have obtained the IP information, including the country, which is China. Now I can provide information regarding the legality of holding drugs in China.
Answer: In China, the possession of drugs is illegal and can lead to severe penalties, including imprisonment. It is important to be aware of and comply with local laws regarding drug possession.
In China, the possession of drugs is illegal and can lead to severe penalties, including imprisonment. It is important to be aware of and comply with local laws regarding drug possession.
```

## 6. Summary

This article details how to convert MCP tools to LlamaIndex tools. By:

- Interacting with MCP servers using `MCPClient`;
- Automatically converting tool parameter definitions (using JSON Schema to convert to Pydantic models) through `MCPToolAdapter`;
- Integrating converted tools into LlamaIndex `ReActAgent` and calling them;

Now you can seamlessly integrate MCP tools into LlamaIndex, reducing development costs and providing great flexibility for AI application expansion.

Welcome to explore the combination of MCP and LlamaIndex, and further expand more practical tools and functions!

---

See the [demo](https://github.com/psiace/psiace/tree/main/demo/llamaindex-mcp-adapter) for more details.
