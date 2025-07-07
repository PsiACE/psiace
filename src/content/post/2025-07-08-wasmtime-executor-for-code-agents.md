---
title: "Sandboxed Python executor for AI agents using WebAssembly"
description: "A weekend hack to explore different sandboxing approaches for Code Agents, using wasmtime-py and VMware's Python WASM binary to run Python code locally. Works with smolagents."
publishDate: 2025-07-08
tags: ["AI", "WebAssembly", "Security", "Code Agents", "Sandbox"]
draft: false
---

AI agents that execute code are powerful but terrifying. Within minutes of testing my first code agent, it was trying to install packages and access environment variables I never intended. **We need sandboxing.**

## The Problem

Code-executing AI agents can do amazing things—analyze data, solve math problems, debug code. But they also operate with zero fear of breaking production systems.

Consider these scenarios:

- **The curious agent**: "Let me check what's in `/etc/passwd`..."
- **The helpful agent**: "I'll install this package" → `pip install` from compromised PyPI
- **The infinite loop**: Code that consumes all available memory

Some projects like [Hugging Face smolagents](https://github.com/huggingface/smolagents/blob/main/src/smolagents/remote_executors.py) recognize this—they built multiple executor options to balance capability and security.

## Why WebAssembly?

WebAssembly's superpower isn't speed—it's **security by design**. Born from browser security, WASM provides:

1. **Capability-based security**: Can't do anything unless explicitly granted
2. **Resource metering**: Count every CPU cycle and memory allocation
3. **Deterministic execution**: Same code, same result every time
4. **Language agnostic**: Python today, others tomorrow

Simon Willison explored this in his [TIL post](https://til.simonwillison.net/webassembly/python-in-a-wasm-sandbox), and [Hacker News discussed it](https://news.ycombinator.com/item?id=34581487). While [Hugging Face smolagents](https://github.com/huggingface/smolagents) already has a `WasmExecutor` using Pyodide and Deno, I wanted to explore a different approach using wasmtime for local execution.

## A Weekend Hack

So I built one. Nothing fancy—just a **"just do it"** demo:

```python
from wasmtime_executor import WasmtimePythonExecutor
from smolagents import CodeAgent, InferenceClientModel

class WasmtimeCodeAgent(CodeAgent):
    def create_python_executor(self):
        return WasmtimePythonExecutor(
            additional_authorized_imports=self.additional_authorized_imports,
            max_print_outputs_length=self.max_print_outputs_length,
            **self.executor_kwargs,
        )

agent = WasmtimeCodeAgent(
    tools=[],
    model=InferenceClientModel(),
    additional_authorized_imports=["math", "json"],
)

result = agent.run("Calculate the square root of 125")
```

Implementation: grab VMware's Python WASM binary, wrap with wasmtime-py, make it compatible with smolagents. The key difference? **Local execution** without needing Deno runtime.

## What I Learned

**What worked:**

- Drop-in compatibility with smolagents
- Basic Python operations run fine
- Error handling is robust
- State persists between executions
- **Local execution** without external dependencies

**Trade-offs:**

- Real isolation vs. limited Python ecosystem
- Better security vs. worse performance
- Deterministic vs. complex setup
- **Local control** vs. remote calls

## Is This Production Ready?

**Absolutely not.** This is a weekend hack. But it proves the approach works.

For production you'd need: better resource management, package management, performance optimization, proper logging, security auditing.

But for experimenting? Understanding trade-offs? Having a concrete example? It works perfectly.

## The Point

The real value isn't this specific implementation—it's demonstrating that **different sandboxing approaches exist for AI code execution**. While smolagents offers Pyodide-based sandboxing with Deno, wasmtime provides an alternative for local execution. You can take an existing agent framework, add security boundaries, maintain functionality, and explore different trade-offs.

## Try It

The complete implementation is in my [Wasmtime Executor demo](https://github.com/psiace/psiace/tree/main/demo/wasmtime-executor). It's rough but works. Clone it, break it, improve it.

The best way to understand these security challenges is to build something. Even if it's just a quick weekend hack.

---

## References

- [Hugging Face smolagents](https://github.com/huggingface/smolagents)
- [Wasmtime Executor Demo](https://github.com/psiace/psiace/tree/main/demo/wasmtime-executor)
- [Simon Willison's WASM Python Sandbox](https://til.simonwillison.net/webassembly/python-in-a-wasm-sandbox)
- [VMware WebAssembly Language Runtimes](https://github.com/vmware-labs/webassembly-language-runtimes)
