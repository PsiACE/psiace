+++
title = "逃离编译时的内存溢出"
description = "通过链接器和符号修饰配置缓解 Rust 编译时 OOM。"
date = 2022-02-23
slug = "escape-oom-at-build-time"

[taxonomies]
tags = ["2022", "Databend", "Rust", "Linux", "Notes"]

[extra]
lang = "zh"
+++

今天写周报的时候提到了这个话题，顺便就记录一下如何逃离 Rust 编译时的内存溢出。

内存溢出，也就是 Out of Memory（OOM），从字面就能看出来，是要用到的内存大于系统能提供的最大内存而引起的故障。

Databend 中的 [common/functions](https://github.com/datafuselabs/databend/tree/main/common/functions) 模块为用户提供常用 SQL 函数支持，体量本身就很大，并且在新一轮的改造中引入了很多需要 codegen 的环节。于是，我们又遇到了老朋友（CI 又挂了）：

> (signal: 9, SIGKILL: kill) warning: build failed, waiting for other jobs to finish... error: build failed.

使用 `-Z time-passes` 这个 RUSTFLAGS 可以帮助观测一些指标，就很容易判断出来是 OOM 。而且之前的一些反馈和报错也能够佐证是发生在链接阶段。

那么，该怎么办呢？最简单的办法是「大就是好，多就是美」，加钱上更多内存，或者分配更大的 Swap 空间（没错，就像我之前有一个 [暴力的 32GiB Swapfile](https://psiace.me/btrfs-32gib-swapfile-on-fedora/)）。这当然可以一劳永逸，但：前者无疑会消耗钱包，目前内存条还是一个很大的负担，而且对于笔记本之类，更换的余地也有限；后者虽然守住了钱包，但是白白占去那么大一块空间，而且说不得会影响一些性能。

让我们一起看一下，有没有什么过渡的选项可以缓解这一尴尬的局面，进行一些有限的平衡。

## 「更快、更高、更强」的 mold

是的，既然是链接器的问题，那么最简单的办法就是换一个。Rust 默认的 linker 选项设定的是 `cc`，这意味着会利用到 gnu 工具链中的 `ld`，尽管 gnu 在自由软件领域有着卓越的贡献，但以目前的经验而言，这并不是一个好的现代选择。它的一个有力的竞争者是 llvm 工具链中的 lld 。

而到了今天，我们还有另外一个更加优越的候选人 —— 「[mold](https://github.com/rui314/mold)」，在实际使用中，表现出与 lld 相当、甚至超过的性能，并且使用更少的内存。

该如何与 Rust 工具链结合使用呢，有这么两种方法：

**mold -run**

采用这种模式，可以帮助我们快速体验 mold ，这得益于内置的拦截机制，可以将指向 ld ，ld.lld ，ld.gold 的命令转向 mold 自身。

```shell
# With Make.
mold -run make <make-options-if-any>
# Or with Cargo.
mold -run cargo <cargo-options-if-any>
```

**编辑 .cargo/config.toml**

添加下面的内容即可，如果是按 `sudo make install` 安装的，`path/to/mold` 大概率会指向 `/usr/local/bin/mold` 。

```toml
[target.x86_64-unknown-linux-gnu]
linker = "clang"
rustflags = ["-C", "link-arg=-fuse-ld=/path/to/mold"]
```

## 船新的符号修饰方案

符号修饰，或者说 symbol mangling ，是现代计算机程序设计语言的编译器用于解决由于程序实体的名字必须唯一而导致的问题的一种技术。

Rust 目前有一个自己设计符号修饰方案，[rust-lang/rfcs#2603](https://github.com/rust-lang/rfcs/pull/2603)，通过启用这一方案，在有重复组件的情况下，会生成更小的符号。

要想启用这一特性，同样有两种方法：

**RUSTFLAGS**

在目前最新的 Rust nightly 中，可以使用 `-C symbol-manging-version=v0` 这个 RUSTFLAG ，相对旧一点的版本可能需要使用 `-Z symbol-manging-version=v0` 。

> RUSTFLAGS="-C symbol-manging-version=v0" cargo <cargo-options-if-any>

**编辑 .cargo/config.toml**

添加下面的内容即可，如果报错，请试试 `-Z`：

```toml
[target.nightly-x86_64-unknown-linux-gnu]
rustflags = ["-C", "symbol-mangling-version=v0"]
```

## 还能做什么？

拆分成更小的单元，让编译每个部分的时候不会太吃力；或者去掉一些笨重的依赖，让它不那么费劲；或者对编译选项进行更多调整，进行针对性优化。

好吧，今天就到这里咯，祝大家都能逃离 OOM ，换上更强悍的机器。

---

笑死，清理了半天依赖，还剩下不到 900 个。
