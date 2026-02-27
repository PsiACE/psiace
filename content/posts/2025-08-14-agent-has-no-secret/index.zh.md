+++
title = "Agent 没有秘密可言"
description = "事件、队列、CRUD，再叠一层模型协作。先把反馈闭环跑通，比任何玄学包装都重要。"
date = 2025-08-14
slug = "agent-has-no-secret"

[taxonomies]
tags = ["agent", "event-driven", "huey", "eventure", "queue", "crud", "llm", "architecture"]

[extra]
lang = "zh"
mermaid = true
+++

> 我是 PsiACE。最近我的工作主要围绕 Agent 与 RAG 展开：**少谈玄学，多把闭环跑通**，多让系统说得清楚、跑得稳定、可被回放与切换。

## TL;DR

- **Agent 不是新宗教**。它依然是事件、队列、CRUD 的工程实践，再加一层模型协作。
- 共用一条 EventBus，把 `agent.*` 与 `huey.*` 事件打通；每条事件立即打印；最后用 Cascade 树复盘因果与时间。
- **单文件 Demo，打开即跑**：先看事件，后看因果，最后看结果。

![Cascade Viewer](cascade-viewer.png)

---

## 为什么写这个（以及为什么这么写）

- 我不想再讨论"如何画出一个复杂的 Agent 架构图"。我更关心"**如何让系统解释得清楚、失败得优雅、复盘得明白**"。
- 这篇文章附带一个单文件 Demo：共享总线、严格 ReACT、因果与时间合并呈现、即时可观测。**开箱即用**。

## 我怎么做的

### 核心设计原则

- **共享 EventBus**：Agent、ToolExecutor、Storage 都向同一条总线发事件。
- **严格 ReACT**：Thought → Action → Action Input → Observation → Final Answer。
- **因果 + 时间**：每轮用户输入推进 `tick`；每次 Observation 再推进 `tick`；`Action → huey.* → Observation` 通过 parent-child 串起来。
- **即时可观测**：每条事件实时打印；最后用树形 Cascade Viewer 做分时复盘。

### 事件流（概览）

![The Agent Loop](cascade-viewer.png)

## 这和"传统架构"有什么不同？

- **没有不同**：事件、队列、CRUD，本来就在；只是把模型作为协作者接了进来。
- **也不浮夸**：没有"智能"也不会失效的设计；它可靠、可解释，也更容易落地。

## 极简骨架（节选）

### Event-driven storage wrapper

```python
class EventureMemoryStorage(MemoryStorage):
    def __init__(self, event_bus: EventBus):
        super().__init__("huey")
        self.bus = event_bus

    def enqueue(self, data, priority=None):
        super().enqueue(data, priority=priority)
        self.bus.publish("huey.queue.enqueue", {
            "data": data,
            "priority": priority
        })
```

### Tool with self-description

```python
def tool_echo(params: dict) -> dict:
    """Echo back text. Args: {"text": string} Returns: {"ok": bool, "echo": string}"""
    return {"ok": True, "echo": str(params.get("text", ""))}
```

### ReACT loop（核心思想）

```python
while True:
    resp = client.chat.completions.create(model=model, messages=history)
    assistant = resp.choices[0].message.content or ""
    call = extract(assistant)

    if call:
        action_id = uuid4()
        bus.publish("agent.action", {"id": action_id, **call})
        # wait for agent.observation(id==action_id) and append as Observation
        continue

    return assistant
```

## 我遵循的几个原则

- **先闭环，后花活**：先把"事件→队列→状态变化→ReACT"打通，再谈优化。
- **因果与时间是工程的一等公民**：tick 表达更新周期；parent-child 表达触发链。
- **可观测性优先**：当系统能解释自己，优化才有基础。
- **可替换**：总线稳定，后端可换（内存→Redis），模型可换（供应商/版本）。

## 如何运行（单终端）

### 代码位置

请点击【阅读原文】跳转：

- [agent_has_no_secret.py](https://github.com/PsiACE/psiace/blob/main/demo/agent-has-no-secret/agent_has_no_secret.py)
- [README.md](https://github.com/PsiACE/psiace/blob/main/demo/agent-has-no-secret/README.md)

### 运行步骤

1. 配置 `.env`（OpenRouter 推荐；OpenAI 也可）
2. `python agent_has_no_secret.py`

### 你将看到什么

- **实时事件流**：`user.input`、`agent.thought`、`agent.action`、`huey.data.*`、`agent.observation` …
- 绿色的 **Final Answer** 面板
- 按 tick 分组的**树形 Cascade Viewer**：在 `agent.action` 下能看到 `huey.data.*` 与 `agent.observation` 的父子层级

---

## 写在最后

我更钦佩能把东西"**说清楚、跑起来**"的工程师。Agent 没有秘密可言：

- 先把闭环打通，再考虑花活；
- 先让因果与代价可见，再谈"更聪明"。
