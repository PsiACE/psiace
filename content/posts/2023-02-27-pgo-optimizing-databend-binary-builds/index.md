+++
title = "Optimizing Databend Binary Builds with PGO"
description = "Building Databend with profile-guided optimization in Rust: profile collection, llvm-profdata merging, and profile-use builds."
date = 2023-02-27
slug = "pgo-optimizing-databend-binary-builds"

[taxonomies]
tags = ["2023", "Databend", "Rust", "PGO", "Archive"]

[extra]
lang = "en"
source_url = "https://juejin.cn/post/7204715616283705401"
source_note = "English translation of the Chinese original, first published on 2023-02-27. Source: "
source_label = "Juejin original"
source_tail = ". This translation was prepared for this archive."
+++

> Author: Chojan Shang
>
> Master's student at Macau University of Science and Technology, R&D Engineer Intern at Databend
>
> [github.com/PsiACE](https://github.com/PsiACE)

In a recent issue [#9387](https://github.com/datafuselabs/databend/issues/9387), a friend in the Databend community expressed the hope that PGO could be used to build a performance-optimized executable. Let us take a look at how to build a PGO-optimized Databend with Rust!

## **Background**

**Profile-guided optimization** is a compiler optimization technique. It collects typical execution data from a program's run (the branches that may be taken), and then optimizes inlining, conditional branches, machine code layout, register allocation, and so on.

The background to introducing this technique is this: static analysis techniques in the compiler can consider code optimizations without executing the code, thereby improving the performance of the compiled artifact; but these optimizations are not necessarily fully effective, because in the absence of runtime information the compiler cannot take the program's actual execution into account.

PGO can collect data based on the application's scenario in production, thereby allowing the optimizer to optimize for speed on hotter code paths and for size on colder code paths, generating faster and smaller code for the application.

rustc supports PGO , allowing you to create a binary with built-in data collection and then collect data while it runs, in preparation for the final compile-time optimization. Its implementation relies entirely on LLVM .

## **Typical Process**

Building a PGO-optimized binary usually requires the following steps:

- Build a binary with built-in data collection
- Run it and collect data; the data is stored in the form of `.proraw`
- Convert the `.proraw` files into `.prodata` files
- Build with optimization guided by the `.prodata` files

## **Prerequisites**

The data collected during the run ultimately has to be converted with `llvm-profdata`. Installing the `llvm-tools-preview` component through `rustup` provides `llvm-profdata` , or you may consider using the one provided by a recent version of LLVM and Clang.

```bash
rustup component add llvm-tools-preview
```

After installation, `llvm-profdata` may need to be added to `PATH` ; the path is as follows:

```text
~/.rustup/toolchains/<toolchain>/lib/rustlib/<target-triple>/bin/
```

## **Specific Steps**

Here we do not pick a workload from any particular production environment; instead, we use Databend's SQL logic tests as a demonstration. This may not have a positive effect on performance, but it helps us understand how to carry out this process.

> ***Note:*** The data samples provided to the program must be statistically representative of typical usage scenarios; otherwise, the feedback may harm the overall performance of the final build.

**1. Clear old data**

```bash
rm -rf /tmp/pgo-data
```

**2. Compile a release that supports collecting profile data. Using `RUSTFLAGS` applies the PGO compilation flags to the compilation of all crates.**

```bash
RUSTFLAGS="-Cprofile-generate=/tmp/pgo-data" \    
cargo build --release --target=x86_64-unknown-linux-gnu
```

**3. Run the compiled program. In practice, it is recommended to use a dataset and queries that match a typical production workload.**

a.  Start a standalone Databend node via a script. Considering that production environments mostly run in cluster mode, you can also start a Databend cluster.

b.  Import the dataset and run a typical query workload.

In the example we choose to run the SQL logic tests, for reference only.

```bash
BUILD_PROFILE=release ./scripts/ci/deploy/databend-query-standalone.sh 
ulimit -n 10000;ulimit -s 16384; cargo run -p sqllogictests --release -- --enable_sandbox --parallel 16 --no-fail-fast
```

**4. Merge the profile data with `llvm-profdata`**

```bash
llvm-profdata merge -o /tmp/pgo-data/merged.profdata /tmp/pgo-data
```

**5. Compile under the guidance of the profile data. In fact, you may notice that both builds use the `--release` flag, because in actual runtime situations we always use the release-built binary.**

```bash
RUSTFLAGS="-Cprofile-use=/tmp/pgo-data/merged.profdata -Cllvm-args=-pgo-warn-missing-function" \    
cargo build --release --target=x86_64-unknown-linux-gnu
```

**6. Run the compiled program once more, running the previous workload to check performance.**

```bash
BUILD_PROFILE=release ./scripts/ci/deploy/databend-query-standalone.sh 
ulimit -n 10000;ulimit -s 16384; cargo run -p sqllogictests --release -- --enable_sandbox --parallel 16 --no-fail-fast
```

## **References**

- [doc.rust-lang.org/rustc/profi…](https://doc.rust-lang.org/rustc/profile-guided-optimization.html)
- [en.wikipedia.org/wiki/Profil…](https://en.wikipedia.org/wiki/Profile-guided%5C_optimization)
- [learn.microsoft.com/en-us/cpp/b…](https://learn.microsoft.com/en-us/cpp/build/profile-guided-optimizations?view=msvc-170)
- [clang.llvm.org/docs/UsersM…](https://clang.llvm.org/docs/UsersManual.html#profile-guided-optimization)

## **About Databend**

Databend is an open-source, elastic, low-cost modern data warehouse built on object storage that can also do real-time analytics. We look forward to your attention as we explore cloud-native data warehouse solutions together and build a new generation of open-source Data Cloud.

- Databend Cloud: [databend.cn](https://databend.cn)
- Databend Docs: [databend.rs/](https://databend.rs/)
- Twitter: [twitter.com/Datafuse_La…](https://twitter.com/Datafuse_Labs)
- Slack: [datafusecloud.slack.com/](https://datafusecloud.slack.com/)
- Wechat: Databend
- GitHub: [github.com/datafuselab…](https://github.com/datafuselabs/databend)
