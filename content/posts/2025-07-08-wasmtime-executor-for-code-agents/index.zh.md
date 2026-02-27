+++
title = "用 WebAssembly 为 Code Agent 范式构建安全沙箱"
description = "周末写的一个 Wasmtime Python 执行器：让代码智能体在本地沙箱里跑起来，又安全又可控。"
date = 2025-07-08
slug = "wasmtime-executor-for-code-agents"

draft = false

[taxonomies]
tags = ["AI", "WebAssembly", "Security", "Code Agents", "Sandbox"]

[extra]
lang = "zh"
+++

Code Agent（代码代理范式）的能力令人惊叹，但安全性问题同样令人担忧。在我测试第一个 Code Agent 时，它很快就尝试安装包、访问环境变量，甚至想要读取系统文件。**我们需要一个真正安全的执行环境。**

## 安全挑战

代码执行型 AI 代理（Code Agent 范式）确实能完成很多任务——数据分析、数学计算、代码调试。但它们缺乏对系统边界的认知，可能带来严重的安全风险。

典型的安全威胁场景：

- **权限越界**：尝试访问 `/etc/passwd`、系统环境变量
- **恶意包安装**：从被污染的 PyPI 源安装恶意包
- **资源耗尽**：无限循环、内存泄漏导致系统崩溃
- **网络攻击**：发起 DDoS、端口扫描等恶意行为

像 [Hugging Face smolagents](https://github.com/huggingface/smolagents/blob/main/src/smolagents/remote_executors.py) 之类的项目已经意识到了这个问题，提供了多种执行器选项来平衡功能性和安全性。

## WebAssembly 的安全优势

WebAssembly 的核心价值不在于性能，而在于**原生安全设计**。作为从浏览器安全模型发展而来的技术，WASM 提供了：

1. **能力安全模型**：基于最小权限原则，只能访问明确授权的资源
2. **细粒度资源控制**：精确监控 CPU 使用、内存分配、网络访问
3. **执行确定性**：相同的输入总是产生相同的输出，便于审计
4. **语言无关性**：支持多种编程语言的安全执行

Simon Willison 在他的 [TIL 文章](https://til.simonwillison.net/webassembly/python-in-a-wasm-sandbox) 中详细探讨了这个方案，[Hacker News 社区也有深入讨论](https://news.ycombinator.com/item?id=34581487)。

虽然 [Hugging Face smolagents](https://github.com/huggingface/smolagents) 已经提供了基于 Pyodide 和 Deno 的 `WasmExecutor`，但我想探索一个基于 wasmtime 的本地执行方案，看看有什么不同的技术权衡。

## 技术实现

基于 wasmtime-py 和 VMware 的 Python WASM 运行时，我实现了一个简单的沙箱执行器：

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

核心实现思路：利用 VMware 提供的 Python WASM 二进制文件，通过 wasmtime-py 进行运行时管理，并实现与 smolagents 的兼容层。关键的技术差异在于**本地执行**，避免了对外部 Deno 运行时的依赖。


## 技术评估

**优势方面：**

- 与 smolagents 框架的无缝集成
- 基础 Python 操作的良好支持
- 完善的错误处理和异常捕获
- 执行状态的有效隔离和持久化
- **本地化部署**，减少网络依赖

**技术权衡：**

- 安全隔离 vs Python 生态系统限制
- 执行安全性 vs 性能开销
- 确定性执行 vs 配置复杂性
- **本地控制** vs 远程服务调用

## 生产就绪性

**当前状态：实验性项目**。这个实现主要用于概念验证和技术探索。

生产环境部署需要解决的关键问题：

- 资源限制和配额管理
- 包依赖管理和安全扫描
- 性能优化和缓存策略
- 完整的审计日志和监控
- 安全漏洞的持续评估

但对于技术研究、原型验证、理解安全边界？这个实现提供了很好的起点。

## 技术价值

这个项目的真正价值不在于具体的实现代码，而在于证明了**Code Agent 范式存在多种安全沙箱方案**。虽然 smolagents 提供了基于 Pyodide 的 Deno 沙箱，wasmtime 为本地执行提供了另一种技术选择。开发者可以基于现有的代理框架，添加安全边界，保持功能完整性，同时探索不同的技术权衡。

## 进一步探索

完整的实现代码和详细文档在我的 [Wasmtime 执行器项目](https://github.com/psiace/psiace/tree/main/demo/wasmtime-executor) 中。代码虽然粗糙，但功能完整。欢迎克隆、测试、改进。

理解 Code Agent 范式安全挑战的最佳方式就是动手实践。即使是简单的概念验证项目，也能带来深刻的技术洞察。

---

## 参考资料

- [Hugging Face smolagents](https://github.com/huggingface/smolagents)
- [Wasmtime 执行器项目](https://github.com/psiace/psiace/tree/main/demo/wasmtime-executor)
- [Simon Willison 的 WASM Python 沙箱](https://til.simonwillison.net/webassembly/python-in-a-wasm-sandbox)
- [VMware WebAssembly 语言运行时](https://github.com/vmware-labs/webassembly-language-runtimes)
