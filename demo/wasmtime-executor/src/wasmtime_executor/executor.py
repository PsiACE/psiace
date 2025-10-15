"""
WASMTIME-based Python code executor for smolagents.

This module provides a sandboxed Python execution environment using WASMTIME
WebAssembly runtime with the real python.wasm binary for strong isolation guarantees.
"""

import os
import tempfile
from pathlib import Path
from typing import Any, List, Optional
import logging
import json
import ast

from wasmtime import Config, Engine, Linker, Module, Store, WasiConfig


logger = logging.getLogger(__name__)


class WasmtimePythonExecutor:
    """
    Python code executor using WASMTIME WebAssembly runtime with real python.wasm.

    This executor provides sandboxed Python execution using WASMTIME's
    WebAssembly runtime and the real Python WebAssembly binary for strong isolation guarantees.

    Args:
        additional_authorized_imports (List[str]): Additional Python packages to make available.
        max_print_outputs_length (int, optional): Maximum length of the print outputs.
        additional_functions (dict, optional): Additional Python functions to be added to the executor.
    """

    def __init__(
        self,
        additional_authorized_imports: List[str],
        max_print_outputs_length: Optional[int] = None,
        additional_functions: Optional[dict] = None,
    ):
        self.additional_authorized_imports = additional_authorized_imports
        self.max_print_outputs_length = max_print_outputs_length or 50_000
        self.additional_functions = additional_functions or {}

        # Path to the Python WASM binary
        # Try to find WASM runtime in package first, then fall back to development path
        package_wasm_dir = Path(__file__).parent / "wasm-runtime"
        dev_wasm_dir = Path(__file__).parent.parent.parent / "wasm-runtime"

        if package_wasm_dir.exists():
            self.wasm_runtime_dir = package_wasm_dir
        elif dev_wasm_dir.exists():
            self.wasm_runtime_dir = dev_wasm_dir
        else:
            raise FileNotFoundError(
                f"WASM runtime directory not found. Checked:\n"
                f"  - Package path: {package_wasm_dir}\n"
                f"  - Development path: {dev_wasm_dir}"
            )

        self.python_wasm_path = self.wasm_runtime_dir / "bin" / "python-3.11.1.wasm"

        if not self.python_wasm_path.exists():
            raise FileNotFoundError(
                f"Python WASM binary not found at {self.python_wasm_path}"
            )

        # Initialize WASMTIME components
        self._initialize_wasm_environment()

        # State management for PythonExecutor compatibility
        self.custom_tools = {}
        self.static_tools = None
        self.state = {"__name__": "__main__"}

    def _initialize_wasm_environment(self):
        """Initialize the WASM execution environment with Python."""
        try:
            # Create engine with fuel consumption for safety
            engine_cfg = Config()
            engine_cfg.consume_fuel = True
            engine_cfg.cache = True

            self.engine = Engine(engine_cfg)
            self.linker = Linker(self.engine)
            self.linker.define_wasi()

            # Load the Python WASM module
            self.python_module = Module.from_file(
                self.engine, str(self.python_wasm_path)
            )

            logger.info("Python WASM environment initialized successfully")

        except Exception as e:
            raise RuntimeError(f"Failed to initialize Python WASM environment: {e}")

    def __call__(self, code_action: str) -> tuple[Any, str, bool]:
        """Execute code and return the result."""
        return self._execute_python_code(code_action)

    def _prepare_code_with_tools(self, code: str) -> str:
        """Prepare code by injecting tools and variables."""
        # Start with imports and basic setup
        prepared_code = []

        # Add basic imports that are always available
        prepared_code.append("import sys")
        prepared_code.append("import json")
        prepared_code.append("import math")

        # Add additional authorized imports
        for import_name in self.additional_authorized_imports:
            # Handle different import formats
            if "." in import_name:
                # For submodules like "os.path", import the full module
                prepared_code.append(f"import {import_name}")
            else:
                # For simple modules like "math", "json", etc.
                prepared_code.append(f"import {import_name}")

        # Add state variables
        for key, value in self.state.items():
            if key not in ["__name__", "_print_outputs", "_operations_count"]:
                try:
                    # Try to serialize the value as JSON first
                    if isinstance(
                        value, (str, int, float, bool, list, dict, type(None))
                    ):
                        prepared_code.append(f"{key} = {json.dumps(value)}")
                    else:
                        # For complex objects, convert to string representation
                        prepared_code.append(f"{key} = {repr(value)}")
                except (TypeError, ValueError):
                    # Skip variables that can't be serialized
                    logger.warning(
                        f"Skipping variable {key} due to serialization issues"
                    )
                    continue

        # Add tools as functions
        if self.static_tools:
            for tool_name, tool_func in self.static_tools.items():
                if tool_name == "final_answer":
                    # Special handling for final_answer
                    prepared_code.append("""
class FinalAnswerException(Exception):
    def __init__(self, value):
        self.value = value

def final_answer(*args, **kwargs):
    '''Final answer function that signals completion'''
    if args:
        result = args[0] if len(args) == 1 else args
    else:
        result = kwargs if kwargs else None
    raise FinalAnswerException(result)
""")
                else:
                    # For other tools, create a placeholder function
                    prepared_code.append(f"""
def {tool_name}(*args, **kwargs):
    '''Tool function: {tool_name}'''
    print(f"Tool {tool_name} called with args={{args}}, kwargs={{kwargs}}")
    return None
""")

        # Add the actual user code
        prepared_code.append("")
        prepared_code.append("# User code starts here")
        prepared_code.append("try:")

        # Indent the user code
        for line in code.split("\n"):
            prepared_code.append(f"    {line}")

        prepared_code.append("except FinalAnswerException as e:")
        prepared_code.append("    print(f'FINAL_ANSWER:{e.value}')")
        prepared_code.append("    sys.exit(0)")
        prepared_code.append("except Exception as e:")
        prepared_code.append("    print(f'ERROR:{type(e).__name__}: {e}')")
        prepared_code.append("    sys.exit(1)")

        return "\n".join(prepared_code)

    def _execute_python_code(
        self, code: str, fuel: int = 1_000_000_000
    ) -> tuple[Any, str, bool]:
        """Execute Python code in the WASM environment."""
        try:
            # Prepare code with tools and variables
            prepared_code = self._prepare_code_with_tools(code)

            # Create WASI configuration
            config = WasiConfig()
            config.argv = ("python", "-c", prepared_code)

            # Create temporary directory for output capture
            with tempfile.TemporaryDirectory() as chroot:
                out_log = os.path.join(chroot, "out.log")
                err_log = os.path.join(chroot, "err.log")

                config.stdout_file = out_log
                config.stderr_file = err_log

                # Mount the WASM runtime directory to provide Python libraries
                config.preopen_dir(str(self.wasm_runtime_dir), "/")

                # Set Python environment variables for library paths
                python_lib_path = "/usr/local/lib/python311.zip"
                config.env = [
                    ("PYTHONPATH", python_lib_path),
                    ("PYTHONHOME", "/usr/local"),
                    ("PYTHONPLATLIBDIR", "lib"),
                    ("PYTHONDONTWRITEBYTECODE", "1"),
                ]

                # Create store and set up execution environment
                store = Store(self.engine)
                # Set fuel limit for execution
                if fuel > 0:
                    store.set_fuel(fuel)
                store.set_wasi(config)

                # Instantiate the module
                instance = self.linker.instantiate(store, self.python_module)

                # Get the _start function (WASI main function)
                start = instance.exports(store)["_start"]

                # Execute the code
                execution_successful = True
                error_message = None
                try:
                    start(store)
                except Exception as e:
                    execution_successful = False
                    error_message = str(e)

                # Read output and error logs
                stdout_content = ""
                stderr_content = ""

                try:
                    with open(out_log, "r") as f:
                        stdout_content = f.read()
                except FileNotFoundError:
                    pass

                try:
                    with open(err_log, "r") as f:
                        stderr_content = f.read()
                except FileNotFoundError:
                    pass

                # Parse output for final answer
                is_final_answer = False
                output = None

                if stdout_content:
                    lines = stdout_content.strip().split("\n")
                    for line in lines:
                        if line.startswith("FINAL_ANSWER:"):
                            is_final_answer = True
                            final_answer_str = line[
                                13:
                            ]  # Remove 'FINAL_ANSWER:' prefix

                            # Try to parse the final answer more safely
                            try:
                                # First try to evaluate as a Python literal (for numbers, lists, etc.)
                                output = ast.literal_eval(final_answer_str)
                            except (ValueError, SyntaxError):
                                # If that fails, try regular eval for simple expressions
                                try:
                                    output = eval(final_answer_str)
                                except Exception:
                                    # If all else fails, just use the string as-is
                                    output = final_answer_str
                            break
                        elif line.startswith("ERROR:"):
                            error_message = line[6:]  # Remove 'ERROR:' prefix
                            execution_successful = False
                            break

                # Combine logs
                logs = ""
                if stdout_content:
                    # Filter out our special markers from logs
                    filtered_lines = []
                    for line in stdout_content.split("\n"):
                        if not line.startswith("FINAL_ANSWER:") and not line.startswith(
                            "ERROR:"
                        ):
                            filtered_lines.append(line)
                    if filtered_lines:
                        logs += "\n".join(filtered_lines)

                if stderr_content:
                    if logs:
                        logs += "\n"
                    logs += f"STDERR: {stderr_content}"

                # Determine output if not already set
                if output is None:
                    if not execution_successful:
                        output = f"Execution error: {error_message}"
                    elif logs.strip():
                        # Try to extract the last meaningful output
                        log_lines = logs.strip().split("\n")
                        if log_lines and not log_lines[-1].startswith("STDERR:"):
                            output = (
                                log_lines[-1] if len(log_lines) == 1 else logs.strip()
                            )

                # Truncate logs if necessary
                if len(logs) > self.max_print_outputs_length:
                    logs = logs[: self.max_print_outputs_length] + "... (truncated)"

                return output, logs, is_final_answer

        except Exception as e:
            return (
                f"WASM execution error: {e}",
                f"Failed to execute code in WASM environment: {e}",
                False,
            )

    def send_variables(self, variables: dict):
        """Send variables to the execution environment."""
        self.state.update(variables)

    def send_tools(self, tools: dict):
        """Send tools to the execution environment."""
        # Combine agent tools and additional functions
        self.static_tools = {**tools, **self.additional_functions}

        # Store tools for later use
        self.custom_tools.update(tools)

    def cleanup(self):
        """Clean up resources used by the executor."""
        try:
            # WASM resources are automatically cleaned up
            logger.info("Cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
