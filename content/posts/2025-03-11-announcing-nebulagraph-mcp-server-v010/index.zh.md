+++
title = "NebulaGraph MCP Server 正式开源！探索 AI+图数据库无限可能"
description = "基于 NebulaGraph 3.x 的 MCP Server，作为 NebulaGraph X MCP 生态中的第一个基础组件。"
date = 2025-03-11
slug = "announcing-nebulagraph-mcp-server-v010"

[taxonomies]
tags = ["MCP", "LlamaIndex", "Python", "NebulaGraph"]

[extra]
lang = "zh"
+++

## ▌一、背景

过去几周，Model Context Protocol (MCP) 在技术社区中引发了广泛的讨论和关注。借此机会，我参与了几个相关的开源项目，包括为 **LlamaIndex 官方仓库贡献了 McpToolSpec 实现**，以及和 Xuanwo、FrostMing 合作开发了一版 **Model Context Protocol Server for Apache OpenDAL™**。

MCP 是目前唯一一个在生态上具有优势的标准。在这一背景下，我们 **基于 NebulaGraph 3.x 实现了一个简单的 NebulaGraph MCP Server，作为 NebulaGraph X MCP 生态中的第一个基础组件，供大家探索 AI 与图数据库结合的可能性**，希望能够看到更多在这个模式下的有趣工作。

## ▌二、Model Context Protocol (MCP)

MCP 是由 Anthropic 团队推出的一项开放协议，旨在为 AI 系统提供统一的、高效的方式访问多种数据资源。通过采用客户端-服务器架构，MCP 将数据访问标准化，解决了传统 AI 系统在不同数据源之间的碎片化问题。

### MCP 核心特点

1. **标准化的通信方式**：通过 MCP，AI 助手能够有效地访问各种数据源，比如本地数据、远程服务和企业工具。
2. **开放性与生态优势**：目前 MCP 社区中已有近 1000 个 MCP Server 实现，覆盖搜索、天气、数据库等多个领域，支持工具的快速接入。
3. **灵活的架构**：通过定义客户端和服务端的交互协议，MCP 为开发者提供了构建可扩展、可复用系统的基础。

虽然目前在安全性和可靠性上仍有一些挑战，但随着协议规范的完善和成熟开发模式的引入，这些问题将逐步得到解决。

## ▌三、NebulaGraph MCP Server 功能

由于最近一段时间一直围绕 GraphRAG 和 Agentic Workflow 做一些工作，利用大模型和智能体进行图上数据的洞见和挖掘是一个非常重要的议题。为此，我快速开发了 NebulaGraph MCP Server，以支持 NebulaGraph 3.x 作为工具接入 MCP 生态，供语言模型（如 Claude、GPT 等）调用和使用。

目前 **NebulaGraph MCP Server 基于 FastMCP 实现，遵循 MCP 的核心规范，旨在提供高效、轻量的图数据库连接服务。** 通过将 NebulaGraph 的功能暴露为标准化的工具接口，该 Server 能够让大模型轻松调用 NebulaGraph 数据，实现简单的图探索任务。

- **多种传输方式**：
  - 支持 stdio 和 SSE 两种传输模式，满足不同开发和部署场景的需求。
- **基础图探索能力**：
  - 图空间（Graph Space）列出：允许模型查询可用的图空间。
  - 模式（Schema）查询：支持查询指定图空间的模式定义。
  - 查询执行（Query Execution）：支持通过 MCP Server 执行 NebulaGraph 查询。
- **内置算子模板**：
  - 实现了路径搜索和邻居发现等常用操作的模板，方便语言模型按需调用这些工具，快速获取图数据的初步洞察（Insight）。

为了展示它的效果，我基于 LlamaIndex 中的 McpToolSpec 和 ReActAgent 构建了一个简单的示例，下面是对应的截图：

![LlamaIndex with NebulaGraph MCP](llamaindex-with-nebulagraph-mcp.png)

## ▌四、结语

**NebulaGraph MCP Server** 是对 MCP 生态的一个初步尝试，旨在为语言模型和图数据库的结合提供一个起点。随着协议的逐步成熟和生态的扩展，我们期待它能够在更多真实场景中发挥价值。如果您对这一方向感兴趣，欢迎一起探索、尝试！
