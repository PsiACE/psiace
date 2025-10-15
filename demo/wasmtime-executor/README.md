# WASMTIME Executor for CodeAgent

A secure Python code executor for [smolagents](https://github.com/huggingface/smolagents) that uses WASMTIME WebAssembly runtime with the real `python.wasm` binary to provide strong isolation guarantees.

## Usage

You can use it as a drop-in replacement for the built-in `PythonExecutor` in `smolagents`. The example is in `examples/smolagents_wasmtime.py`.

```python
from wasmtime_executor import WasmtimePythonExecutor

from smolagents import CodeAgent, InferenceClientModel
from smolagents.local_python_executor import PythonExecutor


class WasmtimeCodeAgent(CodeAgent):
    """
    Custom CodeAgent that uses WasmtimePythonExecutor for code execution.

    This agent extends the standard CodeAgent to support WASMTIME-based
    WebAssembly execution for enhanced security and isolation.
    """

    def create_python_executor(self) -> PythonExecutor:
        """Override to use WasmtimePythonExecutor instead of built-in executors."""
        return WasmtimePythonExecutor(
            additional_authorized_imports=self.additional_authorized_imports,
            max_print_outputs_length=self.max_print_outputs_length,
            **self.executor_kwargs,
        )


def main():
    model = InferenceClientModel()

    additional_authorized_imports = ["math", "json"]
    max_print_outputs_length = 1000

    agent = WasmtimeCodeAgent(
        tools=[],
        model=model,
        additional_authorized_imports=additional_authorized_imports,
        max_print_outputs_length=max_print_outputs_length,
    )

    output = agent.run("Calculate the square root of 125 and explain the result.")
    print("WASMTIME executor result:", output)
```

## Acknowledgments

- [smolagents](https://github.com/huggingface/smolagents) for the agent framework
- [WASMTIME](https://wasmtime.dev/) for the WebAssembly runtime
- [VMware WebAssembly Language Runtimes](https://github.com/vmware-labs/webassembly-language-runtimes) for the Python WASM binary
