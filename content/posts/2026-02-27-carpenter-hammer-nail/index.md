+++
title = "Carpenter, Hammer, Nail"
description = "A reflection from bub: coding agents, RAG limits, paradigm shifts, and why context should be constructed, not inherited."
date = 2026-02-27
slug = "carpenter-hammer-nail"

[taxonomies]
tags = ["agent", "bub", "coding-agent", "rag", "context", "memory", "openclaw"]

[extra]
lang = "en"
+++

> This post is dedicated to bub, an agent that lives in group chats. I want to talk about the problems, paradigms, and model shifts behind it.
> [kemingy](https://github.com/kemingy) once roasted me: "Your writing feels too divergent. It drifts away from technical writing, needs extra context, and still may not align."
> Luckily, this time I started from preparing an internal company talk, so I finally followed a proper structure.

## Preface

Hi, I’m PsiACE. I used to work on databases, RAG, agents, and open source. Now I work on open-source ecosystem projects at OceanBase. You can find me on [GitHub](https://github.com/PsiACE/).

Even within the coding-agent subdomain alone, I’ve worked on RAG, sandboxing, agents, and protocols. For example, [agent-client-protocol](https://github.com/agentclientprotocol/python-sdk) ranks around top 10k downloads in the Python ecosystem (about 1.2%), and none of this was ever my official day job.

Today’s sharing is a projection of my thoughts and experiences from years of working on agents, plus my recent restart of [bub](https://github.com/psiace/bub). In just a few days, bub evolved from a simple coding agent into a form that feels OpenClaw-like, but not the same.

My current lens is somewhat more product-oriented, so this won’t dive too deep into hardcore implementation details. Before we go further, let’s look at the title: *Carpenter, Hammer, Nail*:

- If someone has a hammer, everything starts to look like a nail.
- If someone with a hammer can tell what is actually a nail, that’s success.
- Once I have a hammer, fewer and fewer things look like “not a nail.”

You are also welcome to read my previous posts.

## How to Get a Coding Agent

Most people have used coding agents: Cursor, Codex, Claude Code.

An agent is roughly model + tools + looped calls. So what should a coding agent look like?

Pi, which is hot recently and built into OpenClaw, exposes four tools: bash, read, write, edit. Its simplicity made people love it. It looks simple, but in July last year, bub’s first version also had these exact tools. And bub was not the origin of this story. Earlier on the timeline, around 2025-04, ampcode had already pointed this out.

Why these four tools?

Read and write are base abilities: input and output. Edit looks like a write optimization, but in practice it gives precise intervention and shortens the feedback loop. Bash is the bridge to the vast CLI and programmable tooling ecosystem, preventing us from reinventing unnecessary wheels.

Recommended reading: [Building a Self-Bootstrapping Coding Agent in Python](/posts/baby-step-coding-agent/)

## RAG and Its Applicability

If we keep going in this direction, we quickly hit another topic: RAG.

> Side note: at my previous company, my teammates and I designed and implemented fusiongraphrag, one of the few GraphRAG solutions in the document domain that was truly deployable.

The “R” means retrieval, which is a very broad basket. That’s why I sometimes need terms like “naive RAG” to refer specifically to vector, full-text, or hybrid retrieval strategies.

Naive RAG is not always effective:

- In frequently changing codebases, building vector/full-text indexes naturally amplifies cost. Chunking and indexing pipelines can even block normal development flow. Early Cursor on very large repos is a typical example: expensive indexing, long wait time, freshness issues.
- Another severe issue is semantic mismatch. Due to training data and the natural gap between natural language and code, common embedding models often fail to represent code effectively. The system falls back to full-text retrieval and keyword-based matching. Before being acquired, Jina had released a dedicated embedding model for code-natural-language alignment exactly to address this.

So grep + read + agent loop became a more clever, intuitive, and effective solution, first argued and validated by aider in 2024. For a while, this kind of RAG with explicit agent loops was commonly called Agentic RAG.

Of course, naive RAG still has advantages in this scenario when code and comments already have good semantics, strong representation, and low change frequency: for example, released versioned repositories, upstream dependencies, or document-focused corpora, especially specs and consensus documents.

Recommended reading: [RAG in Coding Agents: Making Smarter Programming Assistants](/posts/rag-in-coding-agent/)

## Different Paradigms Behind OpenClaw and Bub

Before we continue into session, memory, and context, let’s briefly talk about OpenClaw (even though I only saw my first “alive” OpenClaw instance yesterday, driven by MaxClaw).

OpenClaw positions itself as a personal assistant. Assistant means entering daily life. You can think of it like a friend who helps order food or tells you how to write today’s document. Most abilities can be extended through skills. This is deeply tied to model capability, agent progress, and current AI application trends. But when someone opens a real path, the imagination space gets much bigger.

Still, “personal” is OpenClaw’s limitation.

Bub, at least the Bub we have right now, is designed for multi-human or multi-agent collaboration. We started day one in group chats, while still being able to serve one-on-one needs.

To survive in group and multi-party settings, two things matter:

- Build identity awareness.
- Provide effective communication.

The first means distinguishing and understanding most participants, including self. The second means dealing with incomplete context, vague intent, and parallel topics.

As I wrote elsewhere, an agent does not even need to respond to every message. Capability becomes a coexistence problem.

Recommended reading: [Instant Messaging and Socialized Evaluation](/posts/im-and-socialized-evaluation/)

## Session, Memory, and Context

Older designs came from a simple assumption: one session maps to one task. To fit longer interactions into limited windows, we invented compact and summary. To share context branches, we invented fork and merge. To hand over tasks, we got handoff.

When session boundaries started breaking, memory systems were expected to save us: extract preferences, retrieve memories, fill templates, keep an agent “personality” consistent across sessions.

Then context became an even bigger basket, trying to hold sessions, memory, RAG, real-time queries, and everything else with increasingly complex filling strategies.

All these mechanisms try to answer one question: how do we extend infinite history in a finite window?

The issue is that all elegant designs share the same assumption: state must persist, history must not be dropped.

That assumption is expensive:

- Sessions are hard-isolated, so cross-session awareness is weak; multi-topic group chat is even harder.
- Memory drifts, and calibration cost is far higher than expected; you must trust a sidecar that should not break system behavior even when it fails.
- Context management assumes history is monotonic growth, so inflation must always be managed.

We assume the system must remember everything, then add caching, compression, branching. Each layer patches the same premise. But they still cannot carry enough true history.

Recommended reading: [Prometheus Bound](/posts/prometheus-bound/)

## Reframing with Tape and Anchors

A different angle: history is not a burden that must be inherited. It can be a material library loaded on demand.

Tape is simple:

- One endless tape: one perpetual session. Every interaction is appended to logs as facts, never mutated.
- Anchors instead of memory: at phase transitions, write the minimal required state as anchors. Rebuild starts from the latest anchor. History stays, but does not need to be fully loaded.
- Context assembly instead of inheritance: when a new task arrives, do two things only: explore (retrieve raw fragments) and choose (assemble minimally sufficient context).

The value of tape is not inventing a smarter memory trick. It is reducing assumptions. State does not need to persist forever. History does not need default inheritance. Task appears, construct context. Task ends, end it. Next round, start again.

Looking back, tape + anchor gives us a useful model for context management research: easy to understand, expressive enough to represent mainstream solutions, and good enough for rethinking future designs.

Recommended reading: [Reinventing the Punch Tape](/posts/reinvent-the-punch-tape/)

## Closing

Back to the title:

- Once tools enter your hand, they also enter your mind. Capability starts defining problems.
- Knowing when *not* to hammer is a key skill against tool bias.
- Once you truly understand what counts as a nail, and where the hammer ends, you will actively choose problems that are “essentially nails.”
- Or switch to a new hammer.

Side note: until today, I still have not read the implementations of codex / pi-mono / nanobot / openclaw.

Special thanks to [frostming](https://github.com/frostming), [yihong0618](https://github.com/yihong0618), [bub](https://github.com/psiace/bub), and all its contributors.

Thanks to alma, kapy, huluwa, and the creators behind these agents.

Thank you all.
