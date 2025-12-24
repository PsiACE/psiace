+++
title = "On Testing Confidence"
description = "Testing sets a trust boundary between maintainers and users by aligning expectations, not chasing coverage."
date = 2025-12-25
slug = "testing-confidence"
draft = false

[taxonomies]
tags = ["Engineering Confidence"]

[extra]
lang = "en"
+++

In the long process of building software systems that others can rely on, I gradually realized that testing is not merely a QA tool.
It is an engineering method for establishing a trust boundary between maintainers and users.

When a system lacks this boundary, complexity does not disappear.
It shifts into maintainer judgment, user adoption cost, or collaboration friction on both sides.

For maintainers, tests determine whether a system can keep evolving.
For users, tests determine whether a system is worth relying on.

"Testing confidence" does not come from a metric.
It comes from whether these two perspectives are clearly aligned through tests.

## Testing is not the same as coverage

In practice, testing is often reduced to metrics: coverage, CI pass rate, regression counts.
These metrics are valuable to maintainers because they reduce uncertainty when changing code.

But they do not answer the question users really care about:

> When a system is placed in real environments, real load, and real dependencies, is its behavior predictable?

Once others use a system, their usage almost always deviates from the designer's intent.
The value of tests is not to enumerate all paths.
It is to use executable cases to make expected behavior and boundary conditions explicit and fixed.

When those boundaries are clear:

- Maintainers know which behaviors must not be broken.
- Users know which behaviors they can rely on.

From this perspective, tests are not an accessory to code.
They are a layer that connects maintainers and users.

## Testing is a long-term constraint on semantics

In Databend, we rely heavily on test cases already validated by existing database systems.
We also track key benchmarks over the long term to lock in our commitment to established semantics and standards.

One important fact is this:
the primary source of system complexity is not implementation difficulty, but the stability of semantics over time.

For example:

- Whether to return a result or an error under certain exceptional conditions.
- Whether different execution paths satisfy the same invariants.
- Whether behaviors that are inelegant but widely used must remain compatible.

If these semantics are not fixed by tests, they become a hidden burden for maintainers.
Every change then depends on memory and experience to judge, "Will this break something?"

For users, semantic drift is even more direct.
The same usage can produce different results across versions.

Therefore, the role of testing here is not "checking for bugs."
It is:

- Providing clear evolution boundaries for maintainers.
- Providing stable behavioral expectations for users.

This is why systems like MySQL and SQLite treat tests as high-value assets.
Tests carry long-term promises to users.

## Testing aligns maintainer judgment with user reality

In Apache OpenDAL's CI, we include hundreds of tests across multiple platforms and services.
In practice, a single contributor rarely has the time to assemble the full environment of dependencies and services.

If Databend's tests mainly stabilize internal and external semantics, then in Apache OpenDAL, tests are more about bridging the gap between maintainer judgment and user reality.

In the object storage ecosystem, many services claim to be "S3 compatible."
For maintainers, implementing the spec can easily lead to the assumption that the system "should work."

But users do not operate at the spec level.
They use real accounts, real services, and real failure modes.
Many issues surface precisely in that gap between assumption and reality.

Therefore, in OpenDAL, we insist on:

- Using real services for tests whenever possible.
- Not treating docs or compatibility claims as engineering facts.
- Keeping failure cases long term as part of regression tests.

The value of these tests is:

- They constrain maintainers' overly optimistic assumptions about the external world.
- They give users a clear signal about which behaviors are validated in real environments and can be relied on.

Here, tests are not about "proving correctness."
They are about keeping maintainer judgment consistent with user reality.

## Testing confidence: a shared understanding of failure

Across these practices, I have formed a stable view:

> Testing confidence is not that a system "rarely fails," but that when failures happen, maintainers and users share a consistent understanding of their nature.

When a behavior is covered by tests:

- For users, a failure means a bug.
- For maintainers, fixing it is a clear engineering responsibility.

When a behavior is not covered by tests:

- For users, it should not be treated as a system promise.
- For maintainers, it should not be assumed as behavior to keep compatible long term.

Tests make this distinction clear, executable, and regression-ready.
They also significantly reduce friction in expectations on both sides.

## Conclusion

From an engineering perspective, testing is neither a tool only for maintainers nor a mechanism only for users.
It is a structure that helps both sides reach consensus on the same behavioral boundaries.

It turns implicit assumptions into explicit constraints.
It turns personal experience into a sustainable engineering boundary.

For me, no matter which layer the system lives at, testing ultimately serves one thing:

> To make systems predictable when they are depended on,
> and to make maintenance sustainable over the long run.
