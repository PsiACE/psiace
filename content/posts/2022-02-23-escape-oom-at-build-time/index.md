+++
title = "Escaping Out of Memory at Build Time"
description = "Mitigating Rust build-time OOM with linker and symbol mangling configuration."
date = 2022-02-23
slug = "escape-oom-at-build-time"

[taxonomies]
tags = ["2022", "Databend", "Rust", "Linux", "Notes"]

[extra]
lang = "en"
+++

I mentioned this topic while writing my weekly report today, so I will also record how to escape out-of-memory failures during Rust compilation.

Out of Memory, or OOM, is exactly what the name suggests: a failure caused when the required memory exceeds the maximum memory the system can provide.

In Databend, the [common/functions](https://github.com/datafuselabs/databend/tree/main/common/functions) module provides common SQL functions for users. It is already large by itself, and the latest round of refactoring introduced many codegen-related steps. So we met an old friend again: CI failed.

> (signal: 9, SIGKILL: kill) warning: build failed, waiting for other jobs to finish... error: build failed.

Using `-Z time-passes` in RUSTFLAGS can help observe some metrics, making it easy to judge that this was OOM. Earlier feedback and errors also supported that it happened during the linking stage.

So what should we do? The simplest method is "bigger is better, more is beautiful": pay for more memory, or allocate a larger swap space. Yes, like the [brutal 32GiB swapfile](https://psiace.me/btrfs-32gib-swapfile-on-fedora/) I had before. This can solve the problem once and for all, but the former obviously costs money. Memory sticks are still a large burden, and laptops often have limited room for replacement. The latter protects the wallet, but wastes a large chunk of disk space and may affect performance.

Let us see whether there are transitional options that can ease this awkward situation and make a limited compromise.

## The "Faster, Higher, Stronger" mold

Yes, since the problem is the linker, the simplest method is to change it. Rust's default linker option is `cc`, which means it uses `ld` from the GNU toolchain. Although GNU has made outstanding contributions to free software, in my current experience it is not a good modern choice. A strong competitor is lld from the LLVM toolchain.

Today, we also have an even better candidate: [mold](https://github.com/rui314/mold). In real use, it performs similarly to, or even better than, lld while using less memory.

How can it be used with the Rust toolchain? There are two methods.

**mold -run**

This mode helps us quickly try mold. Thanks to its built-in interception mechanism, commands pointing to ld, ld.lld, and ld.gold can be redirected to mold itself.

```shell
# With Make.
mold -run make <make-options-if-any>
# Or with Cargo.
mold -run cargo <cargo-options-if-any>
```

**Edit .cargo/config.toml**

Add the following content. If it was installed with `sudo make install`, `path/to/mold` will most likely point to `/usr/local/bin/mold`.

```toml
[target.x86_64-unknown-linux-gnu]
linker = "clang"
rustflags = ["-C", "link-arg=-fuse-ld=/path/to/mold"]
```

## A Brand New Symbol Mangling Scheme

Symbol mangling is a technique used by compilers of modern programming languages to solve the problem that program entity names must be unique.

Rust currently has its own symbol mangling scheme, [rust-lang/rfcs#2603](https://github.com/rust-lang/rfcs/pull/2603). Enabling it can generate smaller symbols when duplicate components exist.

There are also two ways to enable this feature.

**RUSTFLAGS**

In the latest Rust nightly, `-C symbol-manging-version=v0` can be used as a RUSTFLAG. Slightly older versions may require `-Z symbol-manging-version=v0`.

> RUSTFLAGS="-C symbol-manging-version=v0" cargo <cargo-options-if-any>

**Edit .cargo/config.toml**

Add the following content. If it errors, try `-Z`:

```toml
[target.nightly-x86_64-unknown-linux-gnu]
rustflags = ["-C", "symbol-mangling-version=v0"]
```

## What Else Can Be Done?

Split the project into smaller units so compiling each part is not too heavy; remove some bulky dependencies so the build is less painful; or adjust compilation options further for targeted optimization.

That is all for today. I wish everyone can escape OOM and get stronger machines.

---

Funny enough, after cleaning dependencies for quite a while, fewer than 900 still remain.
