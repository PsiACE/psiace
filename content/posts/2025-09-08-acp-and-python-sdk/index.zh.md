+++
title = "ACP：交互契约与 Python SDK"
description = "Zed 把 ACP 当作统一交互协议；我做了个 Python SDK，让接入这套协议的门槛降到周末项目水平。"
date = 2025-09-08
slug = "acp-and-python-sdk"

[taxonomies]
tags = ["agent", "zed", "protocol", "acp", "agent-client-protocol"]

[extra]
lang = "zh"
+++

## TL;DR

- ACP（Agent Client Protocol）是“客户端 ↔ 智能体”之间的交互契约，定义会话、内容块、工具调用、计划、文件系统等语义。
- Zed 以 ACP 为核心，让内置与外部智能体共享同一套 UX，开发者只需实现一次协议即可通吃多个宿主。
- 我写了 Python SDK：`pip install agent-client-protocol`，提供 Pydantic 模型、`AgentSideConnection`、stdio helper，帮你快速接上。
- 这是一场标准化竞赛。ACP 与 MCP、A2A、AG-UI 互补又竞合，谁先积累生态谁就有话语权。

## ACP 解决了什么

ACP 不只是“一条管道”，它规定：

- 传输层用 JSON-RPC，支持流式更新；
- 会话生命周期（new/load/prompt/cancel）清晰；
- 内容块支持文本、图片、音频、资源链接等；
- 工具调用与更新（`tool_call` / `tool_call_update`）格式统一；
- 文件读写、任务计划、状态同步都有规范字段。

换句话说，宿主（如 Zed）与智能体之间的 UX 语义不再每家重造，体验可以搬家。

## 与其他标准的关系

- **AG-UI**：同样关注交互层，部分语义重合，可能会出现“互转/共存”的场景。
- **MCP**：负责工具和资源接入，适合与 ACP 搭配使用（工具能力来自 MCP，交互流程由 ACP 承载）。
- **A2A**：聚焦智能体之间的通信，后续也可能与 ACP 对接。

## Zed 的视角

- 使用者：可以把 Claude Code、Gemini CLI、内部 Agent 统统接进编辑器，享受一致的流式体验和工具栏。
- 开发者：写一次 ACP，就能跑在任何支持它的宿主上，减少重复 glue code。
- 平台：通过协议锁定体验，生态统一，支持成本下降。

## Python SDK 提供了什么

安装：

```bash
pip install agent-client-protocol
```

功能：

- Pydantic v2 模型：schema 都有类型提示；
- `AgentSideConnection` / `ClientSideConnection`：分别处理智能体端与客户端；
- stdio helper：适合 CLI/本地进程场景；
- 与官方 schema 对齐，严格校验。

### 最小 Echo Agent

```python
import asyncio
from acp import Agent, AgentSideConnection, stdio_streams
from acp import InitializeRequest, InitializeResponse, NewSessionRequest, NewSessionResponse
from acp import PromptRequest, PromptResponse, AuthenticateRequest, LoadSessionRequest, CancelNotification

class EchoAgent(Agent):
    async def initialize(self, params: InitializeRequest) -> InitializeResponse:
        return InitializeResponse(protocolVersion=params.protocolVersion)

    async def newSession(self, params: NewSessionRequest) -> NewSessionResponse:
        return NewSessionResponse(sessionId="sess-1")

    async def loadSession(self, params: LoadSessionRequest) -> None:
        return None

    async def authenticate(self, params: AuthenticateRequest) -> None:
        return None

    async def prompt(self, params: PromptRequest) -> PromptResponse:
        return PromptResponse(stopReason="end_turn")

    async def cancel(self, params: CancelNotification) -> None:
        return None

async def main() -> None:
    reader, writer = await stdio_streams()
    AgentSideConnection(lambda _conn: EchoAgent(), writer, reader)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
```

Zed 侧 `settings.json`：

```json
{
  "agent_servers": {
    "Echo Agent (Python)": {
      "command": "/abs/path/to/python",
      "args": ["/abs/path/to/echo_agent.py"],
      "env": {}
    }
  }
}
```

打开命令面板输入 “dev: open acp logs” 可以调试序列化。

## 接下来

- 补充更多示例：工具调用、文件交互、计划同步；
- 与 MCP 结合，做端到端 demo；
- 观察协议演进，及时跟进 schema 变更。

ACP 代表的是“交互语义的标准化”。当智能体要进主流工作流时，拥有统一契约就像当年云原生时代的容器、服务网格一样重要。Python SDK 的目标，就是让这件事变得简单，让反馈闭环先跑起来，再慢慢打磨。EOF
