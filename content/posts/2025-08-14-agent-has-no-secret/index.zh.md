+++
title = "Agent 没有什么秘密"
description = "事件、队列、CRUD，再叠一层模型协作。先把反馈闭环跑通，比任何玄学包装都重要。"
date = 2025-08-14
slug = "agent-has-no-secret"

[taxonomies]
tags = ["agent", "event-driven", "huey", "eventure", "queue", "crud", "llm", "architecture"]

[extra]
lang = "zh"
mermaid = true
+++

> 我是 [PsiACE](https://github.com/PsiACE)。这些年围着 Agent 和 RAG 打转，最后的共识只有一句：**少谈玄学，多把反馈闭环跑起来**。系统要能自证、能回放、能换件，这才叫工程。

## 三句话先交代清楚

- **Agent 不是新宗教。** 底层还是事件、队列、CRUD，只是多了一层模型协作。
- **总线要讲故事。** EventBus 把 `agent.*` 和 `huey.*` 串起来，事件实时打点，最后用 Cascade Viewer 把因果和时间线复盘。
- **先给 demo 再谈理念。** 我准备了一个单文件脚本，跑起来就能看到闭环、再决定要不要包装。

![Cascade Viewer](cascade-viewer.png)

---

## 为什么要把细节摊开讲

过去一年接触 Agent 相关项目，总有人问：“到底要不要上多智能体协作？”、“模型能不能自己规划？” 但真正让系统可靠的，是那些看似朴素的工程功夫：

- 事件怎么流转？
- 失败是怎么被记录、被回放的？
- 观察信息是不是足够让人看懂？

所以我换个角度写这篇文章：不再展开概念，而是以一个可跑的 demo 为骨架，讲清楚“如何把 Agent 做得像个正经服务”。

## 架构是这样落地的

### 设计原则

- **只有一个事件总线。** Agent、ToolExecutor、Storage 全都往 EventBus 写事件，不分支、不隐蔽。
- **遵循 ReACT 流程。** Thought → Action → Action Input → Observation → Final Answer，让模型有章可循，工具有证可查。
- **因果与时序同时可见。** 每次用户输入推进 `tick`，每个 Observation 也推进 `tick`；`Action → huey.* → Observation` 用父子关系串起来。
- **观察必须即时。** 事件第一时间打印日志，最后再用 Cascade Viewer 纵览整场对话。

### 事件流一览

```mermaid
graph TD
  User([User]) --> Agent
  Agent -->|publish Action| EventBus
  EventBus -->|agent.action| ToolExecutor
  ToolExecutor -->|huey.task| Huey
  Huey --> Storage[(EventureMemoryStorage)]
  Storage -->|huey.queue.* / huey.data.*| EventBus
  ToolExecutor -->|publish Observation| EventBus
  EventBus --> Agent
  EventBus --> EventLog
  EventLog --> Renderer[Cascade Viewer]
```

## 和“传统架构”有哪些区别？

- **底子没变。** 事件、队列、CRUD 这些“老面孔”依然在，只是我们把模型也当成协作者，纳入同一套流程。
- **拒绝玄乎。** 把“智能”两个字抹掉，系统照样能跑，这才叫可靠、可解释、可维护。
- **观测逻辑更丰富。** 传统队列只关心任务状态，这里我们得把“模型想了什么”“调用了什么”“拿到的结果是什么”都记下来。

## 最小骨架长什么样

### 事件驱动的存储封装

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

### 自带说明书的小工具

```python
def tool_echo(params: dict) -> dict:
    """Echo back text. Args: {"text": string} Returns: {"ok": bool, "echo": string}"""
    return {"ok": True, "echo": str(params.get("text", ""))}
```

### ReACT 回路的心跳

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

## 做项目时我守的几条线

- **先把反馈闭环跑通，再谈炫技。** 事件 → 队列 → 状态变更 → ReACT，通了再想优化。
- **因果与时序是一等公民。** `tick` 表示节奏，父子关系标记触发链。
- **观测优先。** 系统能自我解释，调优才有地基。
- **保持可换。** 总线稳定，后端可以换（内存 ↔ Redis），模型可以换（不同厂商 / 版本）。

## 现场演示：单终端就能跑

### 代码在哪

到 [PsiACE/psiace](https://github.com/PsiACE/psiace) 项目的 `demo` 目录拿最新版本：

- [agent_has_no_secret.py](https://github.com/PsiACE/psiace/blob/main/demo/agent-has-no-secret/agent_has_no_secret.py)
- [README.md](https://github.com/PsiACE/psiace/blob/main/demo/agent-has-no-secret/README.md)

### 运行方式

1. 配好 `.env`（推荐 OpenRouter，OpenAI 也行）
2. `python agent_has_no_secret.py`

### 屏幕上会看到

- **实时事件流**（带颜色）：`user.input`、`agent.thought`、`agent.action`、`huey.data.*`、`agent.observation` …
- 绿色的 **Final Answer** 面板
- **树状 Cascade Viewer** 按 tick 分组：`agent.action` 下面能看到 `huey.data.*` 与 `agent.observation` 的父子链

---

## 写在最后

我喜欢那种**讲得清楚又做得出来**的工程师。Agent 没什么神秘：

- 先让反馈闭环转起来，再谈“更智能”；
- 先把因果链和成本摊开，再谈“更聪明”。

搞 Agent，别膜拜神秘感，就和那些能当场拆给你看、并立刻跑给你看的人站在一边。
