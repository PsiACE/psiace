+++
title = "使用 PGO 优化 Databend 二进制构建"
description = "在 Rust 中使用 PGO 构建 Databend：采集 profile、合并数据并以 profile 指导编译。"
date = 2023-02-27
slug = "pgo-optimizing-databend-binary-builds"

[taxonomies]
tags = ["2023", "Databend", "Rust", "PGO", "归档"]

[extra]
lang = "zh"
source_url = "https://juejin.cn/post/7204715616283705401"
source_note = "本文原发于 2023-02-27："
source_label = "掘金原文"
source_tail = "。此处为存档版本，正文按原文照录。"
+++

> 作者：尚卓燃
>
> 澳门科技大学在读硕士，Databend 研发工程师实习生
>
> [github.com/PsiACE](https://github.com/PsiACE)

在最近的一个 Issue 中 [#9387](https://github.com/datafuselabs/databend/issues/9387)，Databend 社区的朋友希望能够利用 PGO 技术构建性能优化的可执行文件。让我们一起来看一下如何使用 Rust 构建 PGO 优化后的 Databend 吧！

## **背景知识**

**Profile-guided optimization** 是一种编译器优化技术，它会收集程序运行过程中的典型执行数据（可能执行的分支），然后针对内联、条件分支、机器代码布局、寄存器分配等进行优化。

引入这一技术的背景是：编译器中的静态分析技术能够在不执行代码的情况下考虑代码优化，从而提高编译产物的性能；但是这些优化并不一定能够完全有效，在缺乏运行时信息的情况下，编译器无法考虑到程序的实际执行情况。

PGO 可以基于应用程序在生产环境中的场景收集数据，从而允许优化器针对较热的代码路径优化速度并针对较冷的代码路径优化大小，为应用程序生成更快和更小的代码。

rustc 支持 PGO ，允许创建内置数据收集的二进制文件，然后在运行过程中收集数据，从而为最终的编译优化做准备。其实现完全依赖 LLVM 。

## **典型过程**

构建 PGO 优化的二进制文件通常需要进行以下几步工作：

-  构建内置数据收集的二进制文件
-  运行并收集数据，数据会以 `.proraw` 的形式存在
-  将 `.proraw` 文件转换为 `.prodata` 文件
-  根据 `.prodata` 文件进行构建优化

## **前置准备**

运行过程中的收集到的数据最终需要使用 `llvm-profdata` 进行转换，经由 `rustup` 安装 `llvm-tools-preview` 组件可以提供 `llvm-profdata` ，或者也可以考虑使用最近版本的 LLVM 和 Clang 提供的这一程序。

```bash
rustup component add llvm-tools-preview
```

安装之后的 `llvm-profdata` 可能需要被添加到 `PATH` ，路径如下：

```text
~/.rustup/toolchains/<toolchain>/lib/rustlib/<target-triple>/bin/
```

## **具体步骤**

这里并没有选用某个具体生产环境的工作负载，而是使用 Databend 的 SQL 逻辑测试作为一个示范。在性能上可能并不具有积极意义，但可以帮助我们了解如何进行这一过程。

> ***特别提示：*** 提供给程序的数据样本必须在统计学上代表典型的使用场景; 否则，反馈有可能损害最终构建的整体性能。

**1. 清除旧数据**

```bash
rm -rf /tmp/pgo-data
```

**2. 编译支持收集 profile 数据的 release ，使用 `RUSTFLAGS` 可以将 PGO 编译标志应用到所有 crates 的编译中。**

```bash
RUSTFLAGS="-Cprofile-generate=/tmp/pgo-data" \    
cargo build --release --target=x86_64-unknown-linux-gnu
```

**3.运行编译好的程序，实际情况下推荐使用符合生产环境典型工作负载的数据集和查询。**

a.   通过脚本启动 Databend 单机节点，考虑到生产环境更多是以集群模式运行，也可以启动 Databend 集群。

b.  导入数据集并运行典型的查询工作负载。

示例中选择执行 SQL 逻辑测试，仅供参考。

```bash
BUILD_PROFILE=release ./scripts/ci/deploy/databend-query-standalone.sh 
ulimit -n 10000;ulimit -s 16384; cargo run -p sqllogictests --release -- --enable_sandbox --parallel 16 --no-fail-fast
```

**4. 使用 `llvm-profdata` 合并 profile 数据**

```bash
llvm-profdata merge -o /tmp/pgo-data/merged.profdata /tmp/pgo-data
```

**5. 在 profile 数据指导下进行编译，其实可以注意到，两次编译都使用 `--release` 标志，因为实际运行情况下，我们总是使用 release 构建的二进制。**

```bash
RUSTFLAGS="-Cprofile-use=/tmp/pgo-data/merged.profdata -Cllvm-args=-pgo-warn-missing-function" \    
cargo build --release --target=x86_64-unknown-linux-gnu
```

**6. 再次运行编译好的程序，运行之前的工作负载以检查性能。**

```bash
BUILD_PROFILE=release ./scripts/ci/deploy/databend-query-standalone.sh 
ulimit -n 10000;ulimit -s 16384; cargo run -p sqllogictests --release -- --enable_sandbox --parallel 16 --no-fail-fast
```

## **参考资料**

- [doc.rust-lang.org/rustc/profi…](https://doc.rust-lang.org/rustc/profile-guided-optimization.html)
- [en.wikipedia.org/wiki/Profil…](https://en.wikipedia.org/wiki/Profile-guided%5C_optimization)
- [learn.microsoft.com/en-us/cpp/b…](https://learn.microsoft.com/en-us/cpp/build/profile-guided-optimizations?view=msvc-170)
- [clang.llvm.org/docs/UsersM…](https://clang.llvm.org/docs/UsersManual.html#profile-guided-optimization)

## **关于 Databend**

Databend 是一款开源、弹性、低成本，基于对象存储也可以做实时分析的新式数仓。期待您的关注，一起探索云原生数仓解决方案，打造新一代开源 Data Cloud。

-  Databend Cloud：[databend.cn](https://databend.cn)
-  Databend 文档：[databend.rs/](https://databend.rs/)
-  Twitter：[twitter.com/Datafuse_La…](https://twitter.com/Datafuse_Labs)
-  Slack：[datafusecloud.slack.com/](https://datafusecloud.slack.com/)
-  Wechat：Databend
-  GitHub：[github.com/datafuselab…](https://github.com/datafuselabs/databend)
