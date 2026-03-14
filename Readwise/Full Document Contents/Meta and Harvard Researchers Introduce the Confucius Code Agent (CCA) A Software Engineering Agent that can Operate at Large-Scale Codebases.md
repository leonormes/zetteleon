---
created: 2026-03-14T09:49:41+00:00
modified: 2026-03-14T11:09:54+00:00
tags: [articles]
title: Meta and Harvard Researchers Introduce the Confucius Code Agent (CCA) A Software Engineering Agent that can Operate at Large-Scale Codebases
---

## Meta and Harvard Researchers Introduce the Confucius Code Agent (CCA): A Software Engineering Agent that Can Operate at Large-Scale Codebases

![rw-book-cover](https://www.marktechpost.com/wp-content/uploads/2026/01/blog-banner23-1-3-1024x731.png)

### Metadata

- Author: [[Asif Razzaq]]
- Full Title: Meta and Harvard Researchers Introduce the Confucius Code Agent (CCA): A Software Engineering Agent that can Operate at Large-Scale Codebases
- Category: articles
- Summary: Meta and Harvard researchers created the Confucius Code Agent, an AI software engineer designed for large codebases using a strong scaffolding system called the Confucius SDK. This system uses advanced memory, note-taking, and tool management to improve coding performance and efficiency across sessions. Results show it beats bigger models by focusing on smart design, tool use, and automated agent tuning.
- URL: <https://share.google/dnFSGL2J7Q1Do6svT>

### Full Document

How far can a mid sized language model go if the real innovation moves from the backbone into the agent scaffold and tool stack? Meta and Harvard researchers have released the Confucius Code Agent, an open sourced AI software engineer built on the Confucius SDK that is designed for industrial scale software repositories and long running sessions. The system targets real GitHub projects, complex test toolchains at evaluation time, and reproducible results on benchmarks such as SWE Bench Pro and SWE Bench Verified, while exposing the full scaffold for developers.

![](https://www.marktechpost.com/wp-content/uploads/2026/01/Screenshot-2026-01-09-at-7.32.43-AM-1-1024x489.png)![](https://www.marktechpost.com/wp-content/uploads/2026/01/Screenshot-2026-01-09-at-7.32.43-AM-1.png)<https://arxiv.org/pdf/2512.10398>

#### Confucius SDK, Scaffolding around the Model

The Confucius SDK is an agent development platform that treats scaffolding as a primary design problem rather than a thin wrapper around a language model. It is organized around 3 axes, Agent Experience, User Experience, and Developer Experience.

Agent Experience controls what the model sees, including context layout, working memory and tool results. User Experience focuses on readable traces, code diffs and safeguards for human engineers. Developer Experience focuses on observability, configuration and debugging of the agent itself.

The SDK introduces 3 core mechanisms, a unified orchestrator with hierarchical working memory, a persistent note taking system, and a modular extension interface for tools. A meta agent then automates synthesis and refinement of agent configurations through a build, test, improve loop. The Confucius Code Agent is one concrete instantiation of this scaffold for software engineering.

![](https://www.marktechpost.com/wp-content/uploads/2026/01/Screenshot-2026-01-09-at-7.33.46-AM-1-1024x471.png)![](https://www.marktechpost.com/wp-content/uploads/2026/01/Screenshot-2026-01-09-at-7.33.46-AM-1.png)<https://arxiv.org/pdf/2512.10398>

#### Hierarchical Working Memory for long Horizon Coding

Real software tasks on SWE Bench Pro often require reasoning over dozens of files and many interaction steps. The orchestrator in Confucius SDK maintains hierarchical working memory, which partitions a trajectory into scopes, summarizes past steps and keeps compressed context for later turns.

This design helps keep prompts within model context limits while preserving important artifacts such as patches, error logs and design decisions. The key point is that effective tool based coding agents need an explicit memory architecture, not just a sliding window of previous messages.

#### Persistent Note Taking for Cross Session Learning

The second mechanism is a note taking system that uses a dedicated agent to write structured Markdown notes from execution traces. These notes capture task specific strategies, repository conventions and common failure modes, and they are stored as long term memory that can be reused across sessions.

The research team ran Confucius Code Agent twice on 151 SWE Bench Pro instances with Claude 4.5 Sonnet. On the first run the agent solves tasks from scratch and generates notes. On the second run the agent reads these notes. In this setting, average turns drop from 64 to 61, token usage drops from about 104k to 93k, and Resolve@1 improves from 53.0 to 54.4. This shows that notes are not just logs, they function as effective cross session memory.

#### Modular Extensions and Tool Use Sophistication

Confucius SDK exposes tools as extensions, for example file editing, command execution, test runners and code search. Each extension can maintain its own state and prompt wiring.

The research team studies the impact of tool use sophistication using an ablation on a 100 example subset of SWE Bench Pro. With Claude 4 Sonnet, moving from a configuration without advanced context features to one with advanced context raises Resolve@1 from 42.0 to 48.6. With Claude 4.5 Sonnet, a simple tool use configuration reaches 44.0, while richer tool handling reaches 51.6, with 51.0 for an intermediate variant. These numbers indicate that how the agent chooses and sequences tools matters almost as much as the backbone model choice.

![](https://www.marktechpost.com/wp-content/uploads/2026/01/Screenshot-2026-01-09-at-7.34.24-AM-1-1024x512.png)![](https://www.marktechpost.com/wp-content/uploads/2026/01/Screenshot-2026-01-09-at-7.34.24-AM-1.png)<https://arxiv.org/pdf/2512.10398>

#### Meta Agent for Automatic Agent Design

On top of these mechanisms, the Confucius SDK includes a meta agent that takes a natural language specification of an agent and iteratively proposes configurations, prompts and extension sets. It then runs the candidate agent on tasks, inspects traces and metrics, and edits the configuration in a build, test, improve loop.

The Confucius Code Agent that the research team evaluates is produced with the help of this meta agent, rather than only hand tuned. This approach turns some of the agent engineering process itself into an LLM guided optimization problem.

#### Results on SWE Bench Pro and SWE Bench Verified

The main evaluation uses SWE Bench Pro, which has 731 GitHub issues that require modifying real repositories until tests pass. All compared systems share the same repositories, tool environment and evaluation harness, so differences come from the scaffolds and models.

On SWE Bench Pro, the reported Resolve@1 scores are

- Claude 4 Sonnet with SWE Agent, 42.7
- Claude 4 Sonnet with Confucius Code Agent, 45.5
- Claude 4.5 Sonnet with SWE Agent, 43.6
- Claude 4.5 Sonnet with Live SWE Agent, 45.8
- Claude 4.5 Sonnet with Confucius Code Agent, 52.7
- Claude 4.5 Opus with Anthropic system card scaffold, 52.0
- Claude 4.5 Opus with Confucius Code Agent, 54.3

These results show that a strong scaffold with a mid tier model, Claude 4.5 Sonnet with Confucius Code Agent at 52.7, can outperform a stronger model with a weaker scaffold, Claude 4.5 Opus with 52.0.

On SWE Bench Verified, Confucius Code Agent with Claude 4 Sonnet reaches Resolve@1 74.6, compared to 66.6 for SWE Agent and 72.8 for OpenHands. A mini SWE Agent variant with Claude 4.5 Sonnet reaches 70.6, which is also below Confucius Code Agent with Claude 4 Sonnet.

The research team also report performance as a function of edited file count. For tasks editing 1 to 2 files, Confucius Code Agent reaches 57.8 Resolve@1, for 3 to 4 files it reaches 49.2, for 5 to 6 files it reaches 44.1, for 7 to 10 files it reaches 52.6, and for more than 10 files it reaches 44.4. This indicates stable behavior on multi file changes in large codebases.

#### Key Takeaways

- Scaffolding can outweigh model size: Confucius Code Agent shows that with strong scaffolding, Claude 4.5 Sonnet reaches 52.7 Resolve@1 on SWE-Bench-Pro, surpassing Claude 4.5 Opus with a weaker scaffold at 52.0.
- Hierarchical working memory is essential for long horizon coding: The Confucius SDK orchestrator uses hierarchical working memory and context compression to manage long trajectories over large repositories, rather than relying on a simple rolling history.
- Persistent notes act as effective cross session memory: On 151 SWE-Bench-Pro tasks with Claude 4.5 Sonnet, reusing structured notes reduces turns from 64 to 61, token usage from about 104k to 93k, and increases Resolve@1 from 53.0 to 54.4.
- Tool configuration materially impacts success rates: On a 100 task SWE-Bench-Pro subset, moving from simple to richer tool handling with Claude 4.5 Sonnet increases Resolve@1 from 44.0 to 51.6, indicating that learned tool routing and recovery strategies are a major performance lever, not just an implementation detail.
- Meta agent automates agent design and tuning: A meta agent iteratively proposes prompts, tool sets and configurations, then evaluates and edits them in a build, test, improve loop, and the production Confucius Code Agent is itself generated with this process rather than only manual tuning.

Check out the [PAPER HERE](https://arxiv.org/pdf/2512.10398). Also, feel free to follow us on [Twitter](https://x.com/intent/follow?screen_name=marktechpost) and don't forget to join our [100k+ ML SubReddit](https://www.reddit.com/r/machinelearningnews/) and Subscribe to [our Newsletter](https://www.aidevsignals.com/). Wait! are you on telegram? [now you can join us on telegram as well.](https://t.me/machinelearningresearchnews)

Check out our latest release of [ai2025.dev](https://ai2025.dev/), a 2025-focused analytics platform that turns model launches, benchmarks, and ecosystem activity into a structured dataset you can filter, compare, and export.
