+++
title = "Bub：一个自举型命令行编码助手"
description = "从一个 while 循环开始，让智能体先学会修自己的项目。"
date = 2025-07-16
slug = "baby-step-coding-agent"

[extra]
lang = "zh"
+++

Bub 是我在命令行里养的一只“小工程师”。第一件拿得出手的成果，是它帮我把项目里的 mypy 报错从 24 个砍到 23 个。下面记录它是怎么长大的。

## 为什么要自己造

市面上的编码智能体越来越多，但很多都是“堆 token 不讲效率”。我想试试能不能做一个**自举能力有限但实用**的助手：自己能修自己的代码库，还能解释它做了什么。

## 第一原则：先跑起来

忘掉“完美架构”，先构建最小正反馈循环——收到指令，判断是否需要工具 → 调用工具 → 把结果写回上下文 → 再次推理。

```python
class Agent:
    def chat(self, message: str) -> str:
        history.append(Message("user", message))
        while True:
            response = litellm.completion(history, tools)
            assistant_msg = response.choices[0].message.content
            history.append(Message("assistant", assistant_msg))
            tool_calls = tool_executor.extract(assistant_msg)
            if not tool_calls:
                return assistant_msg
            for call in tool_calls:
                result = tool_executor.execute(call)
                history.append(Message("user", f"Observation: {result}"))
```

踩坑提醒：

- LLM 格式出错时要能退出循环；
- 工具参数必须校验，不然随手传个 `None` 就炸；
- Observation 不要写诗，信息密度越高越好。

## 工具是手和脚

- 参数用 Pydantic 校验，错误直接拒绝；
- 命令行工具有黑名单，`rm -rf` 这种不用讨论；
- 输出结构化：stdout、stderr、exit code 分开回传；
- 结果里明确说明“成功/失败、后续建议”。

```python
class RunCommandTool(Tool):
    BLOCKED = {"rm", "shutdown"}
    async def execute(self, command: str) -> ToolResult:
        base_cmd = command.split()[0]
        if base_cmd in self.BLOCKED:
            return ToolResult(error=f"Command blocked: {base_cmd}")
        proc = await anyio.run_process(command, check=False)
        return ToolResult(stdout=proc.stdout, stderr=proc.stderr, returncode=proc.returncode)
```

## Prompt 要“画线”

ReAct 格式简单粗暴：Thought、Action、Action Input、Observation、Final Answer。有三点要做到：

1. 列出所有工具及参数示例；
2. 给几段完整的使用样例；
3. Observation 控制在可读范围内。

## 第一个里程碑：自动修类型

流程是：

1. 运行 `mypy`，记录报错；
2. 让 Bub 阅读报错，定位文件；
3. 用“编辑文件”工具打补丁；
4. 再跑一次 mypy 验证。

举例：

```diff
-    def __init__(self):
-        self.console = Console()
-        self._show_debug = False
+    def __init__(self) -> None:
+        self.console: Console = Console()
+        self._show_debug: bool = False
```

约束条件：只允许改类型注解、命名、文档，不碰业务逻辑；补丁必须能自动验证；失败要能回滚。

## 工程化心得

- 工具要职责单一，方便组合；
- 大上下文要裁剪或摘要，否则 LLM 迟早超窗；
- 命令执行默认在沙箱里跑，危险操作默认禁用；
- 对于不稳定的模型输出，兜底逻辑要早做。

## 现在进展

Bub 能自动跑 lint/mypy、执行脚本、读写文件，并把修改记录下来。还远没到发布的程度，但已经足够在自己项目里当小助手。下一步计划：

- 引入 RAG，帮助它在仓库里更快定位上下文；
- 更细粒度的安全护栏；
- 把“自举”扩展到工具注册、Prompt 微调等环节。

“Bub it. Build it.” 就是这只助手的小口号。有些工作不必等行业旗舰搞定，自己动手也能见到火花。EOF
