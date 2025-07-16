---
title: Agent in CLI
description: TUI is good, but in CLI Context, we can do more.
publishDate: "2025-07-16T13:23:00Z"
---

A CLI assistant that can help you with various tasks.

CLI tools should behave like CLI—users expect to see command output in their terminal buffer, especially for chat-like, append-only interactions. Instead of hiding interactions behind fancy TUIs, it should let every command and response live in the terminal buffer—visible, searchable, and scriptable. For chat-like tools, this append-only, scrollable history is not a limitation, but a feature. Sometimes, less interface means more power.

This note is inspired by [yetone's original post on X](https://x.com/yetone/status/1945332013231476986).
