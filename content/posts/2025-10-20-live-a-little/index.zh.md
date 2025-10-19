+++
title = "Live a Little · 上篇（2016 – 2021）"
description = "在二十七岁前回看 2016 至 2021 年与代码相伴的日子。"
date = 2025-10-20
slug = "live-a-little-part-1"

[taxonomies]
tags = ["Memoir", "Career"]

[extra]
lang = "zh"
+++

**在代码与青春之间**

> 我即将二十七岁。
> 按新时代的算法，已经稳稳进入「老登」序列。
> 这一年，我的第二份正式工作也满了一年多。
> 回头看，想聊聊那些年我和代码之间的故事。

---

## 2016：少年意气与第一行代码

把时间拨回 2016 年。
那时我沉迷小说，读过的大部头早已按「车载斗量」计。
Ruby 风头正盛，我用 Rails 搭过小站，也在 GitHub 上部署过 Jekyll 生成的静态页。
想写漂亮 UI 的冲动驱使我去学 HTML；
我偷偷读完了 *Digital Design and Computer Architecture* ——一本讲 Verilog HDL 和计算机体系结构的书。
那时我并不真正懂，只是怀着一点少年心气。

---

## 2017 – 2018：大学、算法与初恋

2017 年，我进入大学，主修计算机科学与技术。
学校很大，疫情前的校车也只能遍历小半个校区。
数学天赋平平，但我仍喜欢编程——因为它让我能「造点什么」。

2018 年，我试图认真地学算法与英语，已经在 Linux 环境下生活。
我读 GNU 和自由软件基金会的故事，也在 GNU.org 帮忙校对文章。
那时的我还不会 git 之外的工具，全靠前辈帮我合并推送。
在邮件列表里，我看到俊余的名字——几年后，他做的 WebP 图像服务在推特上火爆一时。

同年我写信给刚落地中国的 [LeetCode 力扣](https://leetcode.cn/)，想参与题解翻译。
Hercy 给我了第一封正式回复。
和 Winston 一起帮我做了 landing 。
如今一晃也结缘七年。

当然，2018 也有更多故事：
我挂了高数，也遇见了现在的女朋友。
那年秋天我和工作室的朋友一起看《昨日青空》，出来吃小吃时我说：

> 「这电影该和女生一起看。」
> 后来我又买了两张票，和学妹二刷——
> 转眼，我们已经在一起七年。

技术上，18 年我第三次重生 GitHub 账号，尝试 Rust 项目 Servo，学 Cargo 命令，修 README 里的构建流程。
当时谁能想到，我未来有一段工作会真正用 Rust 写代码。

---

## 2019：翻译、社区与早期项目

翻译比我想的走得更远。
2019 年，[LCTT](https://linux.cn/lctt/) 仍是国内最活跃的 Linux 中文社区。
我在里面结识了老王和白宦成老师；我们计划合写一本书，虽最终搁浅，但那段共同写作的日子至今难忘。

技术上，Python 当时如日中天。
我学了 Flask、Django、FastAPI 皮毛，用 Cookiecutter 生成项目模板。
后来成为 [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) 的维护者——一个几千 star 的项目。
她和 Pydanny 是有名的「夫妻店」，今天依然活跃。

年底，我修完编译原理课，读 *Crafting Interpreters*，写了个 C 语言项目的模板 [meco](https://github.com/PsiACE/meco) 和玩具语言 [emo](https://github.com/PsiACE/emo)。
那时也尝试 Neo4j 与 NebulaGraph，做过可视化图查询的项目。
我没想到，几年后我真会在图数据库公司工作。

---

## 2020：Rust 之夏与方向初定

2020 准备考研，但心思其实一半在代码。
我从 Python 转向 Rust，入选首届 [开源之夏 OSPP](https://summer-ospp.ac.cn/)，在 Casbin 写了 [casbin-raft](https://github.com/casbin-rs/casbin-raft)，认识了江成和 Hackerchai。
江成后来为我写了推荐信，chai 去了 Kong。
和 OSPP 的缘分甚至更深，一直延续到今天。

同年，我在 Rust 中文社区贡献翻译：
译过 *Writing an OS in Rust* 中的一章，与洛佳结识——后来他做了 [RustSBI](https://github.com/rustsbi/rustsbi)。
我还翻译了 nrc 的 *“Early Impressions of Go from a Rust Programmer”* 。
PingCAP 的 VLDB 论文成为了毕设开题材料。
这个内容在获得授权后发布在了 [PsiACE/TiDB-A-Raft-based-HTAP-Database](https://github.com/psiace/tidb-a-raft-based-htap-database)

毕业设计题是 “基于 Rust 的分布式 KV”——Raft + Bitcask。
熟悉 PingCAP 的同学应该都知道灵感出自何处。
我研究 async-raft（即 [databend/openraft](https://github.com/datafuselabs/openraft) 前身），也给 P 社周边库提 PR。
那年我以个人捐赠者身份支持 [Rust China Conf 2020](https://rustcc.cn/2020rustchinaconf/)，和夏歌、Mike、汉东有了更多交流。
后来，我还做了几年 Rust 中文社区日报编辑。

---

## 2021：转折与第一份工作

考研失败——毕竟我复习间隙还在给 [xi-editor](https://github.com/xi-editor/xi-editor) 修过 lint。
我去 Wasmedge 面试实习，了解到了 WebAssembly 和 ERC20 标准，我修正的方案最后被用于社区。
又从 Meilisearch 和 Hashlink 分叉出 [riteraft](https://github.com/PsiACE/riteraft) 和 [ritelinked](https://github.com/PsiACE/ritelinked)，前者积累 300 多 star，后者成为我下载量最高的 crate 之一。

我也拿到 PingCAP 面试机会，当时项目是给 [Tichi](https://github.com/pingcap/tichi) 做贡献。
练习部署 Prow 时，第一次切身感受国内网络之艰难。
Mini256 就在那个组里——几年后，我在做 GraphRAG 时看到 TiDB 推出 AutoFlow，他也在做 RAG 了。

那段时间，我一边写论文，一边给 [Databend](https://github.com/datafuselabs/databend) 做早期贡献，从 CI 到模糊测试，再到上游的 Arrow 和 SQL 解析器。
那时 Databend 不过 10 人左右。
我加了虎哥好友，只想向技术大佬多学习，没想到真的因此获得了工作机会。
他爽快地约我在武汉见面。
我至今记得那天的阳光——
那是创业者最有光的年纪。

6 – 7 月间，我在 Databend 上下游提了约 40 个 PR。
就这样，我加入了这个立志打造“中国版 Snowflake”的团队，开始了我的第一份真正意义上的工程师工作。

---

> *未完待续 —— Part 2 将讲述 2022 至 2025，从 Databend 到 Apache OpenDAL 等这些年的故事。*
