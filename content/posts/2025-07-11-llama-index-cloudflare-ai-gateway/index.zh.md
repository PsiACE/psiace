+++
title = "让 LlamaIndex 接上 Cloudflare AI Gateway"
description = "一个轻量封装，把多个 LLM 服务放进 Cloudflare 的网关，自动兜底、缓存、限流。"
date = 2025-07-11
slug = "llama-index-cloudflare-ai-gateway"

draft = false

[taxonomies]
tags = ["AI", "LLM", "Cloudflare", "LlamaIndex", "Orchestration"]

[extra]
lang = "zh"
+++

## 为什么折腾这个

单供应商的 LLM 太脆弱：OpenAI 宕机、Anthropic 限流，就等于业务停摆。Cloudflare AI Gateway 给了一个诱人的承诺：

- 多家模型的统一入口；
- 内置缓存、限流、熔断；
- 请求失败自动切换。

问题是，LlamaIndex 的 LLM 调用直接命中各家 API，没法自适应 Gateway。我需要一个中间层，让原有代码不改，直接享受多云编排。

## 解决方案

写了一个轻量 wrapper：

```python
from llama_index.llms.cloudflare_ai_gateway import CloudflareAIGateway
from llama_index.llms.openai import OpenAI
from llama_index.llms.anthropic import Anthropic

openai_llm = OpenAI(model="gpt-4o-mini", api_key="your-key")
anthropic_llm = Anthropic(model="claude-3-5-sonnet", api_key="your-key")

gateway_llm = CloudflareAIGateway(
    llms=[openai_llm, anthropic_llm],
    account_id="your-cloudflare-account-id",
    gateway="your-gateway-name",
    api_key="your-cloudflare-api-key",
)

resp = gateway_llm.chat([ChatMessage(role="user", content="2 + 2 = ?")])
```

作用就是：截住 LlamaIndex 发出的请求，改写为 Cloudflare 期待的格式，处理返回值。原始业务代码不用动。

## 能做什么

- 顺序尝试多个模型，失败自动换下一个；
- 支持 Cloudflare 的流式接口、异步调用；
- 统一注入鉴权、重试、日志；
- 经过实测的模型：OpenAI、Anthropic；
- 理论兼容：Google AI Studio、DeepSeek、Grok、Azure OpenAI、Perplexity、Replicate 等。

## 如何体验

PR 在提审（[#19395](https://github.com/run-llama/llama_index/pull/19395)），不过代码已经能跑：

```bash
git clone <repo>
cd llama-index-llms-cloudflare-ai-gateway
pip install -e .

export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
export CLOUDFLARE_ACCOUNT_ID=...
export CLOUDFLARE_API_KEY=...
export CLOUDFLARE_GATEWAY=...

uv run pytest tests/
```

## 注意事项

- Cloudflare 虽然提供 OpenAI 兼容接口，但做中间层能解锁更多功能（自定义头、特定路由、日志追踪）。
- 多模型编排别忘了考虑一致性：模型切换后回答风格可能不同，需要在应用层消化。
- 缓存命中率很依赖 prompt 规范，必要时结合 embedding 去重。

这个封装的意义不在于“又造了个轮子”，而是告诉你：在 LlamaIndex 体系里，替换底层 LLM 客户端是很容易的。运维侧想要多云容灾、成本优化，只需要写一个薄薄的适配层。EOF
