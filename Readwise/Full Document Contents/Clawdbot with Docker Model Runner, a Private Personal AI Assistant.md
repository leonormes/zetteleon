---
created: 2026-03-14T09:49:42+00:00
modified: 2026-03-14T11:09:52+00:00
tags: [articles]
title: Clawdbot with Docker Model Runner, a Private Personal AI Assistant
---

## Clawdbot with Docker Model Runner, a Private Personal AI Assistant

![rw-book-cover](https://www.docker.com/app/uploads/2025/03/image.png)

### Metadata

- Author: [[Ignasi Lopez Luna, Eric Curtin]]
- Full Title: Clawdbot with Docker Model Runner, a Private Personal AI Assistant
- Category: articles
- Summary: Clawdbot and Docker Model Runner let you build a private AI assistant that keeps your data on your own device. This setup protects your privacy and avoids costly cloud fees by running AI models locally. You can connect Clawdbot to apps like Telegram to get smart help without sharing your personal information.
- URL: <https://www.docker.com/blog/clawdbot-docker-model-runner-private-personal-ai/>

### Full Document

Personal AI assistants are transforming how we manage our daily lives—from handling emails and calendars to automating smart homes. However, as these assistants gain more access to our private data, concerns about privacy, data residency, and long-term costs are at an all-time high.

By combining [Clawdbot](https://clawd.bot/) with [Docker Model Runner](https://docs.docker.com/ai/model-runner/) (DMR), you can build a high-performance, agentic personal assistant while keeping full control over your data, infrastructure, and spending.

This post walks through how to configure Clawdbot to utilize Docker Model Runner, enabling a privacy-first approach to personal intelligence.

Clawdbot is a self-hosted AI assistant designed to live where you already are. Unlike browser-bound bots, Clawdbot integrates directly with messaging apps like Telegram, WhatsApp, Discord, and Signal. It acts as a proactive digital coworker capable of executing real-world actions across your devices and services.

Docker Model Runner (DMR) is Docker's native solution for running and managing large language models (LLMs) as OCI artifacts. It exposes an OpenAI-compatible API, allowing it to serve as the private "brain" for any tool that supports standard AI endpoints.

Together, they create a unified assistant that can browse the web, manage your files, and respond to your messages without ever sending your sensitive data to a third-party cloud.

Privacy by Design

In a "Privacy-First" setup, your assistant's memory, message history, and files stay on your hardware. Docker Model Runner isolates model inference, meaning:

- No third-party training: Your personal emails and schedules aren't used to train future commercial models.
- Data Sovereignty: You decide exactly which "Skills" (web browsing, file access) the assistant can use.

Cost Control and Scaling

Cloud-based agents often become expensive when they use "long-term memory" or "proactive searching," which consume massive amounts of tokens. With Docker Model Runner, inference runs on your own GPU/CPU. Once a model is pulled, there are no per-token fees. You can let Clawdbot summarize thousands of unread emails or research complex topics for hours without worrying about a surprise API bill at the end of the month.

#### Configuring Clawdbot with Docker Model Runner

Clawdbot uses a flexible configuration system to define which models and providers drive its reasoning. While the onboarding wizard (clawdbot onboard) is the standard setup path, you can manually point Clawdbot to your private Docker infrastructure.

You can define your provider configuration in:

- Global configuration: ~/.config/clawdbot/config.json
- Workspace-specific configuration: clawdbot.json in your active workspace root.

To bridge the two, update your configuration to point to the DMR server. Assuming Docker Model Runner is running at its default address: <http://localhost:12434/v1>.

Your config.json should be updated as follows:

|  |  |
| --- | --- |
| 1234567891011121314151617181920212223242526272829303132 | `{``"models": {``"providers": {``"dmr": {``"baseUrl": "<http://localhost:12434/v1>",``"apiKey": "dmr-local",``"api": "openai-completions",``"models": [``{``"id": "gpt-oss:128K",``"name": "gpt-oss (128K context window)",``"contextWindow": 128000,``"maxTokens": 128000``},``{``"id": "glm-4.7-flash:128K",``"name": "glm-4.7-flash (128K context window)",``"contextWindow": 128000,``"maxTokens": 128000``}``]``}``}``},``"agents": {``"defaults": {``"model": {``"primary": "dmr/gpt-oss:128K"``}``}``}``}` |

This configuration tells Clawdbot to bypass external APIs and route all "thinking" to your private models.

Note for Docker Desktop Users:

Ensure TCP access is enabled so Clawdbot can communicate with the runner. Run the following command in your terminal:

docker desktop enable model-runner–tcp

While coding models focus on logic, personal assistant models need a balance of instruction-following, tool-use capability, and long-term memory.

DMR can pull models directly from Hugging Face and convert them into OCI artifacts automatically:

|  |
| --- |
| `docker model pull huggingface.co/bartowski/Llama-3.3-70B-Instruct-GGUF` |

For a personal assistant, context length is critical. Clawdbot relies on a SOUL.md file (which defines its personality) and a Memory Vault (which stores your preferences).

If a model's default context is too small, it will "forget" your instructions mid-conversation. You can use DMR to repackage a model with a larger context window:

|  |
| --- |
| `docker model package --from llama3.3 --context-size 128000 llama-personal:128k` |

Once packaged, reference llama-personal:128k in your Clawdbot config to ensure your assistant always remembers the full history of your requests.

With Clawdbot and DMR running, you can move beyond simple chat. Let's set up a "Morning Briefing" task.

1. Verify the Model: docker model ls (Ensure your model is active).
2. Initialize the Soul: Run clawdbot init-soul to define how the assistant should talk to you.
3. Assign a Task:"Clawdbot, every morning at 8:00 AM, check my unread emails, summarize the top 3 priorities, and message me the summary on Telegram."

Because Clawdbot is connected to your private Docker Model Runner, it can parse those emails and reason about your schedule privately. No data leaves your machine; you simply receive a helpful notification on your phone via your chosen messaging app.

The Clawdbot and Docker Model Runner ecosystems are growing rapidly. Here's how you can help:
