+++
title = "Reinventing the Punch Tape"
description = "An Agent has only one deterministic session. It is perpetual—never ending, never forking, only moving forward."
date = 2026-01-28
slug = "reinvent-the-punch-tape"

[taxonomies]
tags = ["agent", "memory", "context", "architecture", "log", "session"]

[extra]
lang = "en"
+++

> Hi, I'm [PsiACE](https://github.com/PsiACE). This idea was born about 4 months ago when I was still working toward better GraphRAG. I have some experience with Agents and databases over the past few years—feel free to read my previous posts.

## TL;DR

Agent systems tend to grow complex: forking, rollback, short-term and long-term memory, carefully designed compression and truncation.

The more engineering invested, the harder the behavior becomes to predict. I think it's time to reinvent the punch tape: an Agent has only one deterministic session. It is perpetual—never ending, never forking, only moving forward. On this endless punch tape, you can always reliably retrieve the small piece of context you need most at that moment.

**Let interactions happen as naturally as in the real world.**

Real human interaction never truly forks into multiple equally real timelines, nor does it erase what has happened through rollback. Conversations may wander off-topic, correct mistakes, switch tasks, or start a new phase—but they always happen along the same continuous timeline.

## The Endless Tape

**The foundation of an Agent should be a long tape**—yes, a log.

Beyond simple conversation history, the log should record what happened: a tool result, a key decision, a phase transition—all written as facts. Once a fact is written, it is never modified or replaced with a lossy substitute.

You can always go back to any point in time and see what actually happened—not a version that was later revised, compressed, or rewritten. The purpose of the log is not just to let the model read through history, but to make the Agent's behavior easier to verify.

On top of this long tape, **the Agent computes state**.

Naturally, we should use state computed from the log—instead of "memory"—to support queries and context assembly, rather than replacing facts with summaries or compressed content. It's somewhat like a materialized view in a database: it can be discarded, it can be rebuilt, and it should be able to explain where each piece of state comes from.

At any moment, the system simply picks a new starting point, rebuilds state from the log, and continues execution.

Anchors are introduced precisely for this purpose.

If you rebuild state from the beginning of the log every time, the system eventually becomes unwieldy and hits context limits. **Anchors provide a set of explicit rebuild starting points**, expressing "from here, the state is stable enough to continue working." Anchors don't delete history, nor do they summarize it—they just tell the system where to start counting.

An anchor is typically created by a handoff. When the Agent recognizes that the phase has changed, or that continuing from the current rebuild starting point would make state messy, it performs a handoff: it writes the minimal structured state still necessary for the next phase into the log, creates a new anchor, and subsequent state rebuilds start from that new anchor.

What gets packaged here is not a summary of history, but state oriented toward the next phase; history remains complete in the log. The thread doesn't break, nor does it fork—it just keeps moving forward.

## The Wheel Rolls Forward

**Agents don't really fork.**

Forking essentially creates multiple equally real futures, but the real world has only one "now." You can change direction, but you can't branch what has already happened into another timeline.

Many scenarios that seem to require forking are more naturally expressed as handoffs. You don't need to create a parallel thread—you just acknowledge that you've entered a new phase. You're still moving forward on the same thread, just rebuilding state from a new anchor. The past still exists in the log, ready to be queried and referenced at any time, but it doesn't need to become a parallel world.

Similarly, **Agents don't really roll back.**

Rollback means undoing what has already happened, but in real interaction, correction isn't done by erasing the past—it's done by adding new facts. From an engineering perspective, rollback changes state, but we only allow state to be changed by new facts; we don't allow old facts to disappear.

The essence of "rollback requirements" is a context assembly problem. You want to ignore certain fragments in this execution, emphasize others, and guide the model to reason in a different direction. This doesn't require modifying the log or returning to an old state—it just requires selecting a different working set when assembling context.

**Agents also don't really rely on various "memory tricks."**

Multi-layer summaries, repeated compression, and complex heuristics may work in the short term, but over time they introduce noise, uncertainty, and inexplicability. It becomes harder and harder to distinguish what is fact, what is a model-generated generalization, and what is residual error from compression.

Retrieval and recall from history are still necessary. You can pull original text fragments from the same thread's history, or pull evidence from external data sources, and temporarily assemble them into the current context. But lossy compression should never quietly replace history.

## The New Punch Tape Computer

This design thus becomes simple.

Maintain an endlessly forward-moving thread, continuously appending facts. Use anchors to express phase transitions, use context assembly to control the window for each execution, allow on-demand reading from history and external data sources, and prevent lossy results from becoming new truth.

Agents should fully leverage everything we've built in storage, computation, and other domains. "More reliable interaction" will beat "smarter memory."
