+++
title = "Spec‑Driven SDKs in the Age of Generative AI"
description = "Walk the middle path: use specs to bound AI, and AI to accelerate specs. An ACP‑based SDK with routing, golden tests, and auditability."
date = 2025-10-15
slug = "spec-driven-sdks"

[taxonomies]
tags = ["AI", "SDK", "Spec", "ACP", "Agent", "MCP"]
categories = ["engineering"]

[extra]
lang = "en"
+++

> AI writes fast — and tends to bloat.
> Specs are strict — and can ossify.
>
> I choose the middle path —
> let AI run inside boundaries, and let humans own outcomes.

## Why Not Pure AI, Nor Pure Spec

AI‑assisted coding is addictive, but as projects grow, context drifts and complexity balloons.
You get something that runs, but barely holds.

On the other hand, pure spec‑driven frameworks — like GitHub’s [Spec Kit](https://github.com/github/spec-kit) — are often heavy for iterative work.
Precise, but hard to live with.

So I took the middle ground: spec‑first boundaries, AI‑assisted speed — using the Agent Client Protocol (ACP).

## What Makes ACP a Good Base

ACP, started by Zed, defines how editors and agents talk.
It uses JSON‑RPC 2.0 and is described in JSON Schema — clear edges, machine‑readable types, auditable behaviors.
That balance makes it ideal for SDKs that must live across languages and over time.

I applied this while maintaining the ACP [Python SDK](https://github.com/psiace/agent-client-protocol-python) for the [Agent Client Protocol](https://agentclientprotocol.com).

## How I Built the Python SDK

### Stage 0 — Minimal, but Runnable

I relied heavily on a coding agent (Codex) with human‑set boundaries and review. Three constraints:

1. Agent‑generated Pydantic models from the datamodel.
2. Minimal I/O (JSON‑RPC over stdio), with agent assistance.
3. Agent‑ported examples and basic tests, human‑verified for regression.

Small on purpose: ship first, surface problems early.

### Stage 1 — Learning from Feedback

Early users found naming awkward and ergonomics rough.
I had the agent scan docs to produce a rename map (more Pythonic names), then borrowed ideas from other SDKs:

- TypeScript had helpers.
- Go had golden tests.
- Rust had clean modular structure.
- Protocol SDKs like MCP offered architecture hints.

With agent assistance I restructured code and tests; I set the standards and did the reviews.

### Stage 2 — Routing over Conditionals

I didn’t want endless if‑trees like `if method == "..."`.
So I wrote a compact router that makes method→handler first‑class:

```python
builder = RouterBuilder()

builder.request_attr(CLIENT_METHODS["fs_write_text_file"], WriteTextFileRequest, client, "writeTextFile")
builder.request_attr(CLIENT_METHODS["fs_read_text_file"], ReadTextFileRequest, client, "readTextFile")
```

Registered handlers are pluggable, testable, and auditable.
By v0.4.9 the SDK wasn’t big, but it was stable and teachable.

### Context curation — feed the agent only what matters

I treat prompt context as an engineering budget:

- Context manifest: list only schemas, public interfaces, and minimal examples; exclude generated/vendor code.
- Diff‑aware prompting: provide changed hunks plus a small window (5–15 lines), not whole files.
- Golden snippets index: let the agent retrieve tagged canonical examples instead of pasting large blobs.
- Guardrails first: “Do not invent fields beyond schema; fail closed; ask for missing inputs.”

## Principles for Spec‑Driven, AI‑Assisted SDKs

| Principle | Description |
| :-- | :-- |
| Separate generated vs human‑governed code | Models are generated; business logic is human‑owned and reviewed. Never mix. |
| Ship the smallest working unit first | Real feedback drives ergonomics. |
| Golden tests for major RPCs | Capture and replay requests/responses as the regression and audit baseline. |
| Curate and budget context | Feed only what’s necessary — small, precise, reproducible. |

Specs give AI a sandbox — and AI makes specs come alive.

## Accountability: Why I Trust AI‑Written Code

AI can write, but I set the boundaries.
Typed models, reproducible tests, and replayable traces let me verify every step.
I trust not the model, but the engineering discipline around it.

## A Note in My PRs

I first saw this note in @Xuanwo’s PRs. I haven’t used it in mine yet, but I’m willing to adopt it — because I’m accountable for the outcome. In this SDK work I used AI heavily; I set the boundaries and own the result:

> This PR was primarily authored with GPT‑5‑Codex and hand‑reviewed by me.
> I’m responsible for every line that lands here.

This isn’t about showing off AI — it’s about owning the outcome.

## Closing: Fuel and Rails

AI is the fuel.
Spec is the rail.
Fuel gives speed; rails keep you alive.

I like this balance — AI writes, I define boundaries.
Every line explainable, every bug reproducible.
That’s how to build responsibly in the AI age.

— **PsiACE** ([GitHub](https://github.com/PsiACE) · [Apache OpenDAL PMC Member](https://opendal.apache.org/))
