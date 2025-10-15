+++
title = "用 WebAssembly 给代码智能体套上安全带"
description = "周末写的一个 Wasmtime Python 执行器：让代码智能体在本地沙箱里跑起来，又安全又可控。"
date = 2025-07-08
slug = "wasmtime-executor-for-code-agents"

draft = false

[taxonomies]
tags = ["AI", "WebAssembly", "Security", "Code Agents", "Sandbox"]

[extra]
lang = "zh"
+++

## 背景：代码智能体的“勇敢”行为

第一次让 AI 智能体执行代码，不到五分钟它就尝试扫 `/etc/passwd`、安装莫名其妙的包、跑无限循环。要让这种系统可用，第一件事就是控制执行环境。

Hugging Face 的 [smolagents](https://github.com/huggingface/smolagents) 已经提供了远程执行、Deno + Pyodide 等多种方案，但我想要一个**纯本地、易嵌入**的执行器，于是有了这个 Wasmtime Python Executor。

## 为什么选 WebAssembly

- **能力最小化**：WASM 默认没有文件、网络、系统访问，授权什么才有什么。
- **资源计量**：可以限制 CPU、内存、运行时间。
- **可移植**：今天跑 Python，明天换 JS、Ruby 也能适配。
- **确定性**：相同输入输出一致，方便调试和审计。

## 周末作品长这样

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

print(agent.run("Calculate the square root of 125"))
```

做法：

1. 使用 VMware 提供的 Python WASM 发行版；
2. 借助 `wasmtime-py` 在本地加载；
3. 实现 smolagents 期望的执行器接口；
4. 支持白名单 import、输出截断、状态持久化等基础功能。

## 优缺点一览

| 项目 | 现在就能用的 | 需要改进的 |
| --- | --- | --- |
| 兼容性 | 可直接接入 smolagents，接口一致 | Python 生态受限，缺包需要自己打 | 
| 安全性 | 默认隔离，权限收敛 | 还缺更精细的文件/网络授权策略 |
| 体验 | 完全本地、无外部依赖，错误信息清晰 | 长时间运行性能一般，镜像下载稍麻烦 |

## 能不能直接上生产？

暂时不行，这是个 weekend hack。但它验证了这个思路：

- WebAssembly 可以成为代码智能体的“安全带”；
- 不需要引入 Deno、远程服务，也能实现沙箱；
- 可以把现有 Agent 框架的执行端换成 Wasmtime，安全性和可控性都会提升。

如果要投入生产，需要：

- 更完善的资源配额与杀死策略；
- 包管理/缓存机制；
- 日志、审计链路；
- 安全审查和长时间压力测试。

## 代码与资料

- Demo 仓库：[psiace/demo/wasmtime-executor](https://github.com/psiace/psiace/tree/main/demo/wasmtime-executor)
- 参考项目：[smolagents](https://github.com/huggingface/smolagents)、[VMware WASM Runtimes](https://github.com/vmware-labs/webassembly-language-runtimes)
- 灵感来源：Simon Willison 的 [WASM Python Sandbox](https://til.simonwillison.net/webassembly/python-in-a-wasm-sandbox)

如果你也在思考“让 AI 安全执行代码”的方案，不妨先写一个属于你的沙箱。造轮子是理解问题最快的方式。
