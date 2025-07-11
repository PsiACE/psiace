---
title: "Building a Cloudflare AI Gateway integration for LlamaIndex"
description: "A wrapper that makes LlamaIndex work with Cloudflare AI Gateway for automatic fallback, caching, and load balancing across multiple LLM providers."
slug: "llama-index-cloudflare-ai-gateway"
publishDate: 2025-07-11
tags: ["AI", "LLM", "Cloudflare", "LlamaIndex", "Orchestration"]
draft: false
---

Single LLM providers are fragile. [OpenAI outage](https://status.openai.com/)? Your app dies. [Anthropic rate limits](https://status.anthropic.com/)? Users wait. It's annoying.

I wanted multi-provider orchestration without the complexity. [Cloudflare AI Gateway](https://developers.cloudflare.com/ai-gateway/) looked perfect—automatic fallback, caching, load balancing. But no [LlamaIndex](https://docs.llamaindex.ai/) integration.

So I built one.

## The Problem

Cloudflare AI Gateway is smart. It handles:

- Automatic provider fallback
- Built-in caching and rate limiting
- Load balancing across providers
- Unified API interface

But LlamaIndex LLMs make direct HTTP requests to provider APIs. Cloudflare expects a different format.

> Cloudflare provides an [OpenAI-compatible API](https://developers.cloudflare.com/ai-gateway/chat-completion/), but I wanted something more flexible. Compatible often means limited.
> And Cloudflare also provides a [Vercel ai-sdk integration](https://developers.cloudflare.com/ai-gateway/integrations/vercel-ai-sdk/), but I save my life by using Python.

## The Solution

A wrapper that sits between LlamaIndex LLMs and their HTTP clients. Intercepts requests, transforms them for Cloudflare, handles responses.

```python
from llama_index.llms.cloudflare_ai_gateway import CloudflareAIGateway
from llama_index.llms.openai import OpenAI
from llama_index.llms.anthropic import Anthropic
from llama_index.core.llms import ChatMessage

# Create regular LlamaIndex LLMs
openai_llm = OpenAI(model="gpt-4o-mini", api_key="your-key")
anthropic_llm = Anthropic(model="claude-3-5-sonnet", api_key="your-key")

# Wrap with Cloudflare AI Gateway
llm = CloudflareAIGateway(
    llms=[openai_llm, anthropic_llm],  # Try OpenAI first, then Anthropic
    account_id="your-cloudflare-account-id",
    gateway="your-gateway-name",
    api_key="your-cloudflare-api-key",
)

# Use exactly like any LlamaIndex LLM
messages = [ChatMessage(role="user", content="What is 2+2?")]
response = llm.chat(messages)
```

Drop-in replacement. Zero code changes.

## What It Does

**Core features:**

- Automatic provider detection and configuration
- Built-in fallback when providers fail
- Streaming support (chat and completion)
- Async/await compatible

**Tested providers:**

- [OpenAI](https://platform.openai.com/), [Anthropic](https://www.anthropic.com/)

**Also supported:**

- [Google AI Studio](https://aistudio.google.com/), [DeepSeek](https://platform.deepseek.com/), [Grok](https://x.ai/)
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service), [Perplexity](https://www.perplexity.ai/), [Replicate](https://replicate.com/)

## Try It

Still a planned PR ([#19395](https://github.com/run-llama/llama_index/pull/19395)), but functional:

```bash
git clone <repository-url>
cd llama-index-llms-cloudflare-ai-gateway
pip install -e .

export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
export CLOUDFLARE_ACCOUNT_ID="your-id"
export CLOUDFLARE_API_KEY="your-key"
export CLOUDFLARE_GATEWAY="your-gateway"

uv run pytest tests/
```

May not be production-ready, but good enough to experiment with. Check out the [LlamaIndex integrations repository](https://github.com/run-llama/llama_index/tree/main/llama_index/llms) for other LLM providers.

---

## References

- [Cloudflare AI Gateway Documentation](https://developers.cloudflare.com/ai-gateway/)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [LlamaIndex LLMs Guide](https://docs.llamaindex.ai/en/stable/module_guides/models/llms/)
