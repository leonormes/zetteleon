---
created: 2026-03-14T09:49:42+00:00
modified: 2026-03-14T11:09:49+00:00
tags: [articles]
title: Legal language change aims to make longstanding policy clear
---

## Legal Language Change Aims to Make Longstanding Policy Clear

![rw-book-cover](https://regmedia.co.uk/2025/05/22/shutterstock_anthropic_claude.jpg)

### Metadata

- Author: [[Thomas Claburn]]
- Full Title: Legal language change aims to make longstanding policy clear
- Category: articles
- Summary: Anthropic updated its legal terms to stop third-party tools from using Claude subscriptions without permission. This change aims to protect their subscription model and prevent misuse. Some third-party developers have already removed support for these accounts following Anthropic's request.
- URL: <https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access/>

### Full Document

Anthropic this week revised its legal terms to clarify its policy forbidding the use of third-party harnesses with Claude subscriptions, as the AI biz attempts to shore up its revenue model.

Anthropic sells subscriptions to its Claude platform, which provides access to a family of machine learning models (e.g. Opus 4.6), and associated tools like Claude Code, a web-based interface at Claude.ai, and the Claude Desktop application, among others.

[Claude Code](https://code.claude.com/docs/en/overview) is a harness or wrapper–it integrates with the user's terminal and routes prompts to the available Claude model in conjunction with other tools and a control loop that, together, make it what Anthropic calls an agentic coding tool.

Many other tools serve as harnesses for models, such as OpenAI Codex, Google Antigravity, Manus (recently acquired by Meta), OpenCode, Cursor, and Pi (the harness behind OpenClaw).

Harnesses exist because interacting with a machine learning model itself is not a great user experience–you feed it a prompt and it returns a result. That's a single-turn interaction. Input and output. To create a product that people care about, model makers have added support for multi-turn interaction, memory of prior interactions, access to tools, orchestration to handle data flowing between those tools, and so on. Some of this support has been baked into model platforms, but some of it has been added through harness tooling.

This can pose a business problem for frontier model makers–they've invested billions to train sophisticated models, but they risk being disintermediated by gatekeeping intermediaries that build harnesses around their models and offer a better user experience.

One of the ways that Anthropic has chosen to build brand loyalty is by selling tokens to subscription customers at a monthly price, with [usage limits](https://support.claude.com/en/articles/9797557-usage-limit-best-practices), that ends up being less costly than pay-as-you-go token purchases through the Claude API. Essentially, the economics are similar to an all-you-can-eat buffet that's priced with certain usage expectations.

That practice, effectively a subsidy for subscribers, led to token arbitrage. Customers accessed Claude models via subscriptions linked to third-party harnesses because it cost less than doing the same work via API key.

The AI biz's Consumer Terms of Service have forbidden the use of third-party harnesses, except with specific authorization [since at least February 2024](https://www.anthropic.com/legal/archive/71085c3c-857c-464d-8075-ae918f0e5555). The contractual language in Section 3.7, which remains unchanged from that time, says as much–any automated access tool not officially endorsed is forbidden.

> You may not access or use, or help another person to access or use, our Services in the following ways:

> Except when you are accessing our Services via an Anthropic API Key or where we otherwise explicitly permit it, to access the Services through automated or non-human means, whether through a bot, script, or otherwise.

Despite the presence of that passage for more than two years, a variety of third-party tools have flouted that rule and have allowed users to supply a Claude subscription account key.

The added rule explicitly states that OAuth authentication, the access method used for Claude Free, Pro, and Max tier subscribers, is only intended for Claude Code and Claude.ai (the web interface for Claude models).

"Using OAuth tokens obtained through Claude Free, Pro, or Max accounts in any other product, tool, or service—including the [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)—is not permitted and constitutes a violation of the [Consumer Terms of Service](https://www.anthropic.com/legal/consumer-terms)," the updated [legal compliance page](https://code.claude.com/docs/en/legal-and-compliance) says.

According to Anthropic, the update represents an attempt to clarify existing policy language to make it consistent throughout company documentation.

Anthropic appears to have decided to police its rules at the start of the year. In a January social media [thread](https://x.com/trq212/status/2009689809875591565?s=20), Anthropic engineer Thariq Shihipar said the company had taken steps to prevent third-party tools from "spoofing the Claude Code harness."

"Third-party harnesses using Claude subscriptions create problems for users and are prohibited by our Terms of Service," he wrote. "They generate unusual traffic patterns without any of the usual telemetry that the Claude Code harness provides, making it really hard for us to help debug when they have questions about rate limit usage or account bans and they don't have any other avenue for this support."

The prohibition proved unpopular enough to elicit a response from the competition. OpenAI's Thibault Sottiaux pointedly [endorsed](https://x.com/thsottiaux/status/2009742187484065881?s=20) the use of Codex subscriptions in third-party harnesses.

After banning accounts for attempting to game its pricing structure, Anthropic has now clarified its legalese, as Shihipar [indicated would happen](https://x.com/trq212/status/2009689814917083363?s=20), and makers of third-party harnesses are taking note.

On Thursday, OpenCode [pushed code](https://github.com/anomalyco/opencode/commit/973715f3da1839ef2eba62d4140fe7441d539411) to remove support for Claude Pro and Max account keys and Claude API keys. The commit cites "anthropic legal requests." ®
