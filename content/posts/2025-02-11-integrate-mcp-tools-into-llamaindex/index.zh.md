+++
title = "把 MCP 工具塞进 LlamaIndex 工作流"
description = "用一个适配器，让 MCP 服务器暴露的工具在 LlamaIndex Agent 里零改动复用。"
date = 2025-02-11
slug = "integrate-mcp-tools-into-llamaindex"

[taxonomies]
tags = ["MCP", "LlamaIndex", "Python"]

[extra]
lang = "zh"
+++

## 一、前言

本文主要介绍了如何将 MCP（Model Context Protocol，模型上下文协议）工具转换为可以直接使用的 LlamaIndex 工具，使 LlamaIndex 用户能像使用 Claude, Cursor 等现代 AI 应用一样无缝集成这些服务。

## 二、技术背景

### 2.1 什么是 MCP 协议？

MCP（模型上下文协议，https://modelcontextprotocol.io）是面向 AI 应用交互的服务构建协议。开发者可通过该协议构建具备数据资源（resources）、功能工具（tools）和提示模板（prompts）的服务端点。例如，我们可以定义获取 IP 详细信息的 fetch_ipinfo 工具：

```python
@mcp.tool()
async def fetch_ipinfo(ip: str | None = None, **kwargs) -> IPDetails:
    """获取指定IP的详细信息

    参数:
        ip(str or None): 目标 IP 地址，格式如 192.168.1.1
        **kwargs: 传递给 IPInfo 处理器的附加参数

    返回:
        IPDetails: 包含城市、时区等信息的结构化数据
    """
    handler = ipinfo.getHandler(
        access_token=os.environ.get("IPINFO_API_TOKEN"),
        headers={"user-agent": "basic-mcp-server"},
        **kwargs,
    )
    details = handler.getDetails(ip_address=ip)
    return IPDetails(**details.all)
```

### 2.2 LlamaIndex 框架特征

LlamaIndex（https://github.com/run-llama/llama_index）是构建知识索引系统的核心框架，其核心价值在于将外部信息结构化地接入大语言模型，实现高效的信息检索、智能问答和对话生成。当需要集成动态数据源时，将 MCP 工具转换为 LlamaIndex 工具成为关键技术需求。

在 LlamaIndex 中，NebulaGraph 已经有两种方法实现 GraphRAG：KnowledgeGraphIndex 用来对任何私有数据从零构建知识图谱（基于 LLM 或者其他语言模型），再 4 行代码进行 Graph RAG：

```python
graph_store = NebulaGraphStore(
    space_name=space_name,
    edge_types=edge_types,
    rel_prop_names=rel_prop_names,
    tags=tags,
)
storage_context = StorageContext.from_defaults(graph_store=graph_store)
# Build KG
kg_index = KnowledgeGraphIndex.from_documents(
    documents,
    storage_context=storage_context,
    max_triplets_per_chunk=10,
    space_name=space_name,
    edge_types=edge_types,
    rel_prop_names=rel_prop_names,
    tags=tags,
)
kg_query_engine = kg_index.as_query_engine()
```

KnowledgeGraphRAGQueryEngine 则可以在任何已经存在的知识图谱上进行 GraphRAG:

```python
graph_store = NebulaGraphStore(
    space_name=space_name,
    edge_types=edge_types,
    rel_prop_names=rel_prop_names,
    tags=tags,
)
storage_context = StorageContext.from_defaults(graph_store=graph_store)
graph_rag_query_engine = KnowledgeGraphRAGQueryEngine(
    storage_context=storage_context,
)
```

## 三、为什么需要将 MCP 集成至 LlamaIndex

在实际 AI 应用开发中，集成 MCP 工具主要解决以下需求：

- 功能复用：利用现有 MCP 生态（项目列表见 https://github.com/AlexMili/Awesome-MCP）快速扩展系统能力
- 流程统一：建立标准化工具调用范式，简化大模型对外部 API 的调用复杂度
- 自动化管理：通过自动转换机制实现 MCP 工具到 LlamaIndex FunctionTool 对象的映射，便于 Agent 自动调度

该集成方案可以有效降低开发成本，同时发挥 LlamaIndex 在上下文管理和对话生成方面的优势。

## 四、技术实现方案

实现流程包含三个关键阶段：

- MCP 服务通信：通过 MCPClient 类建立服务连接，支持工具发现（list_tools）和调用执行（call_tool）
- 适配器构建：定义 MCPToolAdapter 类，将 MCP 工具元数据转换为 LlamaIndex 的 FunctionTool 对象
- 智能代理集成：在 LlamaIndex Agent 中加载转换后的工具，实现自动化调用

## 五、核心代码解析

### 协议转换适配器

```python
from llama_index.core.tools import FunctionTool
from pydantic import create_model, BaseModel

class MCPToolAdapter:
    def __init__(self, client):
        self.client = client

    async def list_tools(self):
        tools = await self.client.list_tools()
        return [
            FunctionTool.from_defaults(
                fn=self._create_tool_fn(tool.name),
                name=tool.name,
                description=tool.description,
                fn_schema=self._create_pydantic_model(tool.schema),
            ) for tool in tools
        ]

    def _create_pydantic_model(self, json_schema):
        # 实现JSON Schema到Pydantic模型的动态转换
        ...
```

### 类型系统映射

```python
JSON_TYPE_MAPPING = {
    "string": str,
    "number": float,
    "integer": int,
    "boolean": bool,
    "object": dict,
    "array": list
}

def create_dynamic_model(schema):
    fields = {}
    for name, prop in schema["properties"].items():
        py_type = JSON_TYPE_MAPPING[prop["type"]]
        if name in schema.get("required", []):
            fields[name] = (py_type, Field(...))
        else:
            fields[name] = (Optional[py_type], Field(None))
    return create_model("DynamicModel", **fields)
```

### 服务调用封装

```python
async def fetch_ipinfo_wrapper(**kwargs):
    return await mcp_client.call_tool("fetch_ipinfo", kwargs)
```

### 关键技术创新点

- 动态模式转换：实现 JSON Schema 到 Pydantic 模型的运行时转换，保证参数校验的严格性
- 异步调用管道：基于 Python asyncio 构建非阻塞式服务调用，提升工具执行效率
- 协议抽象层：通过适配器模式解耦 MCP 协议与 LlamaIndex 框架，保证系统扩展性

将 MCP 工具的输入参数转换为 Pydantic 模型的原因在于：MCP 工具使用 JSON Schema 格式定义输入参数（在工具对象的 inputSchema 中，类型为 Dict[str, Any] ），而 create_model_from_json_schema 函数将其转换为 Pydantic 模型，该模型用作 LlamaIndex 中 FunctionTool 的 fn_schema。

## 六、LlamaIndex 中的 MCP 工具调用实践

以下代码来自 llamaindex_mcp_example.py，完整展示了 MCPToolAdapter 与 LlamaIndex 的集成方式：

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

# 系统级指令模板
SYSTEM_PROMPT = """\
您是一个智能法律助手

在回答用户问题前，必须通过IP信息确认用户所在司法管辖区
操作规则：
- 当涉及地理位置、时区等问题时，自动调用fetch_ipinfo工具
- 法律咨询类问题需结合IP所在国家/地区法律体系
"""

async def get_agent(adapter: MCPToolAdapter):
    """智能代理初始化函数"""
    tools = await adapter.list_tools()  # 获取MCP工具列表

    # 配置Azure OpenAI大语言模型
    llm = AzureOpenAI(
        model=os.environ.get("AZURE_OPENAI_MODEL", "gpt-4"),
        max_tokens=int(os.environ.get("AZURE_OPENAI_MAX_TOKENS", 4096)),
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        engine=os.environ.get("AZURE_OPENAI_ENGINE")
    )

    # 构建ReAct智能代理
    agent = ReActAgent.from_tools(
        llm=llm,
        tools=list(tools),
        react_chat_formatter=ReActChatFormatter(
            system_header=SYSTEM_PROMPT + "\n" + REACT_CHAT_SYSTEM_HEADER,
        ),
        max_iterations=20,  # 限制最大推理步数
        verbose=True        # 启用详细日志
    )
    return agent

async def handle_user_message(message_content: str, agent: ReActAgent):
    """消息处理流水线"""
    user_message = ChatMessage.from_str(role="user", content=message_content)
    response = await agent.achat(message=user_message.content)
    print(f"[智能代理响应] {response.response}")

if __name__ == "__main__":
    async def main():
        # 命令行参数解析
        parser = argparse.ArgumentParser()
        parser.add_argument("--client_type",
                          choices=["sse", "stdio"],
                          default="stdio",
                          help="连接模式：sse(Server-Sent Events)或stdio(标准输入输出)")
        args = parser.parse_args()

        # MCP客户端初始化
        if args.client_type == "sse":
            client = MCPClient("http://0.0.0.0:8000/sse")  # SSE长连接模式
        else:
            client = MCPClient(                            # 子进程模式
                "./venv/bin/python",
                ["mcp_server.py", "--server_type", "stdio"]
            )

        # 工具适配器初始化
        adapter = MCPToolAdapter(client)
        agent = await get_agent(adapter)

        # 执行测试用例
        await handle_user_message("我的IP所在城市是哪里？", agent)
        await handle_user_message("持有大麻在我国是否合法？", agent)

    anyio.run(main)  # 启动异步运行时
```

### 关键实现解析

- 工具获取机制：
  - 通过 adapter.list_tools() 动态加载 MCP 服务端注册的工具列表
  - 自动将每个 MCP 工具转换为 LlamaIndex 的 FunctionTool 对象
- 智能代理配置：
  - 使用 Azure OpenAI 作为底层大语言模型引擎
  - 集成 ReAct 推理框架，支持多步工具调用
  - 设置 20 步的最大推理深度防止无限循环
- 消息处理流程：
  - 将用户输入封装为标准化 ChatMessage
  - 通过 agent.achat() 触发自动化工具调用链

## 七、运行 Demo

### 7.1 标准输入输出模式

```bash
python llamaindex_mcp_example.py --client_type stdio
```

### 执行输出示例

```text
[DEBUG] 检测到ListToolsRequest协议请求
[工具调用] 步骤ID: ede14770-91c9-428b... | 输入: 我的IP所在城市是哪里？
[推理日志] 当前用户语言：中文，需调用工具获取数据
[动作触发] fetch_ipinfo | 参数: {}
[网络请求] 调用MCP工具耗时128ms
[观察结果] {"ip": "183.193.123.192", "city": "上海", "country": "CN"...}
[最终响应] 您的IP所在城市为上海

[法律咨询] 步骤ID: e728f5d0-6c0e-454a... | 输入: 持有大麻是否合法？
[推理日志] 已确认用户所在国家：中国
[知识库检索] 加载中国刑法第357条
[最终响应] 根据中国法律，持有大麻属违法行为，最高可判处有期徒刑
```

### 7.2 SSE 服务模式

```bash
# 终端1：启动SSE服务端
python mcp_server.py --server_type sse

# 终端2：运行客户端
python llamaindex_mcp_example.py --client_type sse
```

## 八、技术方案总结

通过以下三步实现深度集成：

### 协议通信层

- 基于 MCPClient 实现服务发现与工具调用
- 支持 SSE/STDIO 双模连接，适应不同部署场景

### 类型转换层

- 动态将 JSON Schema 转换为 Pydantic 模型
- 实现参数自动校验与类型提示

```python
def create_dynamic_model(schema):
    # 自动生成带字段描述的Pydantic模型
    fields = {
        name: (map_type(prop), Field(..., description=prop["description"]))
        for name, prop in schema["properties"].items()
    }
    return create_model("DynamicModel", **fields)
```

### 智能代理层

- 集成 ReAct 推理框架实现自动化工具调度
- 通过系统提示词约束工具使用规范

```python
SYSTEM_PROMPT = """\
法律咨询必须遵循以下规则：
1. 首次响应前必须调用fetch_ipinfo确认用户辖区
2. 引用法律条文需标注具体条款编号
3. 不得对未覆盖地区提供法律建议"""
```

通过持续扩展 MCP 生态，开发者可快速构建具备专业领域能力的智能代理系统。欢迎访问 MCP 开发者社区获取更多工具资源。

查看源代码：https://github.com/psiace/psiac
