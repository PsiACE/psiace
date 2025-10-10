+++
title = "用 VLM 做图像解析的轻量套路"
description = "把多模态模型当小工，用几十行代码把图片里的结构化信息扒出来。"
date = 2024-11-28
slug = "a-dead-simple-way-to-vlm-parsing"

[taxonomies]
tags = ["VLM", "Parsing", "OpenAI", "Unstructured Data", "MultiModal", "llama-index", "Python"]

[extra]
lang = "zh"
+++

## 需求是什么？

公司内部常见的诉求：有一堆截图、报表、仪表盘，需要自动提取文本、结构化信息；或者想让搜索可以命中图片内容。传统做法是 OCR + 手搓解析器，维护成本高得吓人。多模态模型（VLM）已经足够靠谱，不如直接让它干这类“看图说话”的重活。

## 最小工作流长什么样

1. 选一个 VLM（我用 `llama-index` 的封装 + OpenAI GPT-4o mini，换 Claude、Gemini 也一样）。
2. 准备一个提示词，告诉模型我们要哪些信息：概览、文字、表格、图表、补充细节。
3. 把图片转成 base64，作为 `data:image/png` 发送。
4. 接收结果，按需落地到终端、JSON 或数据库。

就是这么简单，核心代码不到一百行。

```python
class SimpleImageParser:
    def __init__(self, model: MultiModalLLM):
        self.model = model
        self.prompt = BASIC_PROMPT  # 详述我们想要的数据结构

    def process_image(self, image_path: str) -> str:
        image = Image.open(image_path)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    async def parse(self, image_path: str) -> str:
        image_data = self.process_image(image_path)
        image_doc = ImageDocument(image_url=f"data:image/png;base64,{image_data}")
        response = await self.model.acomplete(
            prompt=self.prompt,
            image_documents=[image_doc]
        )
        return str(response)
```

## 跑起来

```bash
python basic.py ./samples/gateway.png
```

脚本会：
- 在 `.env` 里读多模态模型的 key、base、温度等配置；
- 调用 VLM；
- 打印解析结果。

在 demo 里，我给了一张家庭网关的界面截图，模型可以同时识别页面布局、表格内容、按钮状态，还能提取文本。效果对 CRM、客服系统、知识库已经够用了。

## 想拓展？几个方向

- **多格式输入**：引入 `pdf2image`、OpenCV，就能批量处理 PDF、视频帧。
- **结构化输出**：把结果再走一遍规则或 LLM post-processing，转成 JSON / Markdown 表格。
- **流水线化**：用 asyncio / 队列批量处理，或接入 `llama-index` 的 RAG 流程，让图像内容直接进检索。

## 资源

- 代码仓库：[psiace/demo/vlm-parsing](https://github.com/psiace/psiace/tree/main/demo/vlm-parsing)
- 文档参考：[llama-index docs](https://docs.llamaindex.ai/)

一句话总结：VLM 的门槛比你想象得低，把它当“图片解析服务”即可。先用简单套路验证价值，再决定要不要引入更复杂的 OCR/结构化管线。EOF
