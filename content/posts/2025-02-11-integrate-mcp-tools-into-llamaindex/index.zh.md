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

> 这份适配器后来合入了官方仓库 [`llama-index-tools-mcp`](https://pypi.org/project/llama-index-tools-mcp/)，可以直接 pip 安装。示例笔记本在 [examples/mcp.ipynb](https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/tools/llama-index-tools-mcp/examples/mcp.ipynb)。

## 想解决什么问题

MCP（Model Context Protocol）兴起之后，社区里出现了大量“即插即用”的工具服务：查 IP、读数据库、连知识库、调存储……但 LlamaIndex 的 Agent 默认只能识别自己的 `FunctionTool`。我想要的体验是：**给我一个 MCP 服务器地址，我就能把里面的工具全部接到 LlamaIndex 的工作流里。**

## 思路概述

1. **MCPClient**：负责和 MCP 服务器握手，最少要实现 `list_tools`、`call_tool`。
2. **MCPToolAdapter**：拉取 MCP 工具，把 JSON Schema 映射成 Pydantic 模型，然后用 `FunctionTool.from_defaults` 包装。
3. **Agent 侧使用**：把适配出来的工具丢给 ReAct Agent 或者任何 LlamaIndex Agent，像原生工具一样调用。

这样就能做到“工具一次实现，多处复用”，而且保留了 MCP 工具自带的输入校验与描述信息。

## 关键代码片段

```python
class MCPToolAdapter:
    def __init__(self, client: MCPClient):
        self.client = client

    async def list_tools(self) -> List[FunctionTool]:
        response = await self.client.list_tools()
        tools = []
        for tool in response.tools:
            schema = create_model_from_json_schema(tool.inputSchema)
            async def _tool_fn(**kwargs):
                return await self.client.call_tool(tool.name, kwargs)
            fn = FunctionTool.from_defaults(
                fn=_tool_fn,
                name=tool.name,
                description=tool.description,
                fn_schema=schema,
            )
            tools.append(fn)
        return tools
```

`create_model_from_json_schema` 会根据 MCP 工具描述生成动态的 Pydantic 模型：字段、类型、是否必填、说明文字统统带上。LlamaIndex 在执行工具时就能验证参数，也能在调试 UI 里展示字段说明。

## 实际效果

- 运行一个简单的 MCP 服务器，暴露 `fetch_ipinfo` 等工具；
- 让适配器连上去，自动把这些工具注册进 LlamaIndex ReAct Agent；
- 当 Agent 需要查 IP 时，会自动调用 MCP 工具，拿到城市、时区等信息，再返回给用户。

这意味着你可以把已有的 MCP 工具目录（比如 [Awesome MCP](https://github.com/AlexMili/Awesome-MCP)）拉来直接用，而不用为每个平台单独写一份 glue code。

## 适合谁

- 已经部署 MCP 服务，但想在 LlamaIndex 场景下继续复用的团队；
- 想把工具定义留在 MCP，保持统一权限与审计，却又想在对话式 Agent 中灵活调用的人；
- 想减少“每个平台都要写一遍工具 SDK”维护成本的建设者。

总之，这个适配器做的就是一件事：**把工具定义和调用逻辑统一到 MCP，LlamaIndex 负责对话编排，两者互不牵制。**
