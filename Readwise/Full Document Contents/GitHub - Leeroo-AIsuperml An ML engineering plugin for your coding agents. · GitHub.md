# GitHub - Leeroo-AI/superml: An ML engineering plugin for your coding agents. · GitHub

![rw-book-cover](https://opengraph.githubassets.com/01b5049276a285ee0bf855b8f77faf9cf067ad5d94ad838dc4c929a786237b29/Leeroo-AI/superml)

## Metadata
- Author: [[https://github.com/Leeroo-AI/]]
- Full Title: GitHub - Leeroo-AI/superml: An ML engineering plugin for your coding agents. · GitHub
- Category: #articles
- Summary: SuperML is a plugin that gives AI coding agents tools to plan, verify, debug, and improve machine learning workflows. It uses a large knowledge base called Leeroopedia to provide accurate, documented advice and remembers past experiments to avoid repeated mistakes. The plugin works with many coding agents and helps save time and GPU costs by catching errors early and suggesting next steps.
- URL: https://github.com/Leeroo-AI/superml

## Full Document
### Leeroo-AI/superml

main

Go to file

Code

Open more actions menu

### SuperML

**Give your AI coding agent ML engineering superpowers.**

[![Leeroopedia](https://camo.githubusercontent.com/8060acc62938ef8e05bf267b81a9d87c80d4913d56c238f573710171f951e41a/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6b6e6f776c65646765253230626173652d6c6565726f6f70656469612e636f6d2d677265656e)](https://leeroopedia.com)
[![License](https://camo.githubusercontent.com/35b94db23d3ed026343335f74d52ce31e74b77ad7dab4e4b89f49f2026e0937f/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d4170616368652d2d322e302d626c7565)](https://github.com/leeroo-ai/superml/blob/main/LICENSE)
[![Discord](https://camo.githubusercontent.com/a7bb09da25bff6fcbdeb6f0df37c61c810785446f475d2d49c49ae74ca2f0360/68747470733a2f2f646362616467652e6c696d65732e70696e6b2f6170692f7365727665722f68715662504e4e455a4d3f7374796c653d666c6174)](https://discord.gg/hqVbPNNEZM)
[![GitHub commit activity](https://camo.githubusercontent.com/8457074b9f98428cbde187304bf4122012505ae9154256131c19894457f2350d/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f636f6d6d69742d61637469766974792f6d2f6c6565726f6f2d61692f73757065726d6c)](https://github.com/leeroo-ai/superml)
[![Y Combinator X25](https://camo.githubusercontent.com/5574afc629e55301e9283f2327399c62954b5391a46ec2280bfb88e1b4e008b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f59253230436f6d62696e61746f722d5832352d6f72616e67653f6c6f676f3d79636f6d62696e61746f72266c6f676f436f6c6f723d7768697465)](https://www.ycombinator.com/companies/leeroo)
*Watch how SuperML works in 90 seconds:*

[![SuperML Demo Video](https://camo.githubusercontent.com/f7ebdae8397075628dd46ca6f6d7ee1144d2627badad659cce98ff39773ec5c8/68747470733a2f2f696d672e796f75747562652e636f6d2f76692f665778417a666e4c5733512f6d617872657364656661756c742e6a7067)](https://www.youtube.com/watch?v=fWxAzfnLW3Q)
It adds two things your coding agent doesn't have:

**ML Pipeline**: Seven skills that encode the workflow you already follow. Plan against real framework docs. Catch config mistakes before they cost you GPU hours. Debug OOM, NaN, and divergence by root cause, not by guessing. Get ranked next steps when metrics plateau. An agentic experiment memory carries hypotheses, results, and lessons across sessions — your agent stops repeating failed experiments and starts compounding what works.

**Memory**: Backed by [Leeroopedia](https://leeroopedia.com), 27k+ pages across 1000+ ML/AI frameworks. Config references, debugging heuristics, implementation patterns, and battle-tested defaults from vLLM to DeepSpeed to LangChain. Built by the [Leeroo](https://leeroo.com) continuous learning system, structured as a browsable wiki, and continuously updated by AI and human engineers. When your agent recommends a config, it points to the page it learned it from.

Works with Claude Code, Cursor, Codex, OpenCode, and Gemini CLI.

#### How It Works

1. **A session hook** loads automatically, zero setup per conversation.
2. **Skills** guide the ML workflow, verify before launch, debug by root cause, iterate on results, track what worked.
3. **MCP tools** connect to the Leeroopedia knowledge base, your agent looks things up and cites real docs instead of guessing.
4. **A persistent ML agent** (`ml-expert`) handles deeper tasks and remembers your hardware, experiments, and lessons across sessions.

#### Results

We gave 38 ML tasks to Claude Code — once with SuperML, once without — and had an independent LLM judge rate both. Each response is scored out of 15 across correctness, specificity, mistake prevention, actionability, and grounding. Tasks cover QLoRA fine-tuning, distributed training, LLM inference optimization, alignment (DPO/GRPO), RAG pipelines, model merging, quantization, and more.

|  | With SuperML | Without |
| --- | --- | --- |
| ML task average | **13.2 / 15** | 8.3 / 15 |
| ML task win rate | **91%** | 9% |

See [TESTED\_TASKS.md](https://github.com/Leeroo-AI/superml/blob/main/TESTED_TASKS.md) for the full list of tasks and scores.

#### Prerequisites

##### API Key (optional, highly recommended)

The plugin works without an API key — skills use web search to ground answers. With a key, your agent gets access to the Leeroopedia knowledge base (27k+ pages, faster and more precise lookups). The plugin will tell you if it's running without a key.

To get a key: [app.leeroopedia.com](https://app.leeroopedia.com/dashboard) — $20 free credit on signup, no credit card.

```
export LEEROOPEDIA_API_KEY=kpsk_your_key_here
```

Add to your shell profile (`~/.bashrc`, `~/.zshrc`) so it persists.

#### Installation

##### Claude Code

Register the marketplace, then install the plugin:

```
/plugin marketplace add leeroo-ai/leeroo-marketplace
/plugin install superml@leeroo-marketplace

```

Or install directly from GitHub:

```
claude plugin add --from-github leeroo-ai/superml
```

##### Cursor

In Cursor Agent chat (waiting for Cursor team approval):

```
/add-plugin superml

```

Or clone into your project — Cursor auto-detects `.cursor-plugin/plugin.json`:

```
git clone https://github.com/leeroo-ai/superml.git
```

##### Codex

See [.codex/INSTALL.md](https://github.com/Leeroo-AI/superml/blob/main/.codex/INSTALL.md).

##### OpenCode

See [.opencode/INSTALL.md](https://github.com/Leeroo-AI/superml/blob/main/.opencode/INSTALL.md).

##### Gemini CLI

```
git clone https://github.com/leeroo-ai/superml.git
gemini extension add ./superml/gemini-extension.json
```

##### Alternative: Remote MCP (no local install)

If you just want the knowledge base without the full plugin, see [leeroopedia-mcp](https://github.com/Leeroo-AI/leeroopedia-mcp) for setup instructions.

You get the MCP tools (memory) but not the workflow skills (process).

##### Verify Installation

Start a conversation and try something like:

```
I'm fine-tuning Llama 3.1 8B on 50k instruction pairs with 1xA100 80GB.
Set up the full training config — QLoRA, proper chat template, loss masking on prompts.

```

If it's working, your agent will ground its answer in documentation (KB citations or web sources), catch common pitfalls before they waste a training run, and give you a runnable config.

#### What's Inside

##### Skills

| Skill | What it does |
| --- | --- |
| [ml-plan](https://github.com/Leeroo-AI/superml/blob/main/skills/ml-plan/SKILL.md) | Plan training runs, architectures, and multi-step pipelines |
| [ml-verify](https://github.com/Leeroo-AI/superml/blob/main/skills/ml-verify/SKILL.md) | Check configs, code, and math before you burn GPU hours |
| [ml-debug](https://github.com/Leeroo-AI/superml/blob/main/skills/ml-debug/SKILL.md) | Debug OOM, NaN, divergence, crashes, bad throughput |
| [ml-iterate](https://github.com/Leeroo-AI/superml/blob/main/skills/ml-iterate/SKILL.md) | Ranked next steps when results aren't where you want them |
| [ml-experiment](https://github.com/Leeroo-AI/superml/blob/main/skills/ml-experiment/SKILL.md) | Track experiments — hypotheses, results, and learnings across sessions |
| [ml-research](https://github.com/Leeroo-AI/superml/blob/main/skills/ml-research/SKILL.md) | Deep-dive into ML topics, compare approaches, survey frameworks |
| [using-superml](https://github.com/Leeroo-AI/superml/blob/main/skills/using-superml/SKILL.md) | Loaded at session start — wires up skills to KB tools and sets quality standards |

##### Agent

[ml-expert](https://github.com/Leeroo-AI/superml/blob/main/agents/ml-expert.md): a persistent ML engineer agent for the bigger stuff: pipeline reviews, deep analysis, framework deep-dives. It remembers your hardware setup, past experiments, and lessons learned across sessions.

#### SuperML for Enterprise

>  **SuperML is integrated in our enterprise platform** — forecasting & planning, fraud & anomaly detection, customer analytics, recommendation systems, document intelligence, and customer service automation.
> 
>  [**Request enterprise access →**](https://novel-platform.leeroo.com/auth)
> 
>  

#### Contributing

See [CONTRIBUTING.md](https://github.com/Leeroo-AI/superml/blob/main/CONTRIBUTING.md) for how to report bugs, suggest improvements, and submit PRs.

#### Links

* [Leeroopedia](https://leeroopedia.com): the ML/AI knowledge base behind the memory
* [leeroopedia-mcp](https://github.com/leeroo-ai/leeroopedia-mcp): MCP server repo
* [Leeroo](https://leeroo.com): the team behind SuperML

#### License

[Apache-2.0](https://github.com/Leeroo-AI/superml/blob/main/LICENSE)
