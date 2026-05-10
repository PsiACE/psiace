+++
title = "我永远讨厌 Python Fibonacci"
description = "从 Fibonacci 的不同算法实现到使用 C/C++ 扩展 Python 的一次整理。"
date = 2022-09-30
slug = "master-python-fibonacci"

[taxonomies]
tags = ["2022", "Python", "Notes"]

[extra]
lang = "zh"
+++

这里是 PsiACE，好久没和大家见面做公开的汇报了。

目前的话人在澳门，总体上还不错，最近一段时间做饭水平急速提高，并且不得不捡起好久没写过的 Python 。

「回」字大概有四种写法，Python Fibonacci 则更多，让我们一起来看一下吧。

这篇文章主要从两个方面来介绍，前半部分主要关注 Fibonacci 的不同算法实现，后半部分则会关注如何使用 C/C++ 等来拓展 Fibonacci 。

## Fibonacci 的不同算法实现

[斐波那契数列](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Fibonacci%23Fibonacci_sequence)（Fibonacci sequence）是以意大利数学家 `列昂纳多·斐波那契` 的名字命名的数列。

斐波那契数列在计算机里面有很多用途，例如斐波那契查找（二分查找的一种改进），斐波那契堆等。

### 递归

根据 Fibonacci 定义，可以轻松写出一个递归算法：

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

### 记忆化

一个简单的优化思路是采用记忆化，因为是一个递归的计算方法，保存之前的结果会比较有利。

```python
def fib(n):
    @lru_cache()
    def fib(n):
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)
    return fib(n)
```

进一步优化的话可以选择递推形式的算法，比如记忆全部的前置结果。大概是线性级别。

```python
def fib(n):
    data = [0, 1]
    for i in range(n-1):
        data.append(data[-2] + data[-1])
    return data[n]
```

但是事实上，我们不需要记录那么多中间结果，仅需要保留前两个值即可：

```python
def fib(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a
```

### 数学

更进一步地，如果将其递推公式整理为通项公式，可以得到下面的算法：

```python
def fib(n):
    sqrt5 = 5**0.5
    fibN = ((1 + sqrt5) / 2) ** n - ((1 - sqrt5) / 2) ** n
    return round(fibN / sqrt5)
```

这种方法非常快，但是要考虑 `int` 溢出，仅仅对小数据量有效。(常数级别)

### 矩阵乘法

那么还有没有其他方法呢？比如矩阵乘法，大概是对数级别：

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

## 使用 C / C++ 拓展 Fibonacci

一个非常典型的观点是，Python是一种适合初学者、开发快速的语言，但没有很大的性能优势。甚至在 PyCon 上，[@gvanrossum](https://github.com/gvanrossum) 也说，必须让 Python 语言的速度水平提高 2 倍，借此与 C++ 等高性能编程语言正面对抗。

显然，存在一些已知的改善性能的办法，并且在主流的数据科学包以及 web framework 包中得到了应用。

- 降低时间复杂度。不管是什么原因导致程序变慢，只要可以，直接选择一个更快的算法。
- 并行化代码。如果存在多个闲置的处理器，可以尝试将任务分割成可以同时处理的子任务。
- 使用更快的语言重写代码中较慢的部分。

使用 C / C++ 拓展 Python 的显著好处：

- 一方面，得益于 Python 的简单易用，可以提供一套清晰和简化的接口，降低下游开发人员的精力投入，加速应用的开发。
- 另一方面，得益于其他语言的性能和编译优化，可以显著改善程序性能。

### 如何使用 C / C++ 拓展 Python

**使用 Python 的 ctypes 模块**

ctypes 是 Python 官方提供的 FFI 模块，适用于动态链接库。调用时的处理复杂度基本转移到 Python，无法很好利用 Python 中的一些能力。

**使用 Python CAPI**

CPython 为 C / C++ 提供了一套 API ，可以使用 Python 原生的一些能力完成 C / C++ 与 Python 的交互。但是在调试方面依然需要采用 C / C++ 工具链，而且因为调用了 Python 底层的 CAPI，有时候需要手动去操控 Python 的引用计数来完成 Python 的 GC 机制。

**使用 Cython**

Cython 是一种面向 Python 和 Cython 语言的一个优化过的静态编译器。Cython 会将 Python 和 Cython 翻译成 C/C++，然后编译成一个静态链接库供 Python 使用。

Cython 除了提供 CAPI 之外，还提供了大部分的封装好的模块和函数，而对于 Unicode 或者 Python 的异常机制，Cython 会帮助你自动翻译成 C/C++ 。由于 Cython 做的是代码转译，粒度相对较粗，所以无法做一些细粒度优化。

**使用 SWIG**

SWIG 并不只是提供 C/C++ 对 Python 的拓展，还提供对 Java、Perl 等其他语言的拓展支持，就是写一个拓展可以在多处使用。

使用 SWIG 的最大优点是可以使同一套代码拓展多种语言，但是对于某些特性，依然还是要针对 Python 在配置文件中显式地写出一些 Python CAPI 相关的调用，在调试方面，也是只能使用 C/C++ 配套的调试工具。

### 示例与性能

让我们继续回到斐波那契数列的例子，之前的内容中，我们曾经讨论过它的算法和一些优化。

**递归**

接下来的内容中，将会使用递归算法作为基准来展现不同的优化，除了并行部分之外，我们将会使用 `fib(47)` 进行性能评估。

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

**并行**

通过使用 multiprocessing 进行池化，我们得以同时执行多个计算任务，这使得在一些特定场景下具有性能优势。

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

简单看一下性能：

| Language         | Time, s |
| ---------------- | ------- |
| Python Recursive | 1.377   |
| Python Parallel  | 0.669   |

**快速算法 - 记忆化**

递归算法相当朴素，也非常的慢，更加快速的算法我们在之前有过讨论，这里给出一个缓存最近结果的一个简单算法。

```python
from functools import lru_cache

@lru_cache(3)
def fib(n):
  if n <= 1: return 1
  return fib(n - 1) + fib(n - 2)

print(fib(47))
```

**PyPy - JIT**

PyPy 是 CPython 的替代品。它是使用与之共同开发的 RPython 语言构建的。使用它而不是 CPython 的主要原因是速度: 它通常运行得更快。

PyPy 实现了 Python 2.7.18和3.7.10。它支持所有的核心语言，通过 Python 2.7 测试套件和几乎所有的 3.7 测试套件。它支持大多数常用的 Python 标准库模块。

PyPy 快速的秘密在于使用了 JIT 技术，以下是 JIT 编译为提高性能而采取的步骤：

- 标识代码中最常用的组件，例如循环中的函数。
- 在运行时将这些组件转换为机器码。
- 优化生成的机器码。
- 用优化的机器码版本替换以前的实现。

很高兴，我们的递归版本可以自然地利用 PyPy 进行编译以获得性能上的提升。

**C**

由于要展示 C/C++ 拓展的能力，我们也提供 C 语言版本做一个比较。

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

同样的，我们仿照之前的 C 语言版本，编写对应的共享库。

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

接下来，让我们使用 `ctypes` 来调用它。主要的部分都很简单，需要注意的是，`uint64_t` 对应的是 `c_ulonglong` ，我们需要指定参数类型和结果类型。

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

接着，我们需要编译共享库，并像运行其他 Python 程序那样执行。

```bash
$ gcc -O3 -fPIC -shared -std=c99  fib-share.c -o ctypes_fib.so
$ python fib-ctypes.py
```

**CAPI**

相比其他几种方法，CAPI 会显得复杂一些，所以，我大概会推荐你去阅读 [How to Write and Debug C Extension Modules](https://llllllllll.github.io/c-extension-tutorial/) 。

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

所有的函数返回类型都是 PyObject 的指针，参数类型是是 PyObject 的两个指针，前者对应 Python 类里方法的 self，后者对应串里的参数。

完成我们需要的函数之后，需要显示地声明模块暴露在外的方法，接受参数的类型以及文档。

```python
from .fib import fib


__all__ = ['fib']
```

构建 CPython 扩展模块的最常见方法是使用 setuptools 和 setup.py 文件。我们从一个普通的 setuptools setup.py 文件开始：

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

从根目录运行以下命令：

```bash
python setup.py build_ext --inplace
```

最后，像写一个普通的Python程序一样调用它。

```python
import fib

print(fib.fib(47))
```

**Cython**

如果使用 Cython, 代码可以更改为：

```python
cdef long fib(long n):
  if n <= 1: return n
  return fib(n - 1) + fib(n - 2)

print(fib(47))
```

需要使用下面的命令来编译：

```bash
cython -3 --embed -o fib.pyx.c fib.pyx && gcc -O3 $(python3-config --embed --cflags) -o fib fib.pyx.c $(python3-config --embed --ldflags)
```

**SWIG**

首先，让我们复用之前 ctypes 一节中的 `fib-share.h` 和 `fib-share.c` 。

接着，定义对应的 SWIG 接口文件，为了使用 `uint64_t` ，我们不得不引入 `stdint.i` 。

```c
%%file fib-swig.i
%include "stdint.i"

%module fibswig
%{
extern uint64_t c_fib(uint64_t n);
%}

extern uint64_t c_fib(uint64_t n);
```

然后，我们需要编写一点 python 代码来调用 swig 共享库

```python
import fibswig

print(fibswig.c_fib(47))
```

接着，我们需要编译共享库，并像运行其他 Python 程序那样执行。

```bash
$ swig -python fib-swig.i
$ gcc -fPIC -c fib-share.c fib-swig_wrap.c -I /usr/include/python3.10
$ ld -fPIC -shared fib-share.o fib-swig_wrap.o -o _fibswig.so
$ python fib-swig.py
```

**性能汇总**

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

## 致谢

- [509. 斐波那契数 - 力扣](https://leetcode.cn/problems/fibonacci-number/)
- [Extending Python with C or C++](https://docs.python.org/3/extending/extending.html)
- [`ctypes` — A foreign function library for Python](https://docs.python.org/3/library/ctypes.html)
- [Building a Python C Extension Module](https://realpython.com/build-python-c-extension-module/)
- [Write Your Own C-extension to Speed Up Python by 100x](https://towardsdatascience.com/write-your-own-c-extension-to-speed-up-python-x100-626bb9d166e7)
- [Extending Python with C](https://medium.com/delta-force/extending-python-with-c-f4e9656fbf5d)
- [Extending Python with C or C++ code](https://web.mit.edu/people/amliu/vrut/python/ext/intro.html)
- [如何实现 C/C++ 与 Python 的通信？](https://www.zhihu.com/question/23003213)
- [Python 和 C/C++ 拓展程序的性能优化](https://zhuanlan.zhihu.com/p/363434563)
- [用 C/C++ 拓展 Python](https://blog.brickgao.com/2015/08/14/extending-Python-with-C-and-C-Plus-Plus/)
