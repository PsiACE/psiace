#!/usr/bin/env python3
"""
Basic usage example for WasmtimePythonExecutor.

This example demonstrates how to use the WasmtimePythonExecutor to run Python code
in a sandboxed WASM environment.
"""

from wasmtime_executor import WasmtimePythonExecutor


def main():
    """Demonstrate basic usage of WasmtimePythonExecutor."""
    print("=== WasmtimePythonExecutor Basic Usage Demo ===\n")

    # Create the executor with additional authorized imports
    executor = WasmtimePythonExecutor(
        additional_authorized_imports=["math", "json", "random"],
        max_print_outputs_length=1000,
    )

    # Test 1: Simple arithmetic
    print("1. Testing simple arithmetic:")
    result = executor("print(2 + 3 * 4)")
    print(f"   Output: {result[0]}")
    print(f"   Logs: {result[1]}")
    print(f"   Is final answer: {result[2]}")
    print()

    # Test 2: Math operations (testing authorized imports)
    print("2. Testing math operations:")
    result = executor("""
import math
result = math.sqrt(16) + math.pi
print(f"sqrt(16) + pi = {result}")
""")
    print(f"   Output: {result[0]}")
    print(f"   Logs: {result[1]}")
    print(f"   Is final answer: {result[2]}")
    print()

    # Test 3: Random operations (testing additional authorized imports)
    print("3. Testing random operations:")
    result = executor("""
import random
random.seed(42)
numbers = [random.randint(1, 10) for _ in range(5)]
print(f"Random numbers: {numbers}")
""")
    print(f"   Output: {result[0]}")
    print(f"   Logs: {result[1]}")
    print(f"   Is final answer: {result[2]}")
    print()

    # Test 4: String operations
    print("4. Testing string operations:")
    result = executor("""
text = "Hello, WASM World!"
print(text.upper())
print(f"Length: {len(text)}")
""")
    print(f"   Output: {result[0]}")
    print(f"   Logs: {result[1]}")
    print(f"   Is final answer: {result[2]}")
    print()

    # Test 5: List operations
    print("5. Testing list operations:")
    result = executor("""
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print(f"Original: {numbers}")
print(f"Squares: {squares}")
print(f"Sum of squares: {sum(squares)}")
""")
    print(f"   Output: {result[0]}")
    print(f"   Logs: {result[1]}")
    print(f"   Is final answer: {result[2]}")
    print()

    # Test 6: Error handling
    print("6. Testing error handling:")
    result = executor("""
try:
    result = 1 / 0
except ZeroDivisionError as e:
    print(f"Caught error: {e}")
""")
    print(f"   Output: {result[0]}")
    print(f"   Logs: {result[1]}")
    print(f"   Is final answer: {result[2]}")
    print()

    # Test 7: Final answer functionality
    print("7. Testing final answer functionality:")

    # Add a mock final_answer tool
    def mock_final_answer(answer):
        return f"Final nswer: {answer}"

    executor.send_tools({"final_answer": mock_final_answer})

    result = executor("""
import math
result = math.sqrt(125)
final_answer(f"The square root of 125 is approximately {result:.2f}")
""")
    print(f"   Output: {result[0]}")
    print(f"   Logs: {result[1]}")
    print(f"   Is final answer: {result[2]}")
    print()

    print("=== Demo completed ===")


if __name__ == "__main__":
    main()
