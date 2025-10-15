"""
WASMTIME-based Python code executor for smolagents.

This package provides a sandboxed Python execution environment using WASMTIME
WebAssembly runtime with the real python.wasm binary for strong isolation guarantees.
"""

from .executor import WasmtimePythonExecutor

__version__ = "0.1.0"
__all__ = ["WasmtimePythonExecutor"]
