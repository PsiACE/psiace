+++
title = "Prometheus Bound"
description = "Sessions, memory, and context for models and agents: construct, don't inherit."
date = 2026-02-16
slug = "prometheus-bound"

[taxonomies]
tags = ["agent", "session", "memory", "context", "architecture", "bub"]

[extra]
lang = "en"
+++

> This piece is dedicated to bub, and to my friends.

Over the past week, we validated our earlier idea of punch tape and anchors on bub for the first time. Praise Ming; I think everyone can also read his article, "What does it take to create a lobster?"

Back to this post: I want to discuss another topic. What do sessions, memory, and context mean to a model, or to an agent?

> In Greek mythology, Prometheus brought fire to humanity, and was then chained to the Caucasus, enduring punishment day after day.

To me, this is a metaphor for reality.

![Source: my tweet from last October](prometheus-tweet.png)

---

## Session, a Concrete Problem

In the chatbot worldview over the past few years, a session has been the key unit for switching tasks. That led to isolation between sessions. Even today, when openclaw is everywhere, we are still deeply influenced by it:

> Question: When a user says "switch topics / start over", the process has already fixed the session at startup. Switching a symlink within this turn can only affect the next turn. In your AI-native picture, how do you make "this single message" start from a new session immediately? In group chats, multiple topics often run in parallel. What session organization do you recommend?

(Background: from day one, bub grew up in group chats. I call this "socialized evaluation". It's a smarter approach, and if I get the chance, I'll write more about it.)

A session is a form of hard isolation. That means sessions do not perceive each other. A session can only move forward until the task is done, or until people get bored, but context length is limited.

In the past, we've seen a few session patterns:

- To support longer context in a single session, we got compact and summary.
- To let sessions share the same ancestors and descendants, we got fork and merge.
- To reduce the complexity of the first two, we got handoff. Punch tape and anchors are also influenced by this.

These approaches only address problems within a single session. What should we do when the problem is cross-session?

## Memory, a Failed Prototype

Even though memory has been extremely popular over the past year, and many of my friends and colleagues have invested a lot of experience into it, my evaluation of memory is exactly what the title suggests.

Memory mainly targets consistency in generation, and it roughly falls into two categories:

- If conversations happen within the same system, how do we keep consistency?
- If conversations happen across different systems, how do we keep consistency?

Let's look at how a typical memory system works:

- When a user has a conversation, relevant corpora and preferences are extracted by the model and routed to a memory sidecar for retrieval.
- Given relevance to the user's question and the context window, results are ranked and trimmed, then filled into a generation template.
- The template guides the model's generation.

Cost is deterministic. Most memory systems claim that by introducing a smaller model or pre/post steps, they can significantly reduce token cost and latency (for example, a common trick is to drop the facts associated with each memory item) while achieving good enough quality.

But what matters is another point: consistency is not free:

- Extraction is a lossy process, and we require the model to participate deeply in it. If you've ever criticized hallucinations, what makes you accept the extraction step?
- User preferences are broad and not constant. The investment needed to calibrate this will far exceed imagination. If you've looked at knowledge graphs or GraphRAG, you can easily foresee this.
- Most memoryless approaches (for example, Markdown-based ones) are essentially embeddingless approaches. They still cannot solve distortion and drift when switching models.
- As a sidecar, failure should not affect system behavior. So you may not get the consistency you expect.

Will the token and time savings from the past come back at some point? Memory looks full of difficulties. Then what about context, could it be another bright road?

## Context, Another Sugar-Coated Bullet

In the established meaning of context engineering, it contains everything: the sessions and memory mentioned above, external RAG systems, real-time queries on the internet, and knowledge from various business systems.

It's hard for me to imagine anything that cannot be put into this basket. So we can simply assume that, in this worldview, context will keep expanding until it exceeds a fixed window limit. That's also where most people's obsession with context management begins: truncate, add retrieval constraints, add hand-coded rules, and try to find a large enough, high-quality context to solve the problem.

I want to offer two counterexamples:

- In a well-known evaluation of long-context capability, besides the GPT family, most models show cliff-like quality degradation as context grows. And because each model has a different capability boundary, context management can hardly be directly portable across all models and agent systems.
- Another example is "lobsters attacking the moon". A Kimi staff member once suggested that users should use caching mechanisms to design lobsters, and avoid certain time periods to release load. The complexity of context management makes this request almost absurd. I would even criticize it as a form of laziness.

Abstraction leakage is a serious system design problem. When we rely on certain established context management mechanisms to handle all of this, it also means there will be enough ways to break system reliability.

## Smarter, With Fewer Assumptions

From the beginning, bub was not designed as a "persistent conversation system". We designed it to work over a sufficiently long context, an endless tape. On day one it had to face socialized tasks in group chats. Problems keep appearing, tasks keep forming, and then keep ending. In such a diverse and complex setting, every turn may face a new goal. It does not, and cannot, require a state that continues forever, and it does not even require a conversation ancestor that must be inherited.

Looking back at the idea that once scared me to create, an endless punch tape with anchors on it has worked well on bub. When we cross context boundaries or hit system failures, it gives us a chance to have repair methods that are simple and reliable enough.

But in real-world tasks, there is no punch tape, and there will not truly be an anchor at some milestone. The point is an action: construct, not inherit. When a task appears, as humans we do not shove all history into the window. We do two things: explore and choose.

- Explore may include history, external systems, memory, or even real-time queries.
- Choose means discarding most irrelevant content, keeping only the minimal sufficient material.

Context engineering defaults to increment, extension, and managing expansion. It assumes state must be maintained, so it introduces caching, extraction, merging, compression, and forking. Every layer is trying to patch the same premise: history cannot be dropped. But the reality is that they cannot carry enough history.

Practice on bub gave me a simpler answer: history can be dropped. More precisely, history does not need to be inherited by default. It's just a library of materials. Query it when needed, ignore it when not.

This is also where tape matters. It's not about recording everything; it's about enabling "read on demand". It turns state from an "ongoing burden" into an "optional resource". When context is no longer a monotonic function, cache is just an optimization, not a lifeline; memory is just an index, not a personality; session is just a boundary, not an identity.

Being smarter does not mean introducing more mechanisms. It means assuming less.

## Simplicity

When I wrote down the title, "Prometheus Bound", I thought I was criticizing a kind of bondage.

We are used to metaphors, imagining the model as suppressed fire, a force constrained by engineering systems. But maybe the problem is not that dramatic. The model is not imprisoned. It is just misused within a wrong organization.

Task appears, construct context, complete task, end.
Next turn, start over.
When we stop building systems on top of "persistent state", a lot of complexity disappears naturally.

If the system is clear enough, we don't need myths.
And we don't need Prometheus.

---

Of course, every system exists because there were real problems it tried to solve. This post contains a lot of criticism to express a viewpoint, but that does not mean those systems are meaningless.

Again, thanks to bub and my friends, for giving me a chance to feel and express all of this more deeply.

## Recommended Reading

- [What does it take to create a lobster?](https://frostming.com/posts/2026/create-a-claw/)
- [Reinvent the punch tape](https://psiace.me/zh/posts/reinvent-the-punch-tape/)
- [bub](https://github.com/psiace/bub)
- [AI Programming Is a New Framework](https://www.piglei.com/articles/ai-programming-is-a-new-framework/)
