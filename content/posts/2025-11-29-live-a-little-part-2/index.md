+++
title = "Live a Little · Part 2 (2021–2025)"
description = "Fragments from 2021–2025: Databend, OpenDAL, Macau school years, NebulaGraph, and Fusion GraphRAG."
date = 2025-11-29
slug = "live-a-little-part-2"

[taxonomies]
tags = ["Memoir", "Career"]

[extra]
lang = "en"
+++

**A Gambler's City Chronicle**

This piece is 2021–2025, the years when most overlaps with friends began.
2021 was a database boom, 2024 an AI frenzy.
I caught both, never won big, but stayed at the table.
From 2022 to 2024 I lived in a gambling city; the title comes from there.
Names may be missing, but the people are not forgotten.

---

## Addenda

I once wrote some frontend.
Added the ACF2+ pitch detection algorithm in JS to pitchfinder and built a small audio and visualization demo.
Tried music OCR: read sheet music, turn it into notes, play with a Java library.
Did simple image search by extracting features and comparing similarity, testing many combinations out of curiosity.

---

## Databend

I had no database background, was the first new grad, and skipped the interview.
When people asked how, I had no clear answer; I am just grateful for the trust.

Work split between engineering and community.
Engineering was repo-level refactors, dependency upkeep, and occasional new features.
Community came from liking to write and share; by the time I went back to school it had become a main track.

Early on I moved tests from source files to external unit tests to make builds faster and cleaner; it worked but added file switching and mental load.
As the codebase grew, we split things again to improve build parallelism and quality.
I joined the big refactors led by sundy-li: he found `arrow2` from a reddit thread, migrated, then rebuilt again after Chi's type-level ideas.

Cloud work with flaneur and Zhihan taught me cadence through their OKR alignment docs; soon we had an internal cloud prototype we could play with.
For benchmarks I proposed writing results as json in the repo for visualization.
Early Databend was a large practice field; I touched most corners and learned how a data system breathes.

---

## Apache OpenDAL

I met Xuanwo when he was handling the website move.
The storage access layer then was dal, designed by Zhao to favor object storage while staying HDFS friendly.
Xuanwo suggested a rewrite into a general interface, so dal2 was built and later spun out as opendal.

Cai built the early WebHDFS integration; Databend aslo added Hive support.
Many data companies had similar needs, so opendal drew attention; with tison's help it entered foundation incubation.

Before opendal I was just a salaried engineer writing open source.
Here I felt trust and cooperation without a profit goal — “community over code.”

---

## Macau School Years

After a year of full-time work I went to Macau for Applied Math and Data Science.
Maybe it was too much time indoors, maybe feeling not good enough; I wanted to get out.

Math classes were heavy; convex optimization cost hair but I made it through.
AI and LLM work entered daily life: Meta's SAM for segmentation, CLIP for interactive captioning, a small nanogpt with tweaks to model structure, optimizers, and schedulers.

I stayed close to Databend: compiler and Rust optimizations with a few talks; studying lakeFS and HuggingFace data; KubeSphere 4.0 integration and a Databend playground; an online hackathon; most Chinese docs plus an LLM workflow to translate English docs; I even skipped class to join the debate on opening enterprise source.

At ApacheCon 2023 I met Xuanwo in person; we each gave an OpenDAL talk.
He sent me wedding candy; I sometimes acted as his merge bot.
I also met tison, saka, flaneur, xp, and went to the Summer Palace with TCeason.
Later I met Zhihan and Eric; at Rust conf I finally matched RisingWave IDs to faces.

In 2024, after a trip to Japan, I focused on a thesis about modern cache replacement for layered storage.
Talked once with juncheng, who led sieve and s3fifo and kept designs minimal.
Graduation forced me to narrow focus; my advisor's calm helped.
I graduated and left Databend.
My last public talk there was “Caching for Modern Layered Storage.”

---

## NebulaGraph

Leaving Databend meant job hunting again.
I still wanted data infra and even considered less technical roles.
The market was cold; two peer companies took me to CXO rounds with no offer.
Big-tech interviews were flat: interviewers were lukewarm about my background, and I did not lean into algorithms or playbook questions.
Friends pointed me to web3; offers were high but compliance risks kept me away.

The turn came at ApacheCon Hangzhou.
Friends Dinah and Yanli told me NebulaGraph's GenAI team was hiring; the lead was long-time Twitter friend wey-gu.
The final round with Sherman included a spoken algorithm question — not something I expected in a culture-fit chat.

Before joining I went to Shanghai for Rust Conf and to spot the office; finally met yihong0618, an interesting soul.
Met RisingWave friends, including MrCroxx (foyer-rs) and Runji (arrow-udf, later at deepseek).
Six months later at KCD Beijing I visited their office and tried the dried fish.

At PyCon China 2024, wey gave a keynote; I met frostming and Jintao and took a photo with pink-haired saka.
At Rust Conf 2025 I met Leiysky and Andy; they and tison were starting a new product.
Later that year at PyCon I spoke on coding agents and met many friends from chat groups.

Side projects:
- First MCP integration for Llama Index, with the initial implementation contributed to the official repo.
- First agentclientprotocol Python SDK, adopted as an official SDK with help from JetBrains friends.
- Visited their Shanghai office and carried home a basket of swag.

We moved from Pudong to Nanjing West Road, from a dark room to sunlight.
Dinah left for OceanBase; wey left to build nowledage memory.
Yanli and I stayed at NebulaGraph, kept working on GraphRAG and agents, and shipped Fusion GraphRAG.
Shao handled end-to-end evaluation, insisting recall and accuracy come first.
Fusion GraphRAG keeps onboarding cost close to vector or full-text RAG and reaches 95%+ QA accuracy in some domains.

---

## Closing

Time has moved to late 2025.
That is about it.
