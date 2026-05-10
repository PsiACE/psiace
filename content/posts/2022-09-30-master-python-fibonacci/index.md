+++
title = "I Will Always Hate Python Fibonacci"
description = "A walkthrough from different Fibonacci algorithms to extending Python with C/C++."
date = 2022-09-30
slug = "master-python-fibonacci"

[taxonomies]
tags = ["2022", "Python", "Notes"]

[extra]
lang = "en"
+++

This is PsiACE. It has been a long time since I last met everyone with a public report.

At the moment, I am in Macau. Overall, things are going fairly well. My cooking has improved rapidly recently, and I have had to pick up Python again after not writing it for a long time.

There are probably four ways to write the Chinese character "hui", and there are even more ways to write Python Fibonacci. Let us take a look.

This article mainly introduces two aspects. The first half focuses on different algorithmic implementations of Fibonacci, and the second half focuses on how to extend Fibonacci with C/C++ and similar tools.

## Different Algorithmic Implementations of Fibonacci

The [Fibonacci sequence](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Fibonacci%23Fibonacci_sequence) is named after the Italian mathematician `Leonardo Fibonacci`.

The Fibonacci sequence has many uses in computing, such as Fibonacci search, an improved form of binary search, and Fibonacci heaps.

### Recursion

According to the definition of Fibonacci, a recursive algorithm can be written easily:

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

### Memoization

A simple optimization idea is memoization. Since this is a recursive computation, saving previous results is helpful.

```python
def fib(n):
    @lru_cache()
    def fib(n):
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)
    return fib(n)
```

For further optimization, we can use an iterative algorithm, such as remembering all previous results. This is roughly linear.

```python
def fib(n):
    data = [0, 1]
    for i in range(n-1):
        data.append(data[-2] + data[-1])
    return data[n]
```

In fact, we do not need to record that many intermediate results. Keeping only the previous two values is enough:

```python
def fib(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a
```

### Mathematics

Going further, if we convert the recurrence relation into a closed-form formula, we get the following algorithm:

```python
def fib(n):
    sqrt5 = 5**0.5
    fibN = ((1 + sqrt5) / 2) ** n - ((1 - sqrt5) / 2) ** n
    return round(fibN / sqrt5)
```

This method is very fast, but integer overflow needs to be considered, so it is only effective for small data sizes. It is constant-level.

### Matrix Multiplication

Are there other methods? Matrix multiplication, for example, is roughly logarithmic:

```python
def fib(n):
    if n < 2:
        return n

    q = [[1, 1], [1, 0]]
    res = matrix_pow(q, n - 1)
    return res[0][0]

def matrix_pow(a, n):
    ret = [[1, 0], [0, 1]]
    while n > 0:
        if n & 1:
            ret = matrix_multiply(ret, a)
        n >>= 1
        a = matrix_multiply(a, a)
    return ret

def matrix_multiply(a, b):
    c = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            c[i][j] = a[i][0] * b[0][j] + a[i][1] * b[1][j]
    return c
```

## Extending Fibonacci with C / C++

A very typical view is that Python is a language suitable for beginners and rapid development, but it does not have a major performance advantage. Even at PyCon, [@gvanrossum](https://github.com/gvanrossum) said that Python's speed must be improved by 2x so that it can confront high-performance programming languages such as C++ head-on.

Clearly, there are known ways to improve performance, and they have been applied in mainstream data science packages and web framework packages.

- Reduce time complexity. Whatever makes the program slow, choose a faster algorithm directly whenever possible.
- Parallelize the code. If there are multiple idle processors, try splitting the task into subtasks that can be processed at the same time.
- Rewrite the slower parts of the code in a faster language.

The obvious benefits of extending Python with C / C++ are:

- On one hand, thanks to Python's simplicity and ease of use, we can provide a clear and simplified interface, reducing downstream developers' effort and accelerating application development.
- On the other hand, thanks to the performance and compiler optimization of other languages, program performance can be improved significantly.

### How to Extend Python with C / C++

**Using Python's ctypes module**

ctypes is the official FFI module provided by Python and is suitable for dynamic libraries. The complexity of handling calls is mostly shifted to Python, and it cannot make good use of some Python capabilities.

**Using Python CAPI**

CPython provides an API set for C / C++, allowing C / C++ to interact with Python using native Python capabilities. However, debugging still requires the C / C++ toolchain, and because it calls Python's low-level CAPI, manual manipulation of Python reference counts is sometimes required to work with Python's GC mechanism.

**Using Cython**

Cython is an optimized static compiler for Python and the Cython language. It translates Python and Cython into C/C++, then compiles that into a statically linked library for Python to use.

Besides providing CAPI, Cython also provides most wrapped modules and functions. For Unicode or Python's exception mechanism, Cython helps automatically translate them into C/C++. Since Cython is code translation with relatively coarse granularity, some fine-grained optimization is difficult.

**Using SWIG**

SWIG does not only provide C/C++ extensions for Python. It also supports extensions for Java, Perl, and other languages, meaning one extension can be used in multiple places.

The biggest advantage of SWIG is that the same code can extend multiple languages. However, for some features, Python-specific CAPI calls still need to be explicitly written in the configuration file. Debugging also still relies on the C/C++ toolchain.

### Examples and Performance

Let us return to the Fibonacci sequence. Earlier, we discussed its algorithms and some optimizations.

**Recursion**

In the following sections, we will use the recursive algorithm as the baseline to show different optimizations. Except for the parallel section, we will use `fib(47)` for performance evaluation.

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

**Parallelism**

By using multiprocessing pools, we can execute multiple computation tasks at the same time, which gives performance advantages in certain scenarios.

```python
import multiprocessing
import multiprocessing as mp

#function for calculate fibannaci number
def fib(n):
  if n <= 1: return 1
  return fib(n - 1) + fib(n - 2)

def parallel_fib(x):
    # paralleing throught pool.
    p = multiprocessing.Pool(mp.cpu_count())

    return p.map(fib, [x, x+1, x+2, x+3])

# One-time parallel calculation
print(parallel_fib(30))
# Recursive calculation one by one
print(fib(30), fib(31), fib(32), fib(33))
```

A quick look at performance:

| Language         | Time, s |
| ---------------- | ------- |
| Python Recursive | 1.377   |
| Python Parallel  | 0.669   |

**Fast Algorithm - Memoization**

The recursive algorithm is quite plain and very slow. We discussed faster algorithms earlier, and here is a simple algorithm that caches recent results.

```python
from functools import lru_cache

@lru_cache(3)
def fib(n):
  if n <= 1: return 1
  return fib(n - 1) + fib(n - 2)

print(fib(47))
```

**PyPy - JIT**

PyPy is an alternative to CPython. It is built with RPython, a language developed together with it. The main reason to use PyPy instead of CPython is speed: it usually runs faster.

PyPy implements Python 2.7.18 and 3.7.10. It supports the full core language, passes the Python 2.7 test suite and almost all of the 3.7 test suite, and supports most commonly used Python standard library modules.

The secret to PyPy's speed is JIT technology. These are the steps JIT compilation takes to improve performance:

- Identify the most commonly used components in the code, such as functions inside loops.
- Convert these components into machine code at runtime.
- Optimize the generated machine code.
- Replace the previous implementation with the optimized machine-code version.

Fortunately, our recursive version can naturally use PyPy compilation to gain performance improvements.

**C**

To demonstrate the capabilities of C/C++ extensions, we also provide a C version for comparison.

```c
#include <stdio.h>
#include <stdint.h>

static uint64_t fib(uint64_t n) {
  if (n <= 1) return n;
  return fib(n - 1) + fib(n - 2);
}

int main(void) {
  printf("%llu \n", fib(47));
  return 0;
}
```

**ctypes**

Similarly, following the previous C version, we write the corresponding shared library.

```c
%%file fib-share.h
#include <stdint.h>

uint64_t c_fib(uint64_t n);
```

```c
%%file fib-share.c

#include <stdint.h>

uint64_t c_fib(uint64_t n) {
  if (n <= 1) return n;
  return c_fib(n - 1) + c_fib(n - 2);
}
```

Next, let us use `ctypes` to call it. The main parts are simple. The important detail is that `uint64_t` corresponds to `c_ulonglong`, and we need to specify the argument type and return type.

```python
%%file fib-ctypes.py
from ctypes import CDLL, c_ulonglong

def ctypes_fib(n):

    # Use ctypes to load the library
    lib = CDLL('./ctypes_fib.so')

    # We need to give the argument and return types explicitly
    lib.c_fib.argtypes = [c_ulonglong]
    lib.c_fib.restype  = c_ulonglong

    return lib.c_fib(n)

print(ctypes_fib(47))
```

Then we need to compile the shared library and run it like any other Python program.

```bash
$ gcc -O3 -fPIC -shared -std=c99  fib-share.c -o ctypes_fib.so
$ python fib-ctypes.py
```

**CAPI**

Compared with the other methods, CAPI is more complex, so I would probably recommend reading [How to Write and Debug C Extension Modules](https://llllllllll.github.io/c-extension-tutorial/).

```c
#include <Python.h>

static unsigned long
cfib(unsigned long n)
{
  if (n <= 1) return n;
  return cfib(n - 1) + cfib(n - 2);
}

PyDoc_STRVAR(fib_doc, "compute the nth Fibonacci number");

static PyObject*
pyfib(PyObject* self, PyObject* n)
{
    unsigned long as_unsigned_long = PyLong_AsUnsignedLong(n);
    PyObject* result = PyLong_FromUnsignedLong(cfib(as_unsigned_long));
    return result;
}

PyMethodDef methods[] = {
    {"fib", (PyCFunction) pyfib, METH_O, fib_doc},
    {NULL},
};

PyDoc_STRVAR(fib_module_doc, "provides a Fibonacci function");

PyModuleDef fib_module = {
    PyModuleDef_HEAD_INIT,
    "fib",
    fib_module_doc,
    -1,
    methods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC
PyInit_fib(void)
{
    return PyModule_Create(&fib_module);
}
```

All function return types are pointers to PyObject, and the parameter types are two PyObject pointers. The first corresponds to `self` in a Python class method, and the second corresponds to the argument in the call.

After completing the function we need, we need to explicitly declare the methods exposed by the module, the accepted parameter types, and the documentation.

```python
from .fib import fib


__all__ = ['fib']
```

The most common way to build a CPython extension module is to use setuptools and a setup.py file. We start with a normal setuptools setup.py file:

```python
from setuptools import setup, find_packages, Extension


setup(
    name='fibcapi',
    version='0.1.0',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    ext_modules=[
        Extension(
            'fib.fib',
            ['fib/fib.c'],
        ),
    ],
)
```

Run the following command from the root directory:

```bash
python setup.py build_ext --inplace
```

Finally, call it like an ordinary Python program.

```python
import fib

print(fib.fib(47))
```

**Cython**

If using Cython, the code can be changed to:

```python
cdef long fib(long n):
  if n <= 1: return n
  return fib(n - 1) + fib(n - 2)

print(fib(47))
```

Use the following command to compile:

```bash
cython -3 --embed -o fib.pyx.c fib.pyx && gcc -O3 $(python3-config --embed --cflags) -o fib fib.pyx.c $(python3-config --embed --ldflags)
```

**SWIG**

First, let us reuse `fib-share.h` and `fib-share.c` from the ctypes section.

Next, define the corresponding SWIG interface file. To use `uint64_t`, we have to introduce `stdint.i`.

```c
%%file fib-swig.i
%include "stdint.i"

%module fibswig
%{
extern uint64_t c_fib(uint64_t n);
%}

extern uint64_t c_fib(uint64_t n);
```

Then we need to write a little Python code to call the swig shared library.

```python
import fibswig

print(fibswig.c_fib(47))
```

Next, we need to compile the shared library and execute it like any other Python program.

```bash
$ swig -python fib-swig.i
$ gcc -fPIC -c fib-share.c fib-swig_wrap.c -I /usr/include/python3.10
$ ld -fPIC -shared fib-share.o fib-swig_wrap.o -o _fibswig.so
$ python fib-swig.py
```

**Performance Summary**

| Lang           | Time, s |
| -------------- | ------- |
| Python3        | 530.974 |
| Python3 (PyPy) | 39.398  |
| Python - Cache | 0.013   |
| C              | 3.336   |
| ctypes         | 3.245   |
| CAPI           | 3.300   |
| Cython         | 4.487   |
| SWIG           | 13.368  |

## Acknowledgements

- [509. Fibonacci Number - LeetCode](https://leetcode.cn/problems/fibonacci-number/)
- [Extending Python with C or C++](https://docs.python.org/3/extending/extending.html)
- [`ctypes` — A foreign function library for Python](https://docs.python.org/3/library/ctypes.html)
- [Building a Python C Extension Module](https://realpython.com/build-python-c-extension-module/)
- [Write Your Own C-extension to Speed Up Python by 100x](https://towardsdatascience.com/write-your-own-c-extension-to-speed-up-python-x100-626bb9d166e7)
- [Extending Python with C](https://medium.com/delta-force/extending-python-with-c-f4e9656fbf5d)
- [Extending Python with C or C++ code](https://web.mit.edu/people/amliu/vrut/python/ext/intro.html)
- [How to implement communication between C/C++ and Python?](https://www.zhihu.com/question/23003213)
- [Performance optimization for Python and C/C++ extensions](https://zhuanlan.zhihu.com/p/363434563)
- [Extending Python with C/C++](https://blog.brickgao.com/2015/08/14/extending-Python-with-C-and-C-Plus-Plus/)
