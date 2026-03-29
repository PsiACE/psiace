+++
title = "The Code of Hammurabi"
description = "From the Code of Hammurabi to human-Agent interaction: proportionality, shared observability, and equal standing between participants in bub."
date = 2026-03-30
slug = "hammurabi-code"

[taxonomies]
tags = ["agent", "bub", "interaction", "observability", "context", "collaboration"]

[extra]
lang = "en"
+++

> Today I want to talk about a few design ideas in [bub](https://github.com/bubbuild/bub) that have endured to this day, along with some of my thoughts on interaction between humans and agents.
> You have probably seen this project mentioned more than once in my previous writing, so besides understanding its design, I also hope you will take the time to read some of its code.

## Introduction

Historical accounts tell us that the Babylonian king Hammurabi had his law code inscribed on black basalt nearly 3,700 years ago.

What, then, was written in that code?
The best-known line is probably "an eye for an eye, a tooth for a tooth."
The Louvre describes one part of it this way:

> Article 196 states: "If a man destroys the eye of another man of equal rank, they shall destroy his eye."
> This article is prominently featured in the augmented reality experience.
> It vividly illustrates a notion of compensation for injury that was characteristic of Semitic societies in the ancient Near East, later giving rise to the principle commonly summarized as "an eye for an eye, a tooth for a tooth."
> In reality, however, the rule was not meant to encourage revenge, but to require that punishment remain strictly proportionate to the offense, neither too light nor too severe.

One is about law, the other about interaction, but they share the same underlying idea: strict proportionality, neither too much nor too little.
That is also the central theme of this essay.

To make the point easier to follow, let us begin with a few small design choices.

## Different Views, Consistent Behavior

In most systems, the interaction views available to humans and agents are completely asymmetric: both can send text and images, but only the agent can call tools.
As a result, it is difficult for a human to directly experience, understand, or reproduce agent behavior in its actual environment.

Bub takes a different approach.
Its tool system is shared by both humans and Bub itself: inputs that begin with a comma, known as Comma Commands, are forwarded as the corresponding tool calls, while unknown commands fall back to Shell.
The views may differ, but from Bub's perspective, Function Calling and what humans see as Comma Commands correspond to the same behavior.

In day-to-day interaction with Bub, when the context is already in poor shape but Bub has not triggered auto handoff in time, we often manually run `,tape.info` and `,tape.handoff`.
That is, in fact, the natural way Bub manages its own context.
Through that shared mechanism, humans and agents naturally develop the same intuition about load and state, and we can directly observe the concrete impact different tools have on Bub.

> P.S. The idea of Comma Commands comes from a 2009 essay, [*Start all of your commands with a comma*](https://rhodesmill.org/brandon/2009/commands-with-comma/).
> One reason for introducing it early on, besides ensuring consistent behavior, was to make Bub feel at home in the command line.
> After all, the command line remains one of the interfaces programmers know best.

## Symmetry of Information

Most systems we have seen in the past were effectively unobservable to both users and agents: stitched-together prompts, invisible memory, and opaque system state.
Users could see that the result was wrong, but had no access to the basis on which it was produced.
In that situation, interaction with an agent loses much of its meaning, because the participants are no longer operating on shared context.

In Bub, all behavior and the state associated with it are recorded on tape, and behavior is allowed to depend only on visible context.
This is deliberate.
Although the context still has to be assembled, the amount of information available to humans and agents is the same; working from the same underlying data, both can understand behavior and verify state.

Put differently, context and observability are structurally aligned.
The context itself is already a natural expression of tracing.
Beyond exporting a familiar Trace UI through dashboards, Bub can also inspect and analyze its own behavior.

One scenario I use frequently is to have Bub go back through poor performances in a group-chat conversation, extract and analyze the relevant execution paths from the actual exchange, determine what caused the failure, and even draw the corresponding DAG.
Because the data underlying that analysis is visible to me as well, no additional trust assumption is required, and real collaboration becomes possible.

> To avoid making this sound too self-contained, here is another example: both codex and bub support a Dollar Mention mechanism, where `$` triggers the progressive loading of skills and loads specific content from skill files into the current context.
> This is a typical form of prompt augmentation.
> What matters more, however, is that the loaded content is equally visible to humans and agents.

## Equality Between the Participants

Traditionally, dialogue between humans and agents is represented as a session, but control over the session belongs only to the human: when a task changes, when the context drifts out of control, and so on.
This further deepens the asymmetry.
The human is expected not only to know everything, but also to manage everything; the top-level user instruction must usually be precise and free of major drift or conflict, while the agent can do nothing but obey within the confines of the session.

The problem with the session model is that it carries an implicit assumption: interaction revolves around a single subject.
That works in a single-user system, but once multiple participants are present, context no longer serves one subject alone, nor can it guarantee task isolation or linear behavior.
If the boundary remains the session, then someone must take responsibility for coordination and maintenance, and that role usually falls to the human.

Bub was designed with a different goal from the outset.
A group-chat environment places much higher demands on the agency of each participant.
In Bub's model, interaction is organized around `turn`.
It does not belong to any one subject; it is simply an action taken within the current context.
With the help of anchor and handoff, Bub can also control the boundaries of the flow in a natural way.

> When we talk about interaction, we often overlook the equality of the two sides involved.
> We say interaction should be human-centered, and now we also say it should serve agents, but interaction itself is something that happens between the participants.

## Interaction, Not the Design of Interaction

We often speak of "interaction design," but when interaction actually takes place, no participant can easily determine its final form.
More often than not, each side simply bears it as it unfolds.

What Bub does is not to propose a new mode of interaction, but to acknowledge the existence of interaction itself and establish constraints around it.

This is where the article ought to end.
It is late into the night once again.
Welcome to follow and star Bub: <https://github.com/bubbuild/bub>.
