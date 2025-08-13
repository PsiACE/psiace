from __future__ import annotations
import json
import os
import threading
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from openai import OpenAI
from huey import Huey
from huey.storage import MemoryStorage
from eventure import EventLog, EventBus
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme
from rich.tree import Tree
from rich.rule import Rule
import threading as _threading


# Rendering: EventRenderer
class EventRenderer:
    def __init__(self) -> None:
        self.console = Console(
            theme=Theme(
                {
                    "user": "bold magenta",
                    "thought": "yellow",
                    "action": "bold cyan",
                    "observation": "green",
                    "error": "bold red",
                    "hueyq": "dim cyan",
                    "hueyd": "dim white",
                }
            )
        )

    def _style_for(self, et: str) -> tuple[str, str]:
        if et == "user.input":
            return "user", "User Input"
        if et == "agent.thought":
            return "thought", "Thought"
        if et == "agent.action":
            return "action", "Action"
        if et == "agent.observation":
            return "observation", "Observation"
        if et == "agent.error":
            return "error", "Error"
        if et.startswith("huey.queue"):
            return "hueyq", et
        if et.startswith("huey.data"):
            return "hueyd", et
        return "", et

    def print_event(self, e) -> None:
        style, title = self._style_for(e.type)
        self.console.print(
            Panel.fit(str(e.data), title=f"{title} (tick {e.tick})", style=style)
        )

    def print_final(self, text: str) -> None:
        self.console.print(
            Panel.fit(text or "<empty>", title="Final Answer", style="observation")
        )

    def print_cascade(self, events) -> None:
        self.console.print(Rule("Cascade Viewer"))
        ticks = sorted({ev.tick for ev in events})
        for t in ticks:
            tick_events = [ev for ev in events if ev.tick == t]
            by_id = {ev.id: ev for ev in tick_events}
            children: Dict[str, List] = {}
            roots = []
            for ev in tick_events:
                if ev.parent_id and ev.parent_id in by_id:
                    children.setdefault(ev.parent_id, []).append(ev)
                else:
                    roots.append(ev)
            tree = Tree(f"TICK {t}", guide_style="bright_black")

            def add(ev, parent):
                style, title = self._style_for(ev.type)
                node = parent.add(f"[{style}]{title}[/] • {ev.type} • {ev.id}")
                node.add(f"data: {ev.data}")
                for ch in children.get(ev.id, []):
                    add(ch, node)

            for r in roots:
                add(r, tree)
            self.console.print(tree)


# 1) Eventured MemoryStorage: wrap Huey's MemoryStorage and emit events on ops
class _EventContext:
    def __init__(self) -> None:
        self._local = _threading.local()

    def set_parent(self, ev):
        self._local.parent = ev

    def get_parent(self):
        return getattr(self._local, "parent", None)

    def clear(self):
        if hasattr(self._local, "parent"):
            delattr(self._local, "parent")


class EventureMemoryStorage(MemoryStorage):
    def __init__(
        self,
        name: str = "huey",
        event_bus: EventBus | None = None,
        ctx: _EventContext | None = None,
        **kwargs,
    ):
        super().__init__(name, **kwargs)
        if event_bus is None:
            raise ValueError("event_bus is required")
        self.event_bus = event_bus
        self._ctx = ctx or _EventContext()

    # Queue operations
    def enqueue(self, data, priority=None):
        super().enqueue(data, priority=priority)
        self.event_bus.publish(
            "huey.queue.enqueue",
            {"data": data, "priority": priority},
            parent_event=self._ctx.get_parent(),
        )

    def dequeue(self):
        data = super().dequeue()
        self.event_bus.publish(
            "huey.queue.dequeue", {"data": data}, parent_event=self._ctx.get_parent()
        )
        return data

    def flush_queue(self):
        super().flush_queue()
        self.event_bus.publish(
            "huey.queue.flush", {}, parent_event=self._ctx.get_parent()
        )

    # Result/data store operations
    def put_data(self, key, value, is_result=False):
        super().put_data(key, value, is_result=is_result)
        self.event_bus.publish(
            "huey.data.put",
            {"key": key, "value": value, "is_result": is_result},
            parent_event=self._ctx.get_parent(),
        )

    def peek_data(self, key):
        val = super().peek_data(key)
        self.event_bus.publish(
            "huey.data.peek",
            {"key": key, "value": val},
            parent_event=self._ctx.get_parent(),
        )
        return val

    def pop_data(self, key):
        val = super().pop_data(key)
        self.event_bus.publish(
            "huey.data.pop",
            {"key": key, "value": val},
            parent_event=self._ctx.get_parent(),
        )
        return val

    def flush_results(self):
        super().flush_results()
        self.event_bus.publish(
            "huey.data.flush_results", {}, parent_event=self._ctx.get_parent()
        )


# 2) Pub/Sub Bus (from Eventure)

# 3) Tools and Registry (real tools)
import requests
from dataclasses import dataclass


def tool_echo(params: Dict[str, Any]) -> Dict[str, Any]:
    """Echo back the provided text. Useful for quick sanity checks or model-driven confirmations.
    Args: {"text": string}
    Returns: {"ok": boolean, "echo": string}
    """
    text = str(params.get("text", ""))
    return {"ok": True, "echo": text}


def tool_time(params: Dict[str, Any]) -> Dict[str, Any]:
    """Return current UTC time in ISO-8601 format.
    Args: {}
    Returns: {"ok": boolean, "utc": string}
    """
    now = datetime.now(timezone.utc).isoformat()
    return {"ok": True, "utc": now}


def tool_http_get(params: Dict[str, Any]) -> Dict[str, Any]:
    """HTTP GET a URL with optional headers and timeout.
    Args: {"url": string, "timeout"?: number, "headers"?: object}
    Returns: {"ok": boolean, "status"?: number, "headers"?: object, "text"?: string, "error"?: string}
    """
    url = params.get("url")
    if not url:
        return {"ok": False, "error": "missing url"}
    timeout = float(params.get("timeout", 10))
    headers = params.get("headers") or {}
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        return {
            "ok": True,
            "status": resp.status_code,
            "headers": dict(resp.headers),
            "text": resp.text[:2000],
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


@dataclass
class Tool:
    name: str
    func: Callable[[Dict[str, Any]], Dict[str, Any]]
    schema: Dict[str, Any]
    description: str


DEFAULT_TOOLS: Dict[str, Tool] = {
    "echo": Tool(
        name="echo",
        func=tool_echo,
        schema={
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
        description=(tool_echo.__doc__ or "").strip(),
    ),
    "time": Tool(
        name="time",
        func=tool_time,
        schema={"type": "object", "properties": {}},
        description=(tool_time.__doc__ or "").strip(),
    ),
    "http_get": Tool(
        name="http_get",
        func=tool_http_get,
        schema={
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "timeout": {"type": "number"},
                "headers": {"type": "object"},
            },
            "required": ["url"],
        },
        description=(tool_http_get.__doc__ or "").strip(),
    ),
}


# 4) Huey wiring
def build_huey(event_bus: EventBus, ctx: _EventContext) -> Huey:
    # Single-terminal mode: immediate=True executes tasks inline (no extra processes/threads)
    return Huey(
        name="agent-demo",
        immediate=True,
        immediate_use_memory=False,
        storage_class=EventureMemoryStorage,
        event_bus=event_bus,
        ctx=ctx,
    )


# 5) ToolExecutor: subscribes to actions, enqueues huey tasks, publishes observations
class ToolExecutor:
    def __init__(
        self,
        bus: EventBus,
        huey: Huey,
        tools: Optional[Dict[str, Tool]] = None,
        ctx: _EventContext | None = None,
    ) -> None:
        self.bus = bus
        self.huey = huey
        self.tools: Dict[str, Tool] = tools or dict(DEFAULT_TOOLS)
        self._actions: Dict[str, Any] = {}
        self._ctx = ctx or _EventContext()
        self._register()

    def _register(self) -> None:
        huey = self.huey
        bus = self.bus
        tools = self.tools
        actions = self._actions

        @huey.task()
        def run_tool(
            action_id: str, tool_name: str, parameters: Dict[str, Any]
        ) -> Dict[str, Any]:
            try:
                t = tools.get(tool_name)
                if not t:
                    raise ValueError(f"unknown tool: {tool_name}")
                result = t.func(parameters)
                parent = actions.pop(action_id, None)
                bus.publish(
                    "agent.observation",
                    {"id": action_id, "result": result},
                    parent_event=parent,
                )
                return result
            except Exception as e:
                bus.publish(
                    "agent.error",
                    {"type": "Error", "data": {"id": action_id, "message": str(e)}},
                )
                raise

        def on_action(event) -> None:
            data = event.data
            action_id = data.get("id")
            tool = data.get("tool")
            params = data.get("input", {})
            # Validate input; on invalid, publish error and skip queueing
            if (
                not action_id
                or not isinstance(action_id, str)
                or not tool
                or not isinstance(tool, str)
            ):
                bus.publish(
                    "agent.error",
                    {
                        "id": action_id,
                        "message": "invalid action payload (missing id/tool)",
                        "payload": data,
                    },
                )
                return
            # Remember parent event for causality linking
            actions[action_id] = event
            # Set context parent so storage-published huey.* events link appropriately
            self._ctx.set_parent(event)
            try:
                run_tool(action_id, tool, params)  # enqueue; immediate executes inline
            finally:
                self._ctx.clear()

        bus.subscribe("agent.action", on_action)

    def register(
        self,
        name: str,
        fn: Callable[[Dict[str, Any]], Dict[str, Any]],
        schema: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None,
    ) -> None:
        self.tools[name] = Tool(
            name=name,
            func=fn,
            schema=schema or {"type": "object", "properties": {}},
            description=(description or fn.__doc__ or "").strip(),
        )


# 6) Agent abstraction with ReACT + Pub/Sub
class Agent:
    def __init__(
        self, model: str, client: OpenAI, bus: EventBus, executor: ToolExecutor
    ) -> None:
        self.model = model
        self.client = client
        self.bus = bus
        self.executor = executor
        self.history: List[Dict[str, str]] = []
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        header = (
            "You are an AI assistant with access to tools. Always respond using the ReACT format exactly.\n\n"
            "Format (exactly these labels on separate lines):\n"
            "Thought: <your reasoning>\n"
            "Action: <tool name>\n"
            "Action Input: <json arguments>\n"
            "Observation: <will be provided>\n"
            "... (repeat Thought/Action/Action Input/Observation as needed) ...\n"
            "Final Answer: <your final answer>\n\n"
            "Rules:\n"
            "- If you need any external info or to print text, you MUST use a tool.\n"
            "- Never output empty responses. Always include either an Action or a Final Answer.\n"
            "- Action Input must be valid JSON matching the tool schema.\n\n"
            "Available tools:\n"
        )
        tool_parts: List[str] = []
        for name, tool in self.executor.tools.items():
            tool_parts.append(
                f"- {name}:\n  Description: {tool.description}\n  Schema: {json.dumps(tool.schema, ensure_ascii=False)}"
            )
        few_shot = (
            "\nExample 1 (echo):\n"
            "Thought: I should output an encouraging message using echo.\n"
            "Action: echo\n"
            'Action Input: {"text": "You can do it!"}\n'
            'Observation: {"ok": true, "echo": "You can do it!"}\n'
            "Final Answer: Sent an encouraging message.\n\n"
            "Example 2 (http_get):\n"
            "Thought: I will fetch the status code of a URL.\n"
            "Action: http_get\n"
            'Action Input: {"url": "https://httpbin.org/get"}\n'
            'Observation: {"ok": true, "status": 200, ...}\n'
            "Final Answer: The status code is 200.\n\n"
        )
        return header + "\n".join(tool_parts) + few_shot

    def _extract_tool_call(self, text: str) -> Optional[Dict[str, Any]]:
        tool = None
        params: Dict[str, Any] = {}
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("Action:"):
                tool = line[len("Action:") :].strip()
            elif line.startswith("Action Input:"):
                payload = line[len("Action Input:") :].strip()
                try:
                    params = json.loads(payload)
                except Exception:
                    params = {"raw": payload}
        if tool:
            return {"tool": tool, "parameters": params}
        return None

    def chat(self, message: str) -> str:
        self.history.append({"role": "user", "content": message})
        # Advance tick at the start of each user turn
        self.bus.event_log.advance_tick()
        self.bus.publish("user.input", {"message": message})

        while True:
            messages = [
                {"role": "system", "content": self.system_prompt}
            ] + self.history
            self.bus.publish("agent.thought", {"content": "Planning..."})

            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore[arg-type]
                temperature=0.2,
                max_tokens=600,
            )
            assistant_message = resp.choices[0].message.content or ""
            if not assistant_message.strip():
                # Nudge: enforce non-empty output
                self.bus.publish(
                    "agent.error", {"id": None, "message": "empty model response"}
                )
            self.history.append({"role": "assistant", "content": assistant_message})
            self.bus.publish(
                "agent.thought",
                {"content": assistant_message},
            )

            tool_call = self._extract_tool_call(assistant_message)
            if tool_call:
                action_id = str(uuid.uuid4())
                tool_name = tool_call["tool"]
                parameters = tool_call["parameters"]

                # Waiter for observation via pub/sub
                done = threading.Event()
                obs_payload: Dict[str, Any] = {}

                def on_observation(event) -> None:
                    data = event.data
                    if data.get("id") == action_id:
                        obs_payload.update(data)
                        done.set()

                unsubscribe = self.bus.subscribe("agent.observation", on_observation)

                # Publish action
                self.bus.publish(
                    "agent.action",
                    {
                        "id": action_id,
                        "tool": tool_name,
                        "input": parameters,
                    },
                )

                # Wait (with timeout) for observation
                done.wait(timeout=30)
                unsubscribe()

                if not obs_payload:
                    error_msg = f"Tool '{tool_name}' timed out"
                    self.history.append(
                        {
                            "role": "user",
                            "content": f'Observation: {{"ok": false, "error": "{error_msg}"}}',
                        }
                    )
                    continue

                observation = json.dumps(
                    obs_payload.get("result", {}), ensure_ascii=False
                )
                self.history.append(
                    {"role": "user", "content": f"Observation: {observation}"}
                )
                # Advance tick after each observation
                self.bus.event_log.advance_tick()
                continue
            else:
                # If no tool call and no Final Answer, nudge once then retry
                if "Final Answer:" not in assistant_message:
                    self.history.append(
                        {
                            "role": "user",
                            "content": "Observation: Please follow the ReACT format exactly and provide either an Action or a Final Answer.",
                        }
                    )
                    continue
                # End of ReACT: return final answer
                return assistant_message


def build_client_and_model() -> tuple[OpenAI, str]:
    if os.getenv("OPENROUTER_API_KEY"):
        client = OpenAI(
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            api_key=os.environ["OPENROUTER_API_KEY"],
        )
        model = os.getenv("OPENROUTER_MODEL", "openrouter/auto")
    else:
        client = OpenAI()
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return client, model


def main() -> None:
    event_log = EventLog()
    bus = EventBus(event_log)
    ctx = _EventContext()
    huey = build_huey(bus, ctx)

    # Renderer
    renderer = EventRenderer()
    bus.subscribe("*", renderer.print_event)

    # Start ToolExecutor (subscribes to actions and enqueues huey tasks)
    executor = ToolExecutor(bus=bus, huey=huey, ctx=ctx)

    client, model = build_client_and_model()
    agent = Agent(model=model, client=client, bus=bus, executor=executor)

    print("=== agent.has.no.secret (ReACT + PubSub + Huey + Eventure) ===")
    prompt = (
        "Use the tool echo to output an encouraging message, then use http_get to fetch https://httpbin.org/get status. "
        "Strictly follow: Thought/Action/Action Input/Observation/Final Answer."
    )
    answer = agent.chat(prompt)
    # Pretty final answer
    renderer = EventRenderer()
    renderer.print_final(answer)

    # Pretty cascade viewer
    renderer.print_cascade(event_log.events)


if __name__ == "__main__":
    # Ensure .env is loaded before checking keys
    load_dotenv()
    if not (os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")):
        print(
            "Please set OPENROUTER_API_KEY (preferred) or OPENAI_API_KEY before running."
        )
        raise SystemExit(1)
    main()
