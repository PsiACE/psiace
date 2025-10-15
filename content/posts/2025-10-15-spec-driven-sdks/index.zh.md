+++
title = "用 Spec 做 SDK - 生成式 AI 的时代"
description = "在 AI 时代走中间路径：用规范约束 AI，用 AI 加速规范。基于 ACP 的 SDK 实践：路由、黄金样张与可审计性。"
date = 2025-10-15
slug = "spec-driven-sdks"

[taxonomies]
tags = ["AI", "SDK", "Spec", "ACP", "Agent", "MCP"]
categories = ["工程实践"]

[extra]
lang = "zh"
+++

> AI 写得快，但容易膨胀；
> Spec 很严格，但可能僵化。
>
> 我选择中间那条路——
> 让 AI 在边界内跑，让人对结果负责。

## 为什么不是全 AI，也不是全 Spec

AI 写代码的速度让人上瘾；一旦规模扩大，很容易出现上下文漂移、结构膨胀、边界模糊——项目“能跑但不稳”。

另一个极端是 spec 驱动：严谨，但往往过重。GitHub 推出的 [Spec Kit](https://github.com/github/spec-kit) 倡导“先规范再生成”，对快速迭代的团队并不总是友好，容易过度设计、难以跟踪决策。

我走中间态：在维护 [Agent Client Protocol (ACP)](https://agentclientprotocol.com) 的 [**Python SDK**](https://github.com/psiace/agent-client-protocol-python) 时，用规范约束 AI 生成，用 AI 加速规范适配。

## ACP：为 SDK 而生的协议

ACP 由 [Zed](https://zed.dev/blog/bring-your-own-agent-to-zed) 发起，定义**编辑器 ↔ Agent** 的通信方式。
它采用 [JSON-RPC 2.0](https://www.jsonrpc.org/specification) 作为通信机制，并以 **JSON Schema** 描述数据结构（典型 schema 见 ACP 仓库）。边界明确、类型可机读、行为可审计——天生适合需要跨语言、长期维护的 SDK。

## 我的实现过程

### 起点：最小可用体（MVP）

我给自己三条约束（大量使用 Coding Agent，统一由我把边界与审阅）：

1. 基于 datamodel 生成 **Pydantic** 模型（[pydantic.dev](https://docs.pydantic.dev/latest/)）。
2. 实现最小 I/O（JSON-RPC over stdio）。
3. 迁移文档示例与基本测试，由我负责核对与回归。

体量刻意保持小：**先上线，尽快暴露问题**。

### 迭代：从反馈中长出结构

早期用户反馈“命名不一致、使用不顺手”。
我让 agent 扫描文档生成 **rename map**（统一 Python 化命名），并对照其他语言实现取长补短：

- TypeScript SDK 里 **helpers**（降低重复样板）。
- Go SDK 用 **golden tests**（固定请求/响应样张做回归）。
- Rust SDK 的模块组织更克制。
- 其他协议类 SDK（如 [MCP](https://modelcontextprotocol.io/)）采用相似的协议，值得借鉴。

在 agent 协助下完成结构与测试重组，由我把控标准与审阅路径。

### 路由化：替代 if 判断

我不想看到满屏的 `if method == "..."`，于是写了极简路由，把“方法名 → 处理器”变成一等公民：

```python
builder = RouterBuilder()

builder.request_attr(CLIENT_METHODS["fs_write_text_file"], WriteTextFileRequest, client, "writeTextFile")
builder.request_attr(CLIENT_METHODS["fs_read_text_file"],  ReadTextFileRequest,  client, "readTextFile")
```

到 `v0.4.9`，体量不大，但代码 **稳定且可教学**。

## 上下文拣选：让 AI 吃对东西

我把提示词上下文当“工程预算”管理：只喂必要信息、限定边界，并对版本负责。

- **上下文清单（manifest）**：只列 schema、公共接口与最小示例；排除生成代码与外部依赖。
- **Diff 感知**：只给改动的 hunk 与少量前后文（5–15 行），而不是整文件。
- **黄金片段索引**：提示 agent 自检索必要片段，避免大段粘贴。
- **先立护栏**：明确“不得臆造 schema 字段；失败优先；缺信息先询问”。

## 方法论：Spec 与 AI 的协作

| 原则                   | 说明                                       |
| :--------------------- | :----------------------------------------- |
| **生成与人工治理分离** | 模型自动生成，业务由人编排与审阅，不混用。 |
| **从最小可用体开始**   | 用真实反馈驱动人体工学优化。               |
| **Golden Test**        | 捕获/回放请求与响应，作为回归与审计基线。  |
| **上下文拣选与预算**   | 只喂必要上下文，小而准、可复现。           |

规范给 AI 以边界；AI 让规范鲜活起来。

## 责任感：为什么我敢对 AI 写的代码负责

AI 能写，但边界我来定义。
有强类型模型、可复现测试、可回放轨迹，我可以验证每一步。
我信任的不是模型，而是 **它背后的工程纪律** 。

## 我在 PR 里的说明

这段说明最早见于 [@xuanwo](https://github.com/Xuanwo) 的 PR。我之前没有这样写，但我愿意采用这种方式——因为我对结果负责。在这个 SDK 的工作中我大量使用了 AI；**边界与质量由我把关**：

> **This PR was primarily authored with GPT-5-Codex and hand-reviewed by me.
> I’m responsible for every change that lands here.**

这不是“炫 AI”，而是**结果负责的声明**。

## 结语：速度与轨道

AI 是燃料，Spec 是轨道。
燃料给你速度，轨道让你抵达。

我喜欢这种平衡：模型来写，我来设边界。
每一行可解释，每一次失败可复现。
这就是在人工智能时代负责任地构建方式。

— **PsiACE** （[GitHub](https://github.com/PsiACE) · [Apache OpenDAL PMC Member](https://opendal.apache.org/)）
