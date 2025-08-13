---
title: "Agent Has No Secret"
publishDate: 2025-08-14
slug: "agent-has-no-secret"
description: "Events + Queues + CRUD, plus a layer of models. Getting the feedback loop working is more valuable than talking metaphysics."
tags: ["agent", "event-driven", "huey", "eventure", "queue", "crud", "llm", "architecture"]
---

> I'm [PsiACE](https://github.com/PsiACE). My recent work focuses on Agent and RAG: **less metaphysics, more getting the feedback loop working**, making systems that can explain themselves clearly, run stably, and be replayed and switched.

## TL;DR

- **Agent is not a new religion**. It's still engineering practice with events, queues, and CRUD, plus a layer of model collaboration.
- Share one EventBus, connect `agent.*` and `huey.*` events; print every event immediately; finally use a Cascade tree to review causality and timing.
- **Single-file demo, run immediately**: first see events, then see causality, finally see results.

![Cascade Viewer](../../../public/images/agent-has-no-secret/cascade-viewer.png)

---

## Why I Write This (And Why This Way)

- I don't want to discuss "how to draw a complex Agent architecture diagram" anymore. I care more about "**how to make systems explain themselves clearly, fail gracefully, and review transparently**".
- This article comes with a single-file demo: shared bus, strict ReACT, causality and timing combined, immediate observability. **Ready to use**.

## How I Did It

### Core Design Principles

- **Shared EventBus**: Agent, ToolExecutor, Storage all publish to the same bus.
- **Strict ReACT**: Thought → Action → Action Input → Observation → Final Answer.
- **Causality + Timing**: Each user input advances `tick`; each Observation advances `tick`; `Action → huey.* → Observation` is linked through parent-child relationships.
- **Immediate Observability**: Print every event in real-time; finally use tree-shaped Cascade Viewer for time-based review.

### Event Flow (Overview)

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

## How Is This Different from "Traditional Architecture"?

- **No difference**: Events, queues, CRUD were already there; just connected models as collaborators.
- **No hype**: No design that fails when the word "intelligent" is removed; it's reliable, explainable, and easier to implement.

## Minimal Skeleton (Excerpt)

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

### ReACT loop (Core Idea)

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

## Principles I Follow

- **Feedback loop first, fancy features later**: Get "events → queue → state changes → ReACT" working before optimization.
- **Causality and timing are first-class citizens in engineering**: tick expresses update cycles; parent-child expresses trigger chains.
- **Observability first**: When systems can explain themselves, optimization has a foundation.
- **Replaceable**: Bus is stable, backend can be swapped (memory → Redis), models can be swapped (vendor/version).

## How to Run (Single Terminal)

### Code Location

- [agent_has_no_secret.py](file:///Users/psiace/MySelf/psiace/demo/agent-has-no-secret/agent_has_no_secret.py)
- [README.md](file:///Users/psiace/MySelf/psiace/demo/agent-has-no-secret/README.md)

### Running Steps

1. Configure `.env` (OpenRouter recommended; OpenAI also works)
2. `python agent_has_no_secret.py`

### What You'll See

- **Real-time event stream** (with colors): `user.input`, `agent.thought`, `agent.action`, `huey.data.*`, `agent.observation` …
- A green **Final Answer** panel
- A **tree-shaped Cascade Viewer** grouped by tick: under `agent.action` you can see the parent-child hierarchy of `huey.data.*` and `agent.observation`

---

## Final Thoughts

I admire engineers who can "**explain clearly and make things work**". Agent has no mystery:

- Get the feedback loop working first, then consider fancy features;
- Make causality and costs visible first, then talk about "smarter".
