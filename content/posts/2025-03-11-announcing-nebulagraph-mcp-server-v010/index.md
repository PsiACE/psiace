+++
title = "Announcing NebulaGraph MCP Server v0.1.0"
description = "I implemented a simple NebulaGraph MCP Server based on NebulaGraph 3.x, serving as the first foundational component in the NebulaGraph X MCP ecosystem."
date = 2025-03-11
slug = "announcing-nebulagraph-mcp-server-v010"

[taxonomies]
tags = ["MCP", "LlamaIndex", "Python", "NebulaGraph"]

[extra]
lang = "en"
+++

Over the past few weeks, **Model Context Protocol (MCP)** has sparked significant discussion and attention within the tech community. As part of this momentum, I contributed to several related open-source projects, including the [McpToolSpec implementation for the LlamaIndex official repository](https://github.com/run-llama/llama_index/pull/17795) and collaborated with Xuanwo and FrostMing to develop a version of the [Model Context Protocol Server for Apache OpenDAL™](https://github.com/Xuanwo/mcp-server-opendal).

MCP is currently the only standard with an ecosystem advantage. In this context, I implemented a simple **NebulaGraph MCP Server** based on NebulaGraph 3.x, serving as the first foundational component in the NebulaGraph X MCP ecosystem. This server is intended for exploring the potential of combining AI and graph databases, and I hope to see more exciting work emerge under this paradigm.

## About Model Context Protocol (MCP)

MCP is an open protocol introduced by the Anthropic team, designed to provide AI systems with a unified and efficient way to access various data resources. By adopting a client-server architecture, MCP standardizes data access, addressing the fragmentation issue of traditional AI systems dealing with diverse data sources.

The core features of MCP include:

1. **Standardized Communication Protocol**: With MCP, AI assistants can effectively access various data sources, such as local data, remote services, and enterprise tools.
2. **Openness and Ecosystem Advantage**: The MCP community currently boasts nearly 1,000 MCP Server implementations, covering domains such as search, weather, databases, and more, enabling rapid tool integration.
3. **Flexible Architecture**: By defining the interaction protocol between clients and servers, MCP provides developers with the foundation to build scalable and reusable systems.

While challenges remain in terms of security and reliability, these issues are expected to be resolved over time with improved protocol specifications and the adoption of mature development practices.

## Implementation and Features of the NebulaGraph MCP Server

Recently, I have been working on GraphRAG and Agentic Workflow, focusing on deriving insights and mining graph data using large models and intelligent agents. To support this, I quickly developed the **NebulaGraph MCP Server**, which integrates NebulaGraph 3.x into the MCP ecosystem, enabling language models (like Claude, GPT, etc.) to call and use it.

Currently, the NebulaGraph MCP Server is implemented based on **FastMCP**, adhering to the core MCP specifications. It aims to provide an efficient and lightweight graph database connection service. By exposing NebulaGraph’s functions as standardized tool interfaces, the server empowers large models to easily access NebulaGraph data and perform basic graph exploration tasks.

### Features:

1. **Multiple Transmission Modes**:

   - Supports **stdio** and **SSE** (Server-Sent Events) transmission modes to cater to different development and deployment scenarios.

2. **Basic Graph Exploration Capabilities**:

   - **Graph Space Listing**: Allows models to query available graph spaces.
   - **Schema Querying**: Supports querying the schema definitions of specific graph spaces.
   - **Query Execution**: Enables executing NebulaGraph queries through the MCP Server.

3. **Built-in Operator Templates**:
   - Implements templates for common operations like path search and neighbor discovery, allowing language models to quickly call these tools as needed and gain initial insights into graph data.

To demonstrate its effectiveness, I built a simple example using LlamaIndex’s McpToolSpec and ReActAgent. Below is a screenshot:

![LlamaIndex with NebulaGraph MCP](llamaindex-with-nebulagraph-mcp.png)

## Conclusion

The **NebulaGraph MCP Server** is an initial attempt to contribute to the MCP ecosystem, aiming to provide a starting point for combining language models and graph databases. As the protocol matures and the ecosystem expands, I look forward to seeing it deliver value in more real-world scenarios. If you are interested in this direction, feel free to explore and experiment together!

---

For more details, check out the original repository [here](https://github.com/PsiACE/nebulagraph-mcp-server).
