---
created: 2026-05-27T09:18:23+00:00
modified: 2026-05-27T09:25:48+00:00
title: Hermes, OpenRouter, and Model Orchestration
---

## Strategic Implementation Plan: Orchestrating Autonomous Agent Workflows Using Hermes and OpenRouter

### Executive Summary

The paradigm of software engineering and workflow automation is rapidly shifting away from direct, single-model prompt engineering through monolithic provider interfaces toward highly modular, autonomous, multi-agent orchestration. Traditional monolithic subscription services—such as the Claude Pro tier—while offering robust proprietary models, frequently suffer from structural and architectural rigidity. Tooling tied to these subscriptions, most notably single-vendor command-line interfaces (CLIs), often encounters localized execution bottlenecks. These bottlenecks manifest as severe network timeouts, constrained concurrency, blocked event loops, and fundamentally inefficient capital allocation. A primary example of this systemic inefficiency is the latency and timeout degradation experienced when utilizing standard coding CLIs for complex, long-running agentic tasks that require extensive context compilation and chain-of-thought reasoning.

Transitioning from a fixed-cost proprietary subscription model to a decoupled, multi-model orchestration architecture resolves these critical operational vulnerabilities. By integrating the Hermes Agent framework with the OpenRouter model aggregator API, developers can construct a highly resilient, asynchronous, and cost-optimized computing environment. This architectural approach allows for the deployment of a free, high-throughput large language model (LLM) to manage the persistent orchestration layer—handling memory management, strategic planning, file indexing, and tool dispatch—while dynamically delegating computationally intensive reasoning tasks to premium, specialized models on a pay-as-you-go basis.

This report provides an exhaustive, multi-phase strategic plan to implement this architecture, directly addressing the limitations of synchronous CLI tools. It details the precise configuration mechanics required to integrate Hermes with OpenRouter, token economics, model selection parameters, advanced subagent delegation patterns, and risk mitigation strategies required to operate a production-grade multi-agent system.

### Architectural Deficiencies in Monolithic CLIs vs. The Hermes Framework

The user experience degradation—specifically the timeout failures observed when utilizing standard, single-provider interfaces like the Claude Code CLI—stems from fundamental flaws in how early-generation AI tools manage synchronous network requests and application state. Standard CLI wrappers typically operate by compiling the local codebase context, sending a massive payload to the inference provider, and blocking the main execution thread while waiting for the model to stream its response back. When dealing with models that utilize extended reasoning phases, the time-to-first-token (TTFT) can easily exceed standard HTTP timeout thresholds, resulting in a dropped connection and lost work.

#### The Hermes Asynchronous Architecture

The foundation of the proposed deployment strategy relies on circumventing these limitations via the Hermes Agent, an open-source, terminal-native autonomous orchestration framework engineered by Nous Research.1 Hermes has rapidly established itself as a dominant framework in the agentic AI landscape, crossing 140,000 GitHub stars and ranking as the most heavily utilized agent framework globally on OpenRouter by early 2026\.3

Unlike thin wrappers or single-turn API clients that pass raw text back and forth sequentially, Hermes operates as an active orchestration layer designed for persistent, long-running deployment.3 This persistence fundamentally solves the timeout issues common in traditional CLI tools through a combination of terminal user interface (TUI) design and daemon threading.5

When a complex command is issued to Hermes using the /background directive, the system spawns a completely separate agent session within an isolated daemon thread.5 This background agent inherits the provider configuration, toolsets, reasoning settings, and fallback models of the parent session, but it operates with an isolated conversation context. Crucially, this ensures that the foreground session remains entirely non-blocking and interactive.5 The developer can continue to chat, run local shell commands, or even initialize additional background tasks without waiting for the initial API call to resolve. Because the daemon thread manages its own network persistence independently of the foreground UI, long-running agentic workflows—even those taking several minutes to process complex repositories—do not trigger the standard input/output timeout crashes that plague simpler applications.

#### Closed-Loop Learning and Context Persistence

Beyond execution resilience, the Hermes architecture is defined by its self-evolving state management. The framework utilizes a closed learning loop, allowing the agent to curate its own memory via periodic background nudges.1 When Hermes completes a complex multi-step task, it autonomously triggers a skill creation sequence, writing and refining its own executable tools based on the accumulated experience of the session.1 Nous Research guarantees reliability by design, curating and stress-testing the base skills that ship with the agent, while allowing user-specific skills to self-improve during ongoing usage.3

To prevent context window degradation and memory loss over long periods, Hermes employs FTS5 (Full-Text Search) session indexing combined with LLM-driven summarization for cross-session recall.1 This is augmented by a dialectic user modeling system (powered by Honcho) that builds a deepening profile of the operator and the project architecture across multiple days or weeks of interaction.1 The agent is not restricted to local execution; it supports cross-platform continuity, allowing a developer to initiate a complex background task via a local terminal, and later monitor its progress or receive completion alerts via a messaging gateway connected to Telegram, Discord, Slack, or Signal.1

### The API Aggregation Layer: OpenRouter Infrastructure

To achieve the goal of utilizing a free model for orchestration while dynamically targeting premium models for complex tasks, the backend inference provider must be shifted from a direct vendor API to an aggregation layer. OpenRouter operates as a unified AI API gateway, providing standardized access to over 400 LLMs through a single endpoint and a consolidated billing structure.6 This integration allows the Hermes framework to dynamically select models based on real-time task requirements without requiring the developer to manage multiple API keys, varied network protocols, or distinct SDK implementations.1

#### Integration Fundamentals and API Endpoints

Implementing OpenRouter requires interacting with their primary REST API architecture. As documented in the OpenRouter Quickstart guide, direct HTTP requests must be formatted as JSON-encoded payloads directed to their completion endpoint via a POST request.8 The endpoint structure is identical to standard OpenAI architecture, facilitating seamless drop-in replacements for existing infrastructure.8

The integrity and tracking of the connection rely on a specific set of HTTP headers. OpenRouter utilizes these headers not only for authentication but for application attribution, usage analytics, and public ranking metrics.

| HTTP Header Specification | Requirement Level | Operational Function and Implications |
|:---- |:---- |:---- |
| Authorization | Mandatory | Must contain Bearer \<OPENROUTER\_API\_KEY\>. Validates the account and deducts credits based on the targeted model's pricing tier.8 |
| HTTP-Referer | Required for Attribution | Specifies the primary domain or application URL. This is mandatory if the developer wishes the application to appear in OpenRouter's public rankings and to access detailed individual app analytics tracking prompt and completion token consumption.8 |
| X-OpenRouter-Title | Recommended | Modifies the application's display name in analytics. It must be paired with the HTTP-Referer header to function. Best practices dictate using a concise, descriptive name.8 |
| X-OpenRouter-Categories | Optional | Assigns the application to a recognized marketplace category (e.g., cli-agent, ide-extension). Accepts a comma-separated list of up to two categories.8 |

When defining the request payload, the developer must supply the model parameter with the specific slug identifier (e.g., deepseek/deepseek-r1). OpenRouter also supports general aliases, such as \~openai/gpt-latest, which automatically routes the request to OpenAI's newest flagship model, shielding the application from breaking changes when legacy models are deprecated.8

#### SDK Typologies and Framework Abstractions

While Hermes manages the orchestration natively, it is crucial to understand the underlying integration methods OpenRouter provides to fully leverage the platform's capabilities. OpenRouter offers distinct Software Development Kits (SDKs) tailored for different levels of abstraction.

The Client SDK (@openrouter/sdk), available for TypeScript, Python, and Go, is intentionally lean. It provides a type-safe layer over the REST API, handling authentication and request validation directly. This SDK mirrors the OpenRouter API surface exactly, making it ideal for developers building custom orchestration loops who require direct, efficient access to model inference without restrictive high-level abstractions.8

Conversely, OpenRouter provides an Agent SDK (@openrouter/agent), currently supported only in TypeScript. This higher-level primitive is designed specifically for building AI agents, automatically managing multi-turn conversation loops, conversation state tracking, and tool execution via a callModel function.8 The Agent SDK allows developers to define tools using a tool() helper, complete with Zod schema validation for inputs. It executes inference loops that parse model outputs, execute the corresponding local tools, and append the results back into the conversation state until a specific stop condition—such as stepCountIs(limit) or maxCost(limit)—is met.8

While the OpenRouter Agent SDK offers a powerful foundational layer, the Hermes Agent framework supersedes it by providing a complete operating environment, including a terminal UI, cross-platform messaging gateways, daemon threading, and persistent memory subsystems that the standalone SDK lacks.1 Hermes essentially utilizes the lean API endpoint logic to power a much broader, production-ready agent swarm. Furthermore, OpenRouter natively supports an array of third-party frameworks, acting as a drop-in integration for LangChain, LlamaIndex, the Vercel AI SDK, and PydanticAI, ensuring broad interoperability if the developer chooses to expand the tech stack.8

### Credit Thresholds and Token Economics

Transitioning away from a flat-rate subscription like Claude Pro requires a deep understanding of OpenRouter's token economics and pay-as-you-go credit systems. The aggregation model fundamentally alters the cost curve of software development, replacing predictable but high monthly overhead with granular, consumption-based micro-transactions.

#### Account Funding Mechanics

OpenRouter operates entirely on a prepaid credit system for standard users. To make API calls to premium models, developers must purchase credits, with the platform enforcing a minimum transaction threshold of![][image1] and a maximum limit of![][image2] per transaction.9

The platform applies specific processing fees depending on the funding medium. Purchases made via credit card (processed by Stripe) incur a![][image3] markup, with a minimum fee floor of![][image4].10 Alternatively, developers can fund their accounts using USDC cryptocurrency via Coinbase, which incurs a flat![][image5] processing fee.10 Crucially, OpenRouter guarantees that these funding fees are the only markup applied; the platform passes through the raw input and output token pricing of the underlying model providers (like Anthropic or DeepSeek) without any secondary margin.7 Failed model executions or fallback attempts are never billed; charges are applied strictly upon successful model runs.7

Refunds for unused credits are strictly governed by a 24-hour policy. If a developer tops up an account and requests a refund within 24 hours, the transaction can be reversed. Beyond that window, the credits become permanently non-refundable.9

#### The Free Tier Unlock Mechanism

The most critical economic mechanic for the proposed architecture involves OpenRouter's free model tier. The platform hosts dozens of highly capable models entirely free of charge. However, newly provisioned accounts are subjected to severe rate limits on these free models—typically capped at a mere 50 requests per day.7 In an agentic workflow where the Hermes orchestrator generates hundreds of background calls for memory syncing, planning, and file indexing, a 50-request limit would be exhausted within minutes, causing catastrophic workflow failure.

To circumvent this, OpenRouter employs a cumulative purchase threshold. Once a user's account reaches a total historical credit purchase volume of![][image6], the platform permanently unlocks high global rate limits, upgrading the free tier allowance to 1,000 requests per month (or in some configurations, higher localized daily limits).7 It is important to note that this is a cumulative metric; purchasing![][image7] followed later by![][image8] satisfies the requirement.12 Furthermore, the user does not need to maintain a![][image6] balance; the mere act of having purchased that amount historically proves the account is not a bot, thereby preventing users from abusing the free models by spinning up infinite burner accounts.12

By depositing this nominal![][image6] balance, an operator effectively transforms a highly restricted, metered system into a pseudo-unlimited orchestration layer. The primary Hermes agent can run continuously in the background, consuming zero credits for its routine operations, preserving the purchased fiat balance strictly for high-complexity, premium model invocations.

### Strategic Model Tiering: The Free Orchestrator

The success of a bifurcated routing strategy relies entirely on selecting a highly efficient, zero-cost model to serve as the foundational orchestrator. This model must possess a massive context window to ingest entire code repositories, high inference throughput to maintain TUI responsiveness, and native function-calling capabilities to correctly trigger Hermes's local Python skills. OpenRouter provides several enterprise-grade models at zero cost that perfectly fit this operational profile.

#### Tier 1 Analysis: Flagship Free Models

The landscape of open-weight and heavily subsidized models has advanced to the point where models previously considered state-of-the-art are now available as zero-cost routing primitives.

| Model Provider & Slug | Parameter Class | Context Window | Key Architectural Characteristics |
|:---- |:---- |:---- |:---- |
| DeepSeek V4 Flash deepseek/deepseek-v4-flash | Not Disclosed | 1.05 Million | Designed for extreme inference speed and high-throughput workloads. Employs hybrid attention mechanisms for processing massive documents. Natively supports explicit reasoning effort toggles mapping to agent workflows.13 |
| OpenAI gpt-oss-120b openai/gpt-oss-120b | 117 Billion (MoE) | 131,000 | An open-weight Mixture-of-Experts model. While it contains 117B parameters, it dynamically activates only 5.1B per forward pass. Natively supports function calling, web browsing, and structured output generation.13 Optimized via MXFP4 quantization. |
| Poolside Laguna M.1 poolside/laguna-m.1 | 332 Billion | 262,000 | The flagship coding agent model from Poolside. Specifically optimized for complex software engineering and repository-level analysis. Runs efficiently on fp8 quantization and supports an extensive 8,000 output token limit.13 |
| Baidu Qianfan CoBuddy baidu/cobuddy | 28.6 Billion | 131,000 | Engineered specifically for code generation and AI Agent workflows. Operates on fp8 quantization to ensure low end-to-end latency. Uniquely supports up to 65,000 output tokens, making it ideal for rewriting entire application modules.13 |

For the central Hermes orchestrator, DeepSeek V4 Flash and OpenAI gpt-oss-120b emerge as the most optimal choices. The gpt-oss-120b model's MoE architecture ensures that it provides flagship reasoning logic while operating on a highly constrained compute budget per token, resulting in excellent instruction adherence for tool dispatching without hallucinating parameters.13 DeepSeek V4 Flash, conversely, offers a staggering 1.05 million token context window, allowing the orchestrator to keep vast amounts of session history, documentation, and error logs in working memory without requiring aggressive context compression.13

By assigning one of these models as the default in the Hermes framework, all standard user prompts, memory syncs, file reads, and basic shell commands are processed instantly and free of charge.

### Strategic Model Tiering: Premium Subagent Execution

While the free tier handles logistics, the orchestrator will inevitably encounter tasks requiring advanced mathematical logic, deep codebase refactoring, or highly nuanced semantic synthesis. These tasks must be delegated to Tier 2 premium models. The economics of these models vary drastically, and targeting them correctly is the core of this cost-saving strategy.

#### Tier 2 Analysis: The Cost of Premium Logic

The current pricing structure of frontier models reveals a massive disparity between proprietary API vendors and optimized open-weight reasoning models.

| Model Provider & Slug | Input Cost (per 1M tokens) | Output Cost (per 1M tokens) | Cache Hit Metrics | Operational Profile |
|:---- |:---- |:---- |:---- |:---- |
| Anthropic Claude 3.5 Sonnet anthropic/claude-3.5-sonnet |![][image9] |![][image10] | Reads:![][image11] Writes:![][image12] | The industry standard for coding tasks. Highly reliable, but carries a steep premium. Heavy usage can easily exceed $$20/month.6 |
| OpenAI GPT-4o openai/gpt-4o |![][image13] |![][image6] | Reads:![][image14] | High-speed multimodal processing with a massive 128K context. Offers a balanced cost profile compared to Claude.17 |
| DeepSeek R1 deepseek/deepseek-r1 |![][image15] |![][image16] | N/A | Flagship open reasoning model. Achieves performance parity with OpenAI o1. Employs explicit chain-of-thought before generating final outputs.19 |
| DeepSeek V3 deepseek/deepseek-chat |![][image17] |![][image18] | Hits:![][image19] | The most affordable high-capability general model. Ideal for applications where the extra reasoning capabilities of R1 are unnecessary.20 |
| OpenAI GPT-4o-mini openai/gpt-4o-mini |![][image20] |![][image21] | Hits:![][image22] | Small, highly affordable model. Excellent for mid-tier tasks and auxiliary agent functions like data compression.22 |

DeepSeek R1 represents a structural disruption in model pricing algorithms. At![][image15] per million input tokens and![][image16] per million output tokens, it offers reasoning parity with the world's most expensive models at roughly a![][image23] cost reduction.20 It is designed specifically for tasks requiring step-by-step logical thinking, complex code debugging, and multi-step analytical reasoning.20 The higher output cost relative to DeepSeek V3 reflects the model's internal chain-of-thought approach, which generates thousands of hidden reasoning tokens before producing a final formatted answer.20

Conversely, relying exclusively on Claude 3.5 Sonnet incurs significant financial drag. At![][image9] per million input and![][image10] per million output, a standard developer utilizing Claude Code as a daily driver can burn through substantial capital.6 OpenRouter's integration passes this cost directly to the user.23 However, by strictly reserving Claude 3.5 Sonnet or DeepSeek R1 for isolated, high-value subagent execution rather than routine orchestration, capital efficiency is maximized.

Furthermore, models hosted on OpenRouter benefit from advanced Prompt Caching mechanics. For example, when invoking DeepSeek V3, if the prompt shares a substantial prefix with recent calls, the cache hit drops the input cost from![][image17] down to just![][image19] per million tokens.20 Because the Hermes framework also maintains a built-in cross-session 1-hour prefix cache internally 24, repeated system prompts and codebase context injections are heavily subsidized by these backend architectural optimizations.

### System Configuration and State Management

To execute this architecture, the Hermes framework must be meticulously configured to utilize OpenRouter as the exclusive provider gateway, utilizing localized YAML configurations to dictate exactly which model handles which operational tier.

#### The Filesystem Hierarchy

Hermes manages its operational state, memory, and credentials through a strict filesystem hierarchy located in the user's home directory (\~/.hermes/). Understanding this structure is critical for maintaining an agent swarm.

| Directory / File | Core Functionality |
|:---- |:---- |
| config.yaml | The primary master configuration file. Stores non-secret settings including model routing, terminal backend preferences (e.g., Docker, SSH), UI settings, and agent reasoning toggles.25 |
|.env | The secure credential vault. Stores sensitive data such as OPENROUTER\_API\_KEY or custom webhooks. Never exposed to the model's context or committed to version control.25 |
| SOUL.md | Defines the primary agent identity. This file acts as slot \#1 in the system prompt injection, overriding default behavioral constraints.25 |
| memories/ | Directory containing persistent state data (MEMORY.md, USER.md). The agent reads from and writes to this directory to maintain cross-session continuity.25 |
| skills/ | The repository of executable logic. Contains agent-created or manually bundled Python scripts and workflow metadata.25 |
| logs/ | Operational telemetry (errors.log, gateway.log). The system automatically redacts API keys and secrets before writing to these files.25 |

#### Execution Blueprint: Configuration Commands

Hermes strictly enforces a configuration precedence hierarchy. Settings are resolved from highest to lowest priority: (1) CLI arguments per-invocation, (2) config.yaml definitions, (3).env environment variables, and finally (4) hardcoded built-in defaults.25 The framework employs a rule of thumb: secrets go in.env, while routing logic goes in config.yaml.

To initialize the OpenRouter connection securely, the developer must execute:

Bash

hermes config set OPENROUTER\_API\_KEY sk-or-…

The hermes config set command acts as an intelligent router; it detects that the key being passed is a secret and automatically shunts it into the.env file, bypassing config.yaml entirely.25

Next, the developer establishes the free orchestrator by editing the config.yaml directly or using the CLI. The default model must perfectly match the OpenRouter slug format.

YAML

\# \~/.hermes/config.yaml

model:

  default: "openai/gpt-oss-120b"

  provider: "openrouter"

agent:

  max\_turns: 60

  reasoning\_effort: medium

This ensures that the primary daemon process running the TUI uses the zero-cost MoE model for all standard interactions.27

#### Auxiliary Model Specialization

Hermes utilizes auxiliary models for peripheral tasks that run parallel to the main conversation thread. These side-jobs include context compression, visual image analysis, tool execution approval scoring, session-title generation, and skill vector search.28 Because these tasks occur frequently in the background but are computationally shallow, they represent a hidden vector for token expenditure if left unconfigured.

The config.yaml allows for independent overrides of every auxiliary slot. By utilizing environment variable substitution (${VAR\_NAME} syntax), developers can map these slots to specific fast, cheap models.25

YAML

\# \~/.hermes/config.yaml (continued)

auxiliary:

  vision:

    model: "google/gemini-flash-1.5"

    provider: "openrouter"

  compression:

    model: "openai/gpt-4o-mini"

    provider: "openrouter"

In this configuration, image analysis is routed to Google's highly efficient multimodal Flash model, while conversation history compression is handled by OpenAI's ultra-cheap gpt-4o-mini, which costs a negligible![][image20] per million input tokens.22 This micro-segmentation ensures maximum capital efficiency.

### Autonomous Subagent Delegation and Parallelization

The true power of this dual-tier architecture is fully realized through Hermes's native subagent delegation mechanics. The framework ships with a core bundled skill titled Subagent Driven Development, which codifies how complex implementation plans are broken down, assigned to child instances, and routed to premium models.29

#### The Delegation Configuration Block

To ensure that complex tasks utilize capable reasoning models while preserving the free orchestrator, the delegation block must be defined in config.yaml. This explicitly overrides the model selection whenever the orchestrator spawns a child instance.30

YAML

\# \~/.hermes/config.yaml (continued)

delegation:

  model: "deepseek/deepseek-r1"

  provider: "openrouter"

Under this configuration, when the free primary orchestrator (e.g., gpt-oss-120b) decides a task is too complex and triggers the delegate\_task tool, the newly spawned subagent will automatically authenticate against OpenRouter requesting deepseek-r1.30 The parent agent remains on the free tier, managing the user interface and conversation context, while the child agent burns compute credits exclusively to solve the algorithmic problem.30

#### Parallel Workstreams and Context Quarantine

The delegate\_task tool allows the agent to spawn multiple isolated child instances to work on tasks concurrently.31 Each subagent receives its own isolated conversation context, its own restricted toolset, and operates in a separate daemon thread.24

This creates a critical context quarantine mechanism. When dealing with complex debugging or parallel research tasks, intermediate tool calls, raw shell outputs, and erroneous reasoning steps generate massive amounts of token noise. If processed sequentially by a single model, this noise floods the context window, degrading the model's instruction adherence and drastically inflating costs. By delegating, intermediate data is trapped within the ephemeral child process. When the subagent completes its objective, only the final, synthesized summary is injected back into the parent orchestrator's context window.30

For example, an orchestrator can execute a parallel research pattern:

Python

\# Internal Hermes Execution Logic via delegate\_task

delegate\_task(tasks=},

  {"goal": "Analyze RISC-V server chip adoption metrics", "toolsets": \["web"\]},

  {"goal": "Review practical quantum computing applications", "toolsets": \["web"\]}

\])

Hermes will simultaneously spawn three independent deepseek-r1 instances. They will browse the web asynchronously, compile their findings, and return three concise summaries to the free orchestrator.31 This pattern reduces latency by running requests in parallel rather than sequentially, directly mitigating the timeout failures associated with single-threaded CLI tools. Furthermore, it enforces a systematic two-stage review process (specification followed by quality assurance) by ensuring fresh contexts are utilized for every distinct subtask.29

### Dynamic Routing, Pareto Code, and Fallback Resilience

While OpenRouter offers automated routing features built into its gateway, implementing them within an autonomous agent framework requires careful strategic consideration to avoid unpredictable cost spikes and systemic failures.

#### The Auto-Router Trap in Agentic Workflows

OpenRouter provides an endpoint designated as openrouter/auto, which utilizes a meta-model to dynamically route prompts to one of dozens of available models.32 The routing algorithm attempts to optimize for the best possible output based on a tunable cost\_quality\_tradeoff parameter ranging from 0 (pure capability regardless of cost) to 10 (maximum cost reduction).34

However, operational data and industry consensus strongly advise against utilizing openrouter/auto as the foundational engine for autonomous agents like Hermes.35 In an agentic workflow, the system generates dozens of background calls that are hidden from the user interface. Because the Auto-Router algorithm operates as an opaque black box, it may unpredictably route a trivial file-reading task to an expensive flagship model like Claude 3.5 Sonnet simply because it detects complex syntactic formatting within the file.35

This silent routing burns substantial credit reserves without explicit user consent. Furthermore, there is no pre-request notification of the selected model; the developer only discovers the token expenditure when reviewing the OpenRouter billing dashboard.35 By surrendering control to an auto-router, operators lose deterministic control over system latency, failure modes, reasoning depth, and budget constraints.35 Therefore, the explicit, hierarchical routing via the Hermes config.yaml (as outlined above) is mathematically safer and operationally superior.

#### The Pareto Code Router

If dynamic routing is strictly required for certain advanced execution tasks, OpenRouter offers a specialized router named openrouter/pareto-code.32 The Pareto router is distinct from the generic auto-router; it is specifically designed for agentic software engineering. It automatically bifurcates workloads, forwarding complex mathematical and logical reasoning to top-tier flagship models while routing simple background formatting tasks to fast, low-cost models.36

To implement this safely without risking massive background billing, the Pareto router must only be utilized within the delegation override block or specifically assigned to auxiliary tasks, never as the default orchestrator.38

YAML

\# \~/.hermes/config.yaml (Safe Pareto Implementation)

delegation:

  model: "openrouter/pareto-code"

  provider: "openrouter"

By restricting Pareto routing to the subagent tier, the operator ensures that dynamic model selection is triggered exclusively when the primary (free) orchestrator explicitly delegates a heavy workload.36

#### Fallback Chains and Execution Resilience

Operating a multi-agent system on a third-party aggregator inherently introduces network dependency risks. Upstream provider outages, transient HTTP 500 errors, or sudden rate limit enforcements (HTTP 429\) can abruptly sever the autonomous execution loop.

Hermes addresses network fragility through a robust, configurable fallback provider mechanism.24 Operators can construct a prioritized chain of backup models. If the primary OpenRouter model invocation fails, Hermes catches the network exception locally and instantaneously redirects the identical JSON payload to the next model in the predefined chain.38

YAML

\# \~/.hermes/config.yaml (Fallback Configuration)

fallback:

  \- provider: "openrouter"

    model: "anthropic/claude-3.5-sonnet"

  \- provider: "anthropic"

    model: "claude-3-5-sonnet-20241022"

This specific fallback architecture provides immense resilience. If a delegated deepseek-r1 subagent on OpenRouter experiences a timeout, the system seamlessly fails over to claude-3.5-sonnet on the same OpenRouter gateway. If the entire OpenRouter gateway itself goes offline due to a DDoS attack or maintenance, the system bypasses the aggregator entirely and routes the payload directly to Anthropic's native proprietary API.38 This multi-layered redundancy ensures near-zero downtime for critical production deployments.

### Advanced Topologies: Multi-Node Swarms and Distributed State

As the scope of the project expands, developers eventually hit a hardware bottleneck. While the heavy LLM inference is offloaded to OpenRouter's cloud infrastructure, Hermes relies on local hardware for vectorizing data, maintaining the FTS5 SQLite search database, sandboxing local Python code execution, and managing the daemon processes.1 The active orchestration layer continuously reads and writes complex memory states to disk.

To scale beyond a single workstation, advanced teams utilize distributed multi-node orchestration, transforming Hermes from a single assistant into a distributed swarm operating across different machines and platforms.40

#### Shared Memory and Networked Filesystems

The primary challenge in multi-node orchestration is not routing the API calls—OpenRouter handles that effortlessly—but rather establishing shared context and state across disparate physical machines.40 If Node A orchestrates the frontend changes, and Node B is assigned backend API modifications, Node B must possess perfect contextual awareness of Node A's data models to prevent integration failures.

A highly effective topology involves utilizing centralized Network File System (NFS) shares backed by ZFS storage arrays.42 For example, a central server (e.g., an Asustor Flashtor equipped with NVMe ZFS datasets) acts as the central repository.42 Multiple headless Linux machines (LLM nodes) are configured with 32-64GB of RAM and multi-core CPUs. Hermes is installed bare-metal on each node as a systemd service, running continuously in the background.42

Each node is configured to mount a centralized NFS project share directly to its local \~/.hermes/project directory.42 Because Hermes writes its operational context, agentic memory logs, and skill metadata directly to this mounted filesystem, the state becomes immediately visible to all other agents in the network. This eliminates the necessity for complex orchestration middleware; the filesystem itself acts as the source of truth for the swarm.

#### Immutable Repositories and Automated DevOps

To prevent agents from overwriting each other's code during simultaneous execution, the swarm must adhere to strict DevOps protocols. This is achieved by integrating the Hermes agents with a centralized version control system, such as a locally hosted Forgejo container.42

The Forgejo instance is partitioned into distinct organizations: a production organization (immutable, human-controlled) and a testing organization (agent-controlled).42 When a Hermes agent receives a task via a cross-platform messaging gateway like Discord or Telegram 1, it treats the production repository as absolute, immutable truth. The agent pulls the code, executes its OpenRouter-backed reasoning loops to generate new logic, and pushes its completed work entirely to the testing repository.42

The human operator, serving as the sole merge authority, reviews the agent-generated pull requests before merging them into production.42 By coupling Hermes's advanced logic delegation (subagents running DeepSeek R1) with immutable, distributed state management (NFS and Forgejo), an individual developer can effectively orchestrate a virtual engineering department operating continuously in the background at an incredibly low capital cost.

### Operational Interface and Continuous Switching

Managing this infrastructure requires seamless control interfaces. Hermes Agent intentionally avoids web-based UIs for its primary control loop, favoring a highly robust Terminal User Interface (TUI).5 The TUI is engineered for power users, featuring multiline editing, slash-command autocomplete, instant interrupt-and-redirect functionality (using Ctrl+C to cancel errant generations without terminating the daemon), and streaming tool output.5

While the config.yaml manages the baseline models, the operator will frequently need to temporarily upgrade the main orchestrator for specific, highly complex planning sessions. Hermes allows for continuous, on-the-fly model switching through custom aliases defined in the configuration.28

YAML

\# \~/.hermes/config.yaml

model\_aliases:

  cheap:

    model: deepseek/deepseek-v4-flash

    provider: openrouter

  heavy:

    model: anthropic/claude-3.5-sonnet

    provider: openrouter

By establishing these aliases, an operator can seamlessly transition the orchestrator's capability mid-session. Typing /model heavy in the TUI immediately elevates the active session to the premium OpenRouter model for a single complex prompt, bypassing the need to restart the agent or edit YAML files manually.28 Once the complex planning is complete, issuing /model cheap reverts the session back to the zero-cost tier, ensuring that subsequent routine commands do not unnecessarily burn the prepaid credit balance.28

### Conclusion

The integration of the Hermes Agent framework with the OpenRouter API represents a structural evolution in agentic software engineering. By systematically abandoning the limitations of monolithic, single-provider subscriptions and blocking CLI wrappers, developers can construct dynamic, task-based model orchestration pipelines that achieve vastly superior system resilience while simultaneously reducing operational expenditures by magnitudes.

The cornerstone of this architecture is the deliberate isolation of execution states using daemon threads, completely resolving the systemic timeout failures endemic to legacy tools. This technical capability is married to a highly optimized economic strategy: by depositing the requisite credit threshold on OpenRouter to unlock the free model tier, developers can lock the persistent, "always-on" orchestration layer to highly capable zero-cost models like DeepSeek V4 Flash or gpt-oss-120b. This configuration effectively nullifies the baseline cost of running continuous autonomous agents.

Consequently, prepaid capital is preserved entirely for the deployment of premier reasoning engines—such as DeepSeek R1 or Claude 3.5 Sonnet. By strictly enforcing model selection through Hermes's delegation configuration blocks, these expensive models are utilized exclusively within quarantined, ephemeral subagent workflows. This prevents costly token inflation caused by context window pollution, ensuring that developers only pay for pure logical reasoning, not background operational noise.

Executing this architecture demands a meticulous understanding of OpenRouter's credit mechanics, Hermes's hierarchical configuration precedence, and the precise YAML structures necessary to map capabilities to specific task vectors. However, when deployed utilizing distributed filesystems, strict DevOps protocols, and robust fallback chains, this system transcends basic prompt engineering. It creates a scalable, infinitely adaptable intelligence layer capable of orchestrating complex parallel engineering tasks with unparalleled economic efficiency, fundamentally altering the productivity potential of the individual developer.

#### Works Cited

1. NousResearch/hermes-agent: The agent that grows with you \- GitHub, accessed on May 27, 2026, [https://github.com/nousresearch/hermes-agent](https://github.com/nousresearch/hermes-agent)
2. Integration with Hermes Agent \- OpenRouter, accessed on May 27, 2026, [https://openrouter.ai/docs/cookbook/coding-agents/hermes-integration](https://openrouter.ai/docs/cookbook/coding-agents/hermes-integration)
3. Hermes Unlocks Self-Improving AI Agents, Powered by NVIDIA RTX PCs and DGX Spark, accessed on May 27, 2026, [https://blogs.nvidia.com/blog/rtx-ai-garage-hermes-agent-dgx-spark/](https://blogs.nvidia.com/blog/rtx-ai-garage-hermes-agent-dgx-spark/)
4. Hermes Agent | OpenRouter, accessed on May 27, 2026, [https://openrouter.ai/apps/hermes-agent](https://openrouter.ai/apps/hermes-agent)
5. CLI Interface | Hermes Agent \- nous research, accessed on May 27, 2026, [https://hermes-agent.nousresearch.com/docs/user-guide/cli](https://hermes-agent.nousresearch.com/docs/user-guide/cli)
6. How to Use OpenRouter with Claude Code: Run Cheaper Models as a Backend, accessed on May 27, 2026, [https://www.mindstudio.ai/blog/how-to-use-openrouter-with-claude-code-cheaper-models](https://www.mindstudio.ai/blog/how-to-use-openrouter-with-claude-code-cheaper-models)
7. Pricing \- OpenRouter, accessed on May 27, 2026, [https://openrouter.ai/pricing](https://openrouter.ai/pricing)
8. OpenRouter Quickstart Guide | Developer Documentation …, accessed on May 27, 2026, [https://openrouter.ai/docs/quickstart](https://openrouter.ai/docs/quickstart)
9. Terms of Service \- OpenRouter, accessed on May 27, 2026, [https://openrouter.ai/terms](https://openrouter.ai/terms)
10. OpenRouter FAQ | Developer Documentation, accessed on May 27, 2026, [https://openrouter.ai/docs/faq](https://openrouter.ai/docs/faq)
11. Support | OpenRouter, accessed on May 27, 2026, [https://openrouter.ai/support](https://openrouter.ai/support)
12. Do I need any minimum credits to use free models like Horizon Alpha?: r/openrouter, accessed on May 27, 2026, [https://www.reddit.com/r/openrouter/comments/1mdwxmr/do\_i\_need\_any\_minimum\_credits\_to\_use\_free\_models/](https://www.reddit.com/r/openrouter/comments/1mdwxmr/do_i_need_any_minimum_credits_to_use_free_models/)
13. Free AI Models on OpenRouter, accessed on May 27, 2026, [https://openrouter.ai/collections/free-models](https://openrouter.ai/collections/free-models)
14. Models | OpenRouter, accessed on May 27, 2026, [https://openrouter.ai/models](https://openrouter.ai/models)
15. Claude Sonnet 4 \- API Pricing & Benchmarks \- OpenRouter, accessed on May 27, 2026, [https://openrouter.ai/anthropic/claude-sonnet-4](https://openrouter.ai/anthropic/claude-sonnet-4)
16. Claude 3.5 Sonnet–AI Vista | Ai Reviews, accessed on May 27, 2026, [https://aivista.co.uk/aivista-reviews/claude-3-5-sonnet/](https://aivista.co.uk/aivista-reviews/claude-3-5-sonnet/)
17. GPT 4o API Pricing 2026 \- Costs, Performance & Providers \- Price Per Token, accessed on May 27, 2026, [https://pricepertoken.com/pricing-page/model/openai-gpt-4o](https://pricepertoken.com/pricing-page/model/openai-gpt-4o)
18. GPT-4o \- API Pricing & Benchmarks \- OpenRouter, accessed on May 27, 2026, [https://openrouter.ai/openai/gpt-4o](https://openrouter.ai/openai/gpt-4o)
19. R1 \- API Pricing & Benchmarks \- OpenRouter, accessed on May 27, 2026, [https://openrouter.ai/deepseek/deepseek-r1](https://openrouter.ai/deepseek/deepseek-r1)
20. DeepSeek API 2026: Complete Pricing, Setup & V4/R1 Cost Guide | NxCode, accessed on May 27, 2026, [https://www.nxcode.io/resources/news/deepseek-api-pricing-complete-guide-2026](https://www.nxcode.io/resources/news/deepseek-api-pricing-complete-guide-2026)
21. R1 API Pricing 2026 \- Costs, Performance & Providers \- Price Per Token, accessed on May 27, 2026, [https://pricepertoken.com/pricing-page/model/deepseek-deepseek-r1](https://pricepertoken.com/pricing-page/model/deepseek-deepseek-r1)
22. OpenAI: GPT-4o-mini–Effective Pricing | OpenRouter, accessed on May 27, 2026, [https://openrouter.ai/openai/gpt-4o-mini/pricing](https://openrouter.ai/openai/gpt-4o-mini/pricing)
23. OpenRouter Pricing 2026: Plans, Costs & Real Fees \- CheckThat.ai, accessed on May 27, 2026, [https://checkthat.ai/brands/openrouter/pricing](https://checkthat.ai/brands/openrouter/pricing)
24. Features Overview | Hermes Agent, accessed on May 27, 2026, [https://hermes-agent.nousresearch.com/docs/user-guide/features/overview](https://hermes-agent.nousresearch.com/docs/user-guide/features/overview)
25. Configuration | Hermes Agent \- nous research, accessed on May 27, 2026, [https://hermes-agent.nousresearch.com/docs/user-guide/configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
26. Quickstart | Hermes Agent \- nous research, accessed on May 27, 2026, [https://hermes-agent.nousresearch.com/docs/getting-started/quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart)
27. Complete Hermes Agent Setup Guide: r/hermesagent \- Reddit, accessed on May 27, 2026, [https://www.reddit.com/r/hermesagent/comments/1rt5syt/complete\_hermes\_agent\_setup\_guide/](https://www.reddit.com/r/hermesagent/comments/1rt5syt/complete_hermes_agent_setup_guide/)
28. Configuring Models | Hermes Agent \- nous research, accessed on May 27, 2026, [https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models](https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models)
29. Subagent Driven Development—Execute plans via delegate\_task subagents (2-stage review) | Hermes Agent, accessed on May 27, 2026, [https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/software-development/software-development-subagent-driven-development](https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/software-development/software-development-subagent-driven-development)
30. Subagent Delegation | Hermes Agent, accessed on May 27, 2026, [https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation)
31. Delegation & Parallel Work | Hermes Agent \- nous research, accessed on May 27, 2026, [https://hermes-agent.nousresearch.com/docs/guides/delegation-patterns](https://hermes-agent.nousresearch.com/docs/guides/delegation-patterns)
32. Auto Router \- API Pricing & Providers \- OpenRouter, accessed on May 27, 2026, [https://openrouter.ai/openrouter/auto](https://openrouter.ai/openrouter/auto)
33. Models \- OpenRouter, accessed on May 27, 2026, [https://openrouter.ai/OpenRouter](https://openrouter.ai/OpenRouter)
34. Auto Router | Smart AI Model Selection | OpenRouter | Documentation, accessed on May 27, 2026, [https://openrouter.ai/docs/guides/routing/routers/auto-router](https://openrouter.ai/docs/guides/routing/routers/auto-router)
35. openrouter auto-mode is a trap. it picks opus when you need flash and you dont find out until the bill arrives \- Reddit, accessed on May 27, 2026, [https://www.reddit.com/r/AskClaw/comments/1t4h505/openrouter\_automode\_is\_a\_trap\_it\_picks\_opus\_when/](https://www.reddit.com/r/AskClaw/comments/1t4h505/openrouter_automode_is_a_trap_it_picks_opus_when/)
36. \*\*Which model do you use with Hermes to balance token usage and reasoning quality?\*\*: r/hermesagent \- Reddit, accessed on May 27, 2026, [https://www.reddit.com/r/hermesagent/comments/1tg1pal/which\_model\_do\_you\_use\_with\_hermes\_to\_balance/](https://www.reddit.com/r/hermesagent/comments/1tg1pal/which_model_do_you_use_with_hermes_to_balance/)
37. OpenRouter ships Pareto Code, Hermes Agent rivals OpenClaw, accessed on May 27, 2026, [https://codenewsletter.ai/p/openrouter-ships-pareto-code-hermes-agent-rivals-openclaw](https://codenewsletter.ai/p/openrouter-ships-pareto-code-hermes-agent-rivals-openclaw)
38. AI Providers | Hermes Agent \- nous research, accessed on May 27, 2026, [https://hermes-agent.nousresearch.com/docs/integrations/providers](https://hermes-agent.nousresearch.com/docs/integrations/providers)
39. Hermes Agent \+ Pareto Code is Insane (FREE\!): r/AISEOInsider \- Reddit, accessed on May 27, 2026, [https://www.reddit.com/r/AISEOInsider/comments/1tb356l/hermes\_agent\_pareto\_code\_is\_insane\_free/](https://www.reddit.com/r/AISEOInsider/comments/1tb356l/hermes_agent_pareto_code_is_insane_free/)
40. Anyone here using ai agent orchestration software to control multiple hermes agents? I'm retired and have some extra hardware: r/ollama \- Reddit, accessed on May 27, 2026, [https://www.reddit.com/r/ollama/comments/1ss19jx/anyone\_here\_using\_ai\_agent\_orchestration\_software/](https://www.reddit.com/r/ollama/comments/1ss19jx/anyone_here_using_ai_agent_orchestration_software/)
41. Feature: Multi-Agent Architecture—Orchestration, Cooperation, Specialized Roles & Resilient Workflows · Issue \#344 · NousResearch/hermes-agent \- GitHub, accessed on May 27, 2026, [https://github.com/NousResearch/hermes-agent/issues/344](https://github.com/NousResearch/hermes-agent/issues/344)
42. Anyone here using ai agent orchestration software to control multiple hermes agents? I'm retired and have some extra hardware \- Reddit, accessed on May 27, 2026, [https://www.reddit.com/r/hermesagent/comments/1srvvs0/anyone\_here\_using\_ai\_agent\_orchestration\_software/](https://www.reddit.com/r/hermesagent/comments/1srvvs0/anyone_here_using_ai_agent_orchestration_software/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAAAZCAYAAAChBHccAAACPklEQVR4Xu2WPUiXURTGT1kUEkVgkfgRBEVEQ9AWTbmIDkIIomJIUxBIFBRBThE5hEhDS+Akoii0tTiaLk4FGUQNptYS2iJF3+fxnvP33NO9b/9R4f3Bw3vPc57363+v95WoZPvQ7Y2dQhvrD6vLN7Yzuyk89LAcH8jxiA0xX1h9rMOsQ6xO1nqUKGaKwnUXWbWup1xlfWL9ZA25XhIEz8sYF1fsWGuvxiiRZi+FbLPUNVLXVxKBadZHU4+x1kydJPXAn50PUD9kPWG1uF4Rs6wV5z2i9PX3JLxW50Ug0GDG4BmFGbH4m1ULzsMLWy6Ir4y4WoH3zpsWBKBrcsxR1MuhS+Se84+Lf1nq71J79NmyHKOtEPSVdTJKBNB7y3rNmqcwM36aPeconHfT+dgM4N+ROveQOT8Cv9BLil/iYJQI3j5TPxeviEsUMgPOx44F/6nUuYfM+UkQtDNRxGkKmUHfMJyikLnh/Drx70udu1/Or7DE6pexBs+asYLZsej34Y3zLbsoZO46v0n8XqmxBP39wH8fHs1lM7a+gr941PuNd0C8F8ZLgUxut9G9fkZqD7zf3rT8MGO9wAkzBh9YG6YG2H+R6TEeXu66qcEv1ivn3ab4+rpUPfBuedOCPXZcxgjrFxHrVcE0vzc1+EZhZ7LgPOiM8S6KZ0H92Hn4hSdM3U7/npcE/03qusNMHI3bm1yh0F+V41zc3qSDteBN2vqlJyns6aNxuwJ62I7xVUYeS7NqqnrTkpKSkpIdwV8xIq2swJM0ngAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGEAAAAZCAYAAAAhd0APAAADwElEQVR4Xu2YWchNURTHl6koScpQIplKFKW8eEDGJEkib8IDT6ZSEikppYTwgoh4kIyZRRkypShTCaHMIfMU1v/be3133XX3vmffvnwe7F+tzlr/vc6+65xz9z57H6JMJhNmqhUyjctYtt9sU2xD5u/TlNzNX+2PK/yxvU7ynCDX9pZtumkDB9g2svVga8LWn+0Y2wCdlEhPtsvkfu+UadNsJpfzmK2raROGsd0ll7fTtBWxhO0922e2GaZNSK01yk+2gd5HJ4L2JW7hfUxbiF+Wmus473VttV40GELlv4+HaOsBv9hGqRg5Y1QM5pPLE2ZRuK8Qt9lOqvgm2wUVg9RaqxK68a+NfpRtv4rBYXI545V2hm0e2w62BUqvFfQ722jf2S6peDlVXuy4gIa4T0BbaTRLG6rsC0Bra+KiWgtBJ52VD/aRGyECfLRNUlpfr71QGoYipqGG0IFcvzhqZCoU4OOfaoHexfsTfGz5RmFdc53COdAwBYLUWgtBMqzaMMVD2m60oeTyrykNQ7ehD2EphevYSpUPITT/Ql/n/dM+tjyksK6R+2LRemqthXSiUsewL2y9yjLCHCeX389oc8gNx22+HQ+3FjDthS5gA5Xr8A+qWICO6RO887HlFoV1jb7ZGq2n1ppEM7YbVPoBGObEGMhHzlWj46YsU3FLcnkjlFbEWQpfwFpyOkalrOj2lmU4oN9TfqgvudZqxM7VekqtNYMT9ciIgdGip6FqFPVl2UXh/PXk9OY+hm8XCwD6Oe8/9bEFq5yQronVrfXUWgt5xDbN+9IhpphQ5wBDebcVPbKE1cQuJkZsnt1C5Tp8TH8W6Ju8H3sn3KewronVrfXUWgtB8hPla92yh9xmTiPnYqOEc7B01cQuJsZgcvlFKw74sdWR7PoX+9iSsjr6QOEcaHe8n1prIT+ULyd2V76wkCrXwx3JvYSAnDOy1FwHNL3cBTMpvCMXcM5Eo31ke6NiPABb46CAhrhdQDtkNDwwzWSq7AtAk82txEW1FrKG3NwG0CGmFBx712cQDfdayEarPMR4aQqLvIYXtIBPGXJuDPyT9IPDshf53ZSGG2v7xr/Xvquek1uSCvLO01PnXK/pPQ+Apld3q7ymSak1CXyGkA0ZRoYdXvqmW9M3HT6Wp+hD2lurduEK2ysrGrCC+URuCkQ/oRUWNLThmxW+Z10sb64HXwBwg4+Qy8eotTygyp11K3L5qBf1fKXwPiil1mTQQWNhp6jMP0DW8pl/xDMKD+tMIxL77p/JZDKZzH/LHy2YWX2X/gzWAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAZCAYAAACo79dmAAACC0lEQVR4Xu2Vv0uXURTGj6VNBilaSLoIoojgFtJiDRbR7BDkooObqKggCg6mf0DQkEsEDepUEEFbbYJKkIPQFs2CiiiRv57H+96v5x7fX18Hi3g/8PDe89xzvu+93/vjFSn4P3gK3bCmodsaf4MT6BG0Ac2bPs80tGZNywi0BLVHcRv0DhouZSSzDc1CTVAl1AWtBxki36G3KubAqQWoBxpSXiYv5DzZ61uQkYytozh5DT1uAc+eat+JnvxzOpSfyAz0UtzsuRTXw+5UOJBJcbWDps/DnG4Vf1FtUis5lt/DAT60Zk4OrREDB9ur4iPVJrmW3zMllx/sH2vE8AHaVPFP1V6WnMvv4TLOiZvhm+j5OshI5jf0CtqBFsXV3g8yHFvQV3H9FZF3G1otZeRkFPpsPP4oT3kWu9BjFd8TV8t9mIVe/mvirrVfUbss+ENl7SUF6ziJNLg1/FVJWFOt2on4ZdHwEKQWRVRZQ7In2gCtqHhAwvznUKeKA5jIPWW9tBeSPnE548bPqrV93ILauwVNqDgg7wt5/fhLnPSLy7mrPELvh/E8n6AW4/Hrqd9VIxfHU2IfqlfxA3HFrcrjVombgI0/xnieRrn4QSBPJKzhiiVuA8Jt4AdDNYfdZ7yHxoxXJy6fVxefBxJ/BkjSJMgxdDNqp+VdCc/EHaw0+LGgyr66CgoKCv5RTgHzX37RI+5QEAAAAABJRU5ErkJggg==>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAAAZCAYAAAChBHccAAACEklEQVR4Xu2WTyutURTGl39FSQZIMXCVW2TmS4hiRmZyDW4Zmpgok1tKyQcwlAyUMmQkmVBCIjLRLVJSKG6XsB57r3PWXmfvw5B6f/X0rvWsdZaXvc/eiDK+DkPW+C70sF5Zg7bwlSkl99Kz/vnHP+t1k2eSdcd6YP0ytWKUsw7Izb1itYblHCOsS9Yza9rUoqCxy8cYLugYHLHWVX7I2lJ5MZ5YJSq/ZY2qHCyzLlS+wLpReZTYC18bv8bkArxaaxpWWe3WpMJ5yLFC1us2XgAamlQMVsitiLCnahp489Y0oGfJeFgFPW/O5AK8M2tq0AD99s8Y0mNJ+Zo1KnyJXXLfH+E/xed8OL+R8k3QI6st6EgPSfkWPf+ENRVU03NSfkAZa5/CH4J9LqSGpHxLJYWz7RcxNSflR0GjXgntx4akfM0Pcj3Y5y0+hnDkCqk5KT/HOWvYx9LYqWLxY0NSvgb1OuNteF/uEhwOsTkfzkfxr4q1L9ybXIB3bE0FXi72OQB/wse4P2J98F6sqcEFIsgA3IB62IDJBXhywQHs7TGVg9jnAPxmH8tWtcAbt6YGZ+yij9Fc4Z8/cx35Go5TYcZ7GuRQh/Kwt3FcavrIraYGf2F9H/RS4fwo+G9S9h1WoiEsv1NFrr5N7mT6R+GVD/pZO8YDp+Q+i2NSZsTAeY/eTXJ91WG5OJ/6TTMyMjIyvgVvl6S2/5UR4MAAAAAASUVORK5CYII=>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAZCAYAAACo79dmAAACCElEQVR4Xu2VyytvURTHl6trdG9xy+OWkZJHyp/wY0DJxOQOFCMTIyFXiTLwyNiMiRQDRqRu3YncmaLkFRNJStRVBlIGHutrn/2z9jr7HL+fAdL51Lez13evc/Y6Zz8OUcLnoJmVp01FShvvwQOrkbXLGld9liHWpjY1PawFVnUQV7LmWN3pjHjqWYdkCppXfWCHNSti5EHTrAZWl/BeZJSek622nIxoeln3Iu6k8KCIsQQs16JdHFzxcWqEH8kwa5LM22Mqct3uWFBIlcebUHFKxGuiDX5QBtNvQYGYymxpofBXBLfk+mj/EvGdaAPfMyIZpNcVu0r+gY7J9ZdZByI+Ee1FynD6LQOsMTIDzATXKSfDzxX5i92nsH/J+hf4OYFXxNpIZ2QINslf5eGhI8rTIEcXBbbJ72tkzhcyx9pp0M6KqEIkZ+TP2SO/L8HSsEclQP430Y7ETosEmyD2Jopes0fk9y0/Wesi7iA3v41VK2IHJGJNaS9uQICN6cvRp4FG92EJSi+f1S9iByT+9nj6oTh+7CFuQQ7OSe2tKM/yh1WuPPw95VgFFK4nzQ2rUMR1ZG6uEB6Wiu8FzskcVZYSMjlfhWcppfAPATSR+9x2ilkGAMvAFgOVud1PLLH6tMn8Z12Q+WpR9wL9ohL8sr8H7bi8N6GVzMaKAz8LKOujKyEhIeGD8gg8cYR7GfZuMAAAAABJRU5ErkJggg==>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAWCAYAAACCAs+RAAACU0lEQVR4Xu2WPWgWQRCGJ8YfRLERJWAjRq1ERCtRYmMhahOJioUoFmIKIWCXIoUgWImKKSWNJAqBWFmYVNr419iJ2IhoGrHwF4wmmfd2h3tvvtlErIx8Dww7887cft/c7u2dSJt/n1NeWIocVptTO+kTS4Vlkhq4lscredzARcRytZ9eJLaqPZU0x5TLLcY5tWm1X2pXXc5Yo/ZQ0vzP1TosgYv2ZB9Jg33wKmtmEQekmdvl4oUYV/tA8R21TxSDTZLmW53j9TmuiP78R6czn6Wcg97vNKzeE6dF4FqsttcOUfxN7R7F4IU5KEan5oMJSSsVUWpkoyQdI2PbYCGuS1wD7Y2LT1AMBs1BEnYhj4tRamRIYn1EYp3BqkU19t9AT/b31+mKM+Z0SX0B7IfaNksGlBq5L7E+LLHO8B9mWB/I/u46XXGcg061l9JsaB0XEKVGHkms35Ck2/aN+JNGLmd/Z52u6HVxBQp5hSJKjYxKrN+SpPsHmSn9Huvns4+TkOkz563a2ezbRTvI95QaKT0jtyXWGRwsUQ03Ys/I3jpdcdocJN+Rz3pEqZF9kvS/ObUmJa6BNpv9VTkunlozJNpkW8j3lBoB0I857au0vtguqq2k2LazB9olF9+kGDwwB2c49jdA4Yo8brcCx3eJfxTg7vP7B58PqN1Mmr3t/Ry483cpPiKtNbj7XmvE+Oq1fYoV8tsDfJH0HYRtCHsv6U53c5Gk0w9vYHxyYL6DzXTFM7WjXpT0Pnmt9ljStWub6Yoxtd95RA2O5RZ8t23atPkPmAfT3MR3YofKHgAAAABJRU5ErkJggg==>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAAAZCAYAAAChBHccAAACHklEQVR4Xu2Wz0tVURDHpyyIkEAwKSKFIBfhQmiXrVpFLgRdiAgiLSoIJBKUoF0ELkTChRuhVUSh4B/g0qVtdKEgbsQfEYpGG0ErnS9n5jlnPPd5lgr3A1/uzHfG8+bdezz3EZWcH3q8cVF4xjpidfvCeeYyhaHH5PpRrjdtU4I/rC5vVmGKwrpLrOuupjxn/WT9ZY24WhI0PpQYiys29rykUM8Z/iqF3kbJayS/XekITLO2TP6FtWvyJKmBd5zv2ab84edYG84bpdPrI7+S8J46LwINd0wMZig8kRS/5Zo7PPomnPdIfOWTyxV4q960oAF6Jddq9LH6Jc4ZXrfIe+c3id8p+YHkHp2tkFt00gTts+5HHSfgn1TJGb6VQt9b5+MwgD8sedGQRX4E7tACxV/iRtRB9It1yeQ5wz+h0Dfg/DrxJyUvGrLIT4JG+yQUvAP8ADnDN1Poe+P8evE/SO4/TynyK6xRvI9Bi4kBtpInZ3g8KfS9c/5d8Xslx+GQGvLM4VFcN7H1FRx3Vj+kvix5NdBXdNroWT8ruQfef29aDk2sC9wzcQrdDv7OX2O9dt4/1qLzhiheX7eqB96gNy04Y79KjGZ9I2LAItoo9LxwPjzogfEei2dBPu483OFvJm+n03+XBL8mdd/hSTTE5Yg91iaFrYY3J3KlgzVvckXv9HcKZ/rnuFwBtRUKWxH9tXG5OlnftKSkpKTkQnAMSXepNBu0tI8AAAAASUVORK5CYII=>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAAAZCAYAAAChBHccAAACQklEQVR4Xu2WT0gXURDHp/8REggmiZkoKGERQuAhPIgQih6CLhJdwpMgiBQoYpeQwIOIefAi5EWsKPAaePQg4UkPHqSLKHUwPSZoafPtzfx+s+PbtaPCfuDLvvnO7Oz+dt/vvSXKOT089cZZoYN1xOryidPMeQo3PS7HN3K8YYsMw6w/ojaXy+IThb5rrGsup3SzfrB+s0ZdLgoKH8gYzRU7Vg5Y0zK+wjpkXS2mo1yi0Ou2xBckrihUBD6zvpt4lrVr4iixG/7pfLDD2jbxWwo1TcaLscjact4YHe+P+GLEa3deAhRUmjGYp/BGlBrJ6dNT7rs4Bs6bct5D8ZUJFyvwvnnTggKoR44xlqiYu8x6ZHJZ6BR55fxq8Z9IvC+xR+8tlZtULIL2WHWJimLuPauFdVdiTJ0sGinUvXA+FgP4gxKn3WSanwBPaIWSP+K6yav32ni14t0ynqeVQk2f80vF1z9/2k2m+VFQaN+E9WNN4NkVwlNPoabf+WXij0ic1T/mF9hgPZexFt4zY/VjTdJ85RyF/JDzq8R/JjEWh1ifk/r/S26asfWVry5WTmxOIZ+22uhavyCxBx72klSw8SjaQOezcsfFCrwZE2PD6jUxwE686rwBSvbTqeqB99KbFqyxczJGse6ImK+WX6wvJsZngr8gYqjBeM3iWRBPOg9P+IOJO+n4eVHwNanzDm+iPJkugOmFGqzLuBi+iyyPWcvOA/qkP1I4910yXQC5dQq7MupLkuls/uuX5uTk5OScCf4Cs6izBT6G+t8AAAAASUVORK5CYII=>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAAAZCAYAAAChBHccAAACPklEQVR4Xu2WT0hVQRTGj2YYIYJgYUQJggrhQmgXIdIqciG0EXMj0kIIIgySoF0IERHhQhdCi4ioDAW30cqlq0JciAulyILITRT2z87XnPM6c5p57y2fcH/wced859y5c2fmzX1EBbXDsDf2CxdYe6whn6hl6ikM+r5cp+R6xBYJzynkdlmTLleJeQr3rrEOu5wyxtpm/WTdcbkkKDwtbXSu2LbGzS7+buIcBynUnpT4gMTHShWBF6z3Jn7M+mziJKkBf3J+n8SvjLcjXrfxUiyz3jnvHqUnpyHhnXdeBAqOmzZYpLAiCjpF7q7xvopnVyMFamacd0Z85YGLFXgb3rSgABqXa7XofeXQLXLL+e3iX5QY2y/VV8VntNG/IugbqzOqiMEqrLJ+s+pcztNLoc8J5+MwgK8/+twgc34EZug1xS+R2g6XWLOsj6wll0txjkJfV53fIv6cxLlB5vwkKLQrUY4PFGrKzX4XhZprzm8V/7bEuefl/BJbrFFpa2GPaee4TqEG53IOvBhqbjr/hPgjEuNwSD2v4uCRfGva1lceUXz6gLNURecU8rnTRs/6lxJ74OG3leWHaWsHHaatPtRvvMvi2Q/LIdYVE4NfrDfOu0Fx/7pVPfCwwllwxj6RNor1i4j9quDcx8fG8oVCXaPx9CVPGU9XyIJ42nmY4acmHqD/70uCf5O677ASR+P0XxYo5DfliiPVDhwMslacB3Smn1E40x/G6RLIrVOYKNQ3xenyVPWmBQUFBQX7gj/PBLF2wXwiDQAAAABJRU5ErkJggg==>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADkAAAAZCAYAAACLtIazAAACdklEQVR4Xu2XTYhOYRTHD+NjNLIgUsqCxkqIhZRsUMJm5CNJZCEbIStWmlKzmmRhrXyXEkXjoyxYYTO7STbSjI0syEe+z/8+57jnOe/zPO9rlq/7q3/3nP9z7jP3vM+997lD1NC97PVGt7GV9Zu1xw90A1MpNDcsx7NynG+LDNNY37wp3GZdYC1lTWGtZI2wVtmiAodYb1k/WENuTOljPaBwjc8p/J22YMI1EuNExcZgTDxViqcU10BXooo8N1kTJr/Mem9ysIjCnLMknyc5FqpIqrF3zrd8oPzYY9YJ1iXWSTfWDsyJu8R7W0z+iXXD5OAF66vzWsBE+IU0BrcorHCKUpOPqMPbx3GO0nPCe+Xy3SYHp8UvggLoiBzbUWryIU2uSTzjqTn12sAGidfXwxUHxJ/r/IiFVE8GfWH1RxUxpSbvs45RuOiLVP947bDNWKx/XOLV9XDFLvHXOr+FHtYoxc3OiSpqSk3eYZ0xeS+F2k3GS9FJk4MSr6iHKwbE3+f8LCi2K5ui1GSK0lxKrsb6hyX229FO8Tc6P+I166DEOuFyE3tKTU73BuUbsOAll6qx5+ozua4ertgvvr48k6DgjYmtnyLX5GIK/l3nd9IkXlipGni/JJ4p+aTert9NrMVLTOzJNannbHY+PL8dHWXNMLk+Ih54dr9Fft7k4J74RbBHXZUYxbjlcFz2tyLmM+UnhW+/Pk6JhxeQgmcKnp8DK3bd5NuotSa1ash3OC8J/vvQ5wIruyAervhI4bsStzY0TuGzC9+pChrE9oE5tJHZZlx5xtruTQrnvmQ9ofy511g/5YgabC3/hP+VGhoaGhoa/lf+AOF3yrQA2gbIAAAAAElFTkSuQmCC>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAAWCAYAAABdTLWOAAAB8klEQVR4Xu2WsUpcQRSGjxrBQJCARAQrA1EMNhJI4SOYwi5iZYgWgvgGsQxIBMkDpEsIFoJlCgsJYqNNBFGw2RVBG7FQEsWEmPPvzLme+2dmrYQt9oOfnfPN3OPl7t0ZRZrcHxMsGo1RzY1mnCcagVYJN7cUP9/Hzyd+UWRec675pZmiuXqgV0VC3wNNf3m64K3mRPNHs+AnIF7EMZoYfgz2NGuu3tVsujrHsGbd1dMSes85B1Y0x67+ojmzInVjp+Q7qTbgHrMkriSse+gcau6H+kHCFYNekqsSnrDxw8154D6xJJbl/2v5Jj9SbZRuEpnxkuCmRs7XY0TCNR+cu46OKVxPLCyXmmc2GcndTM7neClh/XfyuT4l16bZidKC99Co1yTlUyxqPktYP0lzuT4pV5P+yXqfuiDn69Eu4Zqqc7k+hTvUvCE55Mbmc01S/i7suoFY40ea6lM4DI5Y0viCagNunyXxU7NFzm7qXayx/+b61/idkE/dGLym2oCzgwB0aGZd3SW3T81jbjDW9ooxhcMe9dVJe2f46ILDNmXgh8CN7Y8/J9fnajsYKs6BvxL2VOOVUH/892NfAZ5st5+M4MTAPL467AQ4SVpKK0TGNNvksHNgW8O11fj5zS9wYL/E2b4hYd2j8nSAn0yTJk2Ifw+Crhthuk+sAAAAAElFTkSuQmCC>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAAWCAYAAABdTLWOAAACB0lEQVR4Xu2VP0hcQRDGJ5qggqYQ/AMWQkgUxM7YBVGxsrH0TyEJSRFIoSDE1sYmATFVIGhjkSKFgoWNWFlaCbZ6JxITIZAmKIlGnY+ZvZube3v3LIQr7gcfu/vN3Hvz5r3dI6pyf0x6o9IYZd2wxn2gEqghKW5Jx0UdW2yS8o0k9pc172IxPrEyrBnWNMnbmiBphm3IP9Ysq43VwBphZUPwitWncxQQsPOwfuzWuHA5jkhyYwp4HxqyQT//5fwBXe8Y77d63cZLAjnDrF7WM9YTFR6w3uUtsFYo4ZNDsMPMwQZJhwMPNfbBeOfq2e4mce0N5iPrtfNsU4oIrX2rY1rC7+5KM+vQm1TmWu2UvyF0QfJaYqCrByQdeuBiaYgVA3+b9Z21pWtsohy1rH0NBCW9xinWZ9YZa9PF0vCKZCMlgXt2mvV79YqAaTtbip8kOXfpJvJferMEuRqOKf/DYGInlityjiTnhw9EeEqS3+gDyiNvkKkBkxNvuvkaFe528ILSdTzwheK5qySxfufn8i8TTJxjvmBo0Hhv1Ds1Hs69d2ZtwUaLFYkm/KfCT6eJTP4y66vOYaLtGLtCAsm5uWvW4A9JXp3xwsP0GC8QYkngrxmniiVDLh//p3idMNHZVhtU1kniWR1xUVsgGGPtOS+ATsWKBM9J4jg5MIZPsIhSF6lSpQpzC63enUaMXudiAAAAAElFTkSuQmCC>

[image13]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAAWCAYAAABdTLWOAAAB+ElEQVR4Xu2VPyhHURTHT/6UQTb/sikGLJhEUZSiWJRMZCK7nVImWWwm+ReKRfJnECOKgcEm5V9ioxDOt3vPc95xn18GZfh96tu753vOve+++959lyjN39Fjjf9GG+uD1W0T/4EMcpOb8Ncxf83XRZ4tcrlHVr/JJVHN2mHVkLtXKWuStaaLPBjzmvXGGtcJGLW+jQkIui1xtm/js0B895VOpIVcrVao3wrrSsWzrAcJQhO7N/4GfX/ydXI1Hca3NJKrnWaNsnLj6QiMlRXwokaJMVfJrbCANnJdyqv03q3yQjSwRqxpwOvXiyLEJgkNaNOAh5gxXhO5+iPjW+op9SRfKHzvyCvygeiZVSbJH9gkV19lE4Y61hy52gXWE2svVvF1b0vMy2SdeFOUpwsMqEfNgU0EwK6+MB767ps45SQFmHplk8Bqp3rNP3FD8fGT7hd5eMo+Y+IVhjqBU9aSNX/JLrnxC30sG9MSeWhcWtO0BfzL8LPXSN8kQqt06L0cH2/72BJ5rwETp4LtNMwaNB5WYkrFuOmQigHGWTae3c3yiVkiD/+oeWXiVMG1XAqYZu+F1KrqxKtQ3jG535BQTK6mV3ngnbWo4nYyE8cxJ98FVrZAJ72fJJzHQieFd/wZuVpZQRyVIZA/J7fzURc8nWIzT5MmzXc+AQ9spz4tfzTIAAAAAElFTkSuQmCC>

[image14]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAAWCAYAAABdTLWOAAABzElEQVR4Xu2Wuy9EURDGxyshQiMeiSAhCNF59BKVRiGCTqIhGpVaoxWNjkah1Wn8AQqViES3HhERoiDxFubbM2d37uzZXbsi2eL+ki9nzjfnMTl77r1LFPN/zFqj1BhnfbOmbaIUKCdX3Lq0a9I26kGKSta7NfPQzjont+4Jqz6SdWDNZVYzq4Y1Rm5Okk/WoMRYxKNjcCae12+ZZB2qfoLc/AnlAb2216hO2vje+JpHyp4LgbFTAc+ugf4qa4sCVw7JVhWDPXInHKKYIu34O/H6lGfHRPCLLEibj0KLXGTNGO+N3Br6buZcs4XShUIvrO7IiCiFFhkidLroH7CuWfvSx0OUooJ1LAmv0BMI/lrkJrn5vcaH16H6K+JlAFOfbIi/FNlAbu6ITWQhtc8Fa86YAyq2FFtkGbl5bTYhVFmD1D4IrqxpYk2xRWJOrerPs7ok3iaXH06nk6T2+QiYnSq25CqymrVkTeaV3JdKc6riHdYXudP21JHaZ4O1KzFMHDvaHj/A8EzZi4QP9SvvUvlWHnya8VbRJMjsg38/eHnDxMk26aTwxLohdzUgvCoeKP2TAXzqjlQf2MJCRYIh8W6l9VcwAzsxJibG8APTs5yJks4POwAAAABJRU5ErkJggg==>

[image15]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAAAZCAYAAAChBHccAAACKklEQVR4Xu2WP0hXURTHj4qQoOFiGg6BUEO4mDqIQgROLm6KU0FL0NLUJqjQJIiz1CKog4MutaQgios2KIiOFSFYOBmUlKLn673n9zv3eK/vLYLC+8CXd8/3nHvfff/ufUQFN4cha9wW+lhnrEGbuMlUkpv0hD++88cGXeQZZh2x/rBemlyKNtYS6wm5c7WwJlmLuoj5x3rDamTVsHpZ33RBjBNWu29j0oJug13WZxXvsNZVnAKTwFhav4IKh62BngUVEWITPjT+XRML8OqtaXjK+sh6zxpj1YbpEhhrhFxd7lcXnZpVGyyQeyLClspp4OFkV9HDGrVmhNj4mcgjeuWPMaTGkvI13XSNk2+i8iSgv6yHQUV6kilf08WaIVc3R+5jXw0qHMjjm9pnffIxPt5MqljbFF4E3nMhNcmUr8Eq89146LMW8R6o+K33coNi/SS0Hxso5WdxQPn6oWbZmhrclRe+LQO2qrb4sZOl/CxWyPXTr0W1aguZ4yP5Q7W1L/w2sQBvz5qG2AS+eO+Ojz/4uLNU4YD333gBOiknwS6oTzhgYgGebHAAk3mtYoCaeeNhN9XjTbNOWRXKqyNXM6W8S2CrnvVtFOPx4fioVFHOYTkVxr2nkbv8WHnYI7BcCvfJ1TxXHn4bsMppvtLl8aPgbxKbEorxJO6F6Qvwv4H8BrmV6ZjCOwX6WZvGA/i1QF+54/hlsHSQy/30R3mVc5PrSgsKCgoKbgXnokCqum8g+i8AAAAASUVORK5CYII=>

[image16]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAAAZCAYAAAChBHccAAACDElEQVR4Xu2WSytFURTHV14ZKeVVZooBZr6AUMqAFMlEkkQMjPgEpjLxBSTlzUAeY0YyMGAkkkdIEQMDxPq39753nXXP684unV/923v919rnrnv2OXdfooTcoV8bf4UO1g+rTydymTwyTc/accaO5bLIckAm98IaUrk44AYta1OAG/dG5jMGVM6XL1aTnWORQ85dXGjneLwQP6XTgUyx3snUQyvedIpzMnWOY9ahiH3xa/hZ+busLRGDHTI1ncoPI6j5XjK5UuXDq1CeBxRUiznYJLMjDsyR6xFeg/UehRdFUPNn5L1ZDnh72pS47Ry1ox/4cgvKayZTf6L8MIKadz1ogvwUVZQugj5YtZ4Kf/bJ1DfqRAhBzV+Rf5ORzYN81il5v0SJp8IL6lGDlyobsGZVm0wLmVyZ8ORNjQUK4yzC7mTzuDhwzXVtWi5YryLGZ0T1QdesQTt3hXgUghbh5fLb+jjgmhvaFEyw7lmLNkb9dzqdCQpuxFz6mjUyh5jErY0Drql/csNA/Yg2JZ9i7hquEXMHDpsx5VWy5kVczBoXsQbX3NamBblpEU9aL5Q51pKdoxinKMa6VAVRq/X81C7qnFcvPEcRmdyRTjAFZHLDwkPcLeJAcNy7gwg7oU813bAU/hs5uijzFwjPMU7sOzKP2C3rgcwLKcE6XO/Sjm3edDRYlJCQkJDwP/gF1l+k9bvjRsAAAAAASUVORK5CYII=>

[image17]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAAAZCAYAAAChBHccAAACHklEQVR4Xu2Wz0tVQRTHj2WQBGJEEmgtCg2jTQRC+B8IIiJpUYHQpoi27lpKRBBt2rl26x/gKiEjbZFoufP1Y2GiKwMrEup8mzn5vefO3NdS4X7gyz3nO+eeN29m3r1PpObgcNMbh4VB1W/VuB84yByRMOln8ToVr6e5KPJItaPaVd11Y1WcU32U0HdF1V4YLXJL9VNC7QM3VmJPdTXGuMHgGHxQzVG+qnpFeY5R1WvKGxJ6D5NnfFW9oRwLdY3yEqkJbzsfK+W/DIDX4U0Haq4nPN9v3nkjMZ8krwQKuigGsxJ2xHhHYwy8aW86UhPdil4fecjvUA6uuLyENb8XrylSEwA5n7mvuuE8O9N29h/H/JSqRTUU/aackf1JQN9VPYWK/CRzfjP8fZsxf6i6rTqr+qFaoJosR1XLUvwS/ETwH2bk/CpeSLjnInnW5yV52AF4+MH/FyjmnWA/NcmcnwPHAvX9zrc+vRk/yyfVRIyt8DLF5qea5PwUtpI4Ep6GpPs07Y/BLxSzb3xzuQFvzZsZUHuCcrzkLsT4ieT7p/x//KLYCs9TDMZcbsCzFxw4Lum3In58rc57T7HtSjd5AN668wo8V83EGMXH4jV1/vA4NZ5Gj7GVukTeZ/K9GOzgBuUDEmrwMKkE/ybxUkIxdqKzOPyXNgnjixKeTFhNrBiDV/6S8/yEc5MHbyX4+FuA68nicDWphjU1NTU1h5M/AiOzviYYoT4AAAAASUVORK5CYII=>

[image18]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAAWCAYAAABdTLWOAAACE0lEQVR4Xu2WPUhcQRDHR0WICBIQRdDGbyJaiCAoWKVLYxMiVgpaCGplGzttFEIKO+3EYGcpYiEp0iSNAYmgxZ2IVULwAz9AMZn/7czdvMnbswpY3A/+7Mx/dvf27XvsHlGJ/8eoN54bb1h/WCO+8Bwop7C4D9IuSltnOwnzrEvWDWvC1YqBuTIU5j1idSTLeTDnI4V+q7bwwOqTGEXFxuAHa9fkB6wvJo/Ry9oz+SSFuWeNBxZYMybXN5sjbWG/nF/jcgXeS2867ij0qzIecj+fz8FPDVBsNDHYorDDyr6pWeCtedOxSf+O9YvEgyIvMx74rYEOmJI2DT+pEvOLMUhhzJLzda7XkldLnqPBdIBuWe1aFGKLifkx+in0/+wLzBwV5juTNkEF67sUVPgOldhiYn4ay6x1Cv3HXE3ZoOQa3ibLARTszlo/bTExvxiVFMZknX9M4UHADrm5T1jjEqvZbWL10xYT859Cx3VKjmPpvFDO0URmbgSnJra+cuVyBd6hNx3XrK/Ow8mBse8lR5x2OQxpcG9MXUiLicE7lyvw9CIAL1jTJq+l9N1W75XkF6yVQjlPmwYfWZ8kxkD9ZvzVBQ/HlILvJ/bjXc5rNrleDBnjtYqHh7TgLeTBvx99BdjZelsUcGOgjleHkwA3iT98h1nfnIeTA8caxmal3bYdhAEq/D4Wh7gn0UPwO1OiRAnHX/ptrknEZpGwAAAAAElFTkSuQmCC>

[image19]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADkAAAAZCAYAAACLtIazAAACoElEQVR4Xu2XS8hNURTHF/IceIU8QikGUsgEeZSJklIKyUSZkJIUUkw8MiBJMiETj5JkjpmUmCCvUopPRvIs5JFv/+9a/++uvc7Z906MbudX/85e/7XOPmd/e5+97yfS0LtsjkavsSbpX9KmmOgFBosO7pRdj9l1oi8yDiV9TfqetC3kunFdtN/nSaNCjlwRrfmRdDTkyPik96J1r5PG5Ol6/iQtsjZuJL4N8HK3Xfw06Z6LSwwV7WuGxUMsnjJQocCbYO35Fv9tp1sMEx0gGSRat9B5tdQN7EPwR4eYwBsbzcDdpHfBOyl5f/uTHomuKrJXtAYrjHx2bTJPqn+MCuhommuDm6IzTPACpUFeiGYANeeCt9R8ct/is84D8OIk7HAx4Kx3hB1tt2sd8WGk5BMuzYPBn2n+eovxjd6QfCaHS7X/TxbfcR5md7mLa5ks7c4gfPSzs4rqw0jJJwtE83uCj00NPpZpiQOiNTudxz8ahQGudfmO4ObHkneA75CUBlPyySrR/K7gjzP/fPA9yH+MZmKq5O/5LE93Bzf5mfV+3WBKPpkjmt8dfOyi8I8En7wS3fwiq0VXGlgp7edjgjryJmmrtfnC2LH+xyC5xWPpeaabvyX4AGdlaXbqnvVW6v0MFPS5tvfJtxATeC+iGUBNaXeNZyWW9a3g8bkbXDsCf3E0Pb9dm53Mcm2wMcQEHn9IgBGSbxQAZ9iT4O2Tan8rki4FD3BWceDHe0jJH+B00lVro5i/UPA9eeDhmCEnzPMghuY6b5l5HsRnXIxzmvdGHXd1iA+7GCDGOd4V/PeBwx+dYGYn5ekWI0XzD0Q/9J+i35xnXdLD4AHO3LWkX0kX83Rro4mDo5a4OvDF/Jd2vZynu4ObGhoaGhoaGkT6AZ+C2tDkVVmNAAAAAElFTkSuQmCC>

[image20]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAAAZCAYAAAChBHccAAAB80lEQVR4Xu2WzytFQRTHDyIWZONHWSjFQnb4A5SVjR3ZKRvFwspO2VgpWYuNhUJ+bWxkacOGEkuEoqwo5Eecr5njnXvenffuKwuv7qe+zcz3nDfv3Dtz516ilP/DkDWKhT7WF2vQBv4zpeSKnvPtjG/rdJJnivXIemaNmFgScINWrel5Y02wGlhVrF7WpU6I44PV6fsoWtB9cMbaU+NT1oEah5hkPZGbD1qLhn+RuFZPJCOGuIIfjF9jxgK8WmvmIF/x06xFKmDr4kdNqg+2yK2IcKxiGnj4s6TkK75gZIlGfRuH5FhCfog/L76RMkVAL6zWSEa4yJAfIl/xeKZuWbt+jIc3L2WsE4peBPa5ECoy5IdA7ro1PYg1qzEe9ELm/knWK6H9uIlCfgjkblgzB8jft6bmijXs+1JIh+qLH1dkyA+B3E1resqtQQnmR/Ba9bUvyDltgXduzRwgf9uazBK5WLfx4b0bL4IOSoEtqg8GzFiAJy84UMkaU2ML8nesySyzPlklyqsml7+gvCzmWSu+j2QsH9q234xMDMepMOs9DcZQu/FBBblY3FsZnyg45TQXlD1/LPiaxEtJlqk+Gv4B3xuIH5I7mV4peqdAP+vIeOPk3tg4ArE9b1h3lF1sF7n5730rWzkxia40JSUlJaUo+AYzyKJXk+llSgAAAABJRU5ErkJggg==>

[image21]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAAWCAYAAABdTLWOAAACAUlEQVR4Xu2WzyumURTHj19FJCmD7JRRkxX+BRuzsJga2YmSYjVlyU6pKfkDLCdZKEsLZaPZkBo1UTZIiGRBIaPhfN97zjPnOe99Xqupd/F86ttzz/ece1z3fd4DUc7/Y8Qb5cYg65U17BPlQCWFwy3Kc16eLbZImGXdsR5Y4y73Hvg5exR6n7Gq0+kCY6xL1gtrwSZg9MkaDRS7BgesTRP/Zv00cSl6KfRrlfiLxJY11oWJf7BuNYgd7Mb5jS5W4DV501FBoa7feIh9P8T+dpMaLDqcuU7hhpVfJmeBt+xNxwkV78VHX2PiJSquAalDQpPWdMR+c5DlW2zNJ1abySnPFO+TeNikjaBHVpcmhazDZPkW5E9Z16xm1rR49a4m1iflVbH2xVThPVRKNYn5SjvFa46dF6sBMa9g2pu1fmxDlq/gtmI1c+J1SxyrAYmHj2LUmT1mrX5Wk5hvQR5z0fJN/BmJ8SWN9Uk828QfTLl3sQLv0JsO1Fw5D4eDPyEx5m9W/wJ/ImanWYOvLlbg6R8CUMuaMjHAgPZ7deRghgJ9xTyJhw0rxsT8wvOjFpgcxpTyXTwLYgijRtH3Et9sBfGWicFf1qqJP5Prj/9+9L3AzX6wSaGOQn6HwiR4on83oQyxdp0HBijsPZfnRjqdgHl5xNqmUNeQTgf8zeTk5DjeAOnAsMBo5QySAAAAAElFTkSuQmCC>

[image22]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAWCAYAAACCAs+RAAACQklEQVR4Xu2Wz0tVURDHp8RKxDLQEESMqBbhrkWC/QVCtCvaCS0MDdq1C4JqFUQguGodlPijNi2CdkEURIbYOlIQcqWgUWnNt5m5zhvPPN6yB+8DX+6Z78w798x9995ziVr8/1yLRjMyyvrDuhoTzcJBkgYe6fGBHnt9kXKHtcHaYl0PuUbAxXoWTccUybl3WA9DzrjIWiepe0ey/n/8Zp3XMZKGH4Nl1msXL7HeujjjNmuTZD7oeW26Ypt10sVW70Gj0y7GBa1qSou3jo2jITbgdUezDlkjh0hyaNiYV2/ceYgvuNi8atAfTEyCf8r45HIeeE+iWYesEYDcexe/Uu+Sxp0ax3XUNALd8GagNAHI/Ix6jURKc99jjQSvqunTwIR79YwlldKkIPMzGm3kJUntsZgoUHP+NtaimiY8F0a24MzPQO1MNB3DJA/0F9ZHkmenHp8pOT9M/w95v/SDzM9A7Ww0E96Q1PfEhIKHHvlqm/jKGtOxLWrIjc0vLTjzM1A7F80EbAnZ/MdJ/MPehPHNjb1v2D4QgYfboFFQvxBNZoIk1xX8UiO2ge/jlxtbwSk3BldCbMCzzRQcYU26OIL6F9GkvQXfdd5p53t2Q1zxmPVUx/hRux7PVhV7ObyiDXxCxJPYic8FH9imV/oauMVaCx6+HFA/6Lyf6kVV4KsXGyBM/EMnfFLpIMlj08Ib7gfrQE0F0WXWh+DdJPlSWCW5hVdIFo3XvOc+yfzf9YgrP+Dy2LRjA/saMYpmixYtmpu/o0XFweQf+lIAAAAASUVORK5CYII=>

[image23]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACYAAAAZCAYAAABdEVzWAAAB7UlEQVR4Xu2VyysHURTHTxJKkZCUCCWSR8JaSRaSbG2s/AUWihUrCwsWNixslL0spFjYSLHwSiTlkZTHEnmfb/fcn/M7rl9joSzmU99mvt97ZubO3McQxfwfum0QoNEGf0kt60mOr6zm5OYEx6xeG4bIYK2zPlgrps0ywnoTdZo2XF8p53msR3J1g6wO1qzUXEtNSprIFeeKbxEf4oXczUEm652V9dX87Trti+WILxoJXLwTyPZMdse6UX6KXF2r+ALxGuuHKeIQFpK7eMbk25J7ysWXqgzUG287on06RRxC0E/u4kmTr0nu2VAe8xHzJcQzq0/O21kDpi0yZRT+YmeS54vHObTAaiO36uAxnBbk86xblY2xepSPBG60G8ggLATtRxMVRBWSlagsBL7wlfI1rAdyo5ISfHI8ADcAQ+QmPrI0yXzHLMj0Q0NgP/Pk0Nd9slmHqi1IEbn964BVxzql5I6k6lgo94yzupQ/Zy0qf6LOI2EfuGm8x9ZpsL9dmgy108rbRZdE6Obwer+plsyCbM6GAnZ8i+1YaPEkQDEmo2eLda+8BzXLyuPXFOosmCA3dy348kvKpxzKBnIPuJAj/pk/4WuwJ+F35BeHBkP40wPxG/Mvg8m/r9r+nCMbGKrIvdiqbYiJiYn5JZ9rJ4dDOw4P7gAAAABJRU5ErkJggg==>

## The Real Problem: Claude Code CLI Timeouts

Your debug sessions from this morning (27 May 2026, ~09:42–09:53) show the exact failure mode clearly:

> _"All calls timeout. The proxy accepts the TCP connection and returns HTTP 200, but never writes data to the SSE stream."_

The root cause is your `smart-mcp-proxy` running in `CALL_TOOL` mode, which only exposes `retrieve_tools` and `call_tool`. When Claude Code CLI connects, it sends a `tools/list` request first—and the proxy has no handler for `tools/list`, so the SSE stream opens but hangs indefinitely. The proxy is technically working; the transport handshake is the mismatch. This is a proxy-mode problem, not a model problem.

Immediate fix for the timeout:

```bash
# Check current mode
cat ~/.config/mcpproxy/mcp_proxy.json | grep mode

# Switch proxy to full MCP mode (supports tools/list)
# Edit mcp_proxy.json and set "mode": "mcp" instead of "CALL_TOOL"
# Then restart:
pkill -f smart-mcp-proxy && ~/scripts/start-mcpproxy.sh
```

If you can't change the proxy mode, bypass it and point Claude Code directly at Hermes's MCP endpoint (`hermes mcp serve`) instead.

---

## Is OpenRouter Affordable for the Tiered Model Vision?

Yes—and you already have the right free model defaulting. Your current config (confirmed from memory today at 09:00) shows:

```
Model: {'default': 'openrouter/owl-alpha', 'provider': 'openrouter', ...}
```

`openrouter/owl-alpha` is free—$0/token—and is [explicitly rated as top-tier for agentic workloads, tool use, and long-context tasks on OpenRouter](https://openrouter.ai). Your instinct about a tiered cost structure is directly achievable.

---

## Optimal Tiered Config for Hermes via OpenRouter

### The Model Ladder

| Tier | Role in Hermes | Model | Cost |
|---|---|---|---|
| Free (planning / triage) | `model.default`, aux slots: `title_generation`, `triage_specifier`, `kanban_decomposer`, `profile_describer`, `curator` | `openrouter/owl-alpha` | $0/token |
| Free (routing fallback) | `openrouter/free` router | `openrouter/free` | $0/token |
| Cheap capable (drafts, code) | Complex task execution | `deepseek/deepseek-v4-flash` | $0.112/$0.224 per 1M |
| Mid-tier (coding / reasoning) | Hard problems | `qwen/qwen3.5-plus-20260420` | ~$2.50/M in / $7.50/M out |
| Frontier (critical / public) | `delegate_task` to Claude Code | `anthropic/claude-sonnet-4-6` | ~$3/$15 per 1M |

The point of OpenRouter here: you get one API key, one `base_url`, and can hot-swap any of these models in `private_config.yaml` without changing your Hermes install.

### Cost Estimate for Your Typical Usage

From your OpenRouter analytics (captured 19 May), your Hermes key showed `$0.000` spend—you're currently on all-free models. The tiered approach above means:

- Daily light use (planning, triage, short coding): stays near $0—owl-alpha covers the bulk
- Medium sessions with DeepSeek V4 Flash for code execution: ~$0.01–0.05/session (it's 284B MoE but very cheap)
- Occasional Qwen3.5-plus for complex reasoning: ~$0.10–0.30 per long session
- Frontier delegation (Claude Sonnet) used sparingly: ~$0.05–0.20 per `delegate_task` call

Realistic monthly estimate for your usage pattern: $2–10/month total, dominated by the handful of sessions where you delegate to Sonnet. Essentially free for daily personal use.

---

## Config Patch to Implement This

```yaml
# ~/.hermes/config.yaml (via chezmoi: private_dot_hermes/private_config.yaml)

model:
  context_length: 128000
  default: openrouter/owl-alpha    # free — planning, triage, everyday tasks
  provider: openrouter

providers:
  openrouter:
    api: https://openrouter.ai/api/v1
    default_model: openrouter/owl-alpha

auxiliary:
  title_generation:
    provider: openrouter
    model: openrouter/owl-alpha     # free — was empty/auto
  triage_specifier:
    provider: openrouter
    model: openrouter/owl-alpha     # free
  kanban_decomposer:
    provider: openrouter
    model: openrouter/owl-alpha     # free
  profile_describer:
    provider: openrouter
    model: openrouter/owl-alpha     # free
  curator:
    provider: openrouter
    model: openrouter/owl-alpha     # free
  vision:
    provider: openrouter
    model: qwen/qwen2.5-vl-3b-instruct:free   # free multimodal
  skills_hub:
    provider: openrouter
    model: deepseek/deepseek-v4-flash  # cheap capable ($0.11/M in)
```

For the `delegate_task` to Claude Code (your Tier 1A), that path bypasses OpenRouter entirely—it's still `claude --print "<context>"` hitting Anthropic directly. That part doesn't need to change.

---

## The `/goal` Prompt to Apply This in Hermes

```
/goal Optimise model routing: pin all auxiliary slots to openrouter/owl-alpha (free), 
set vision to qwen/qwen2.5-vl-3b-instruct:free, set skills_hub to 
deepseek/deepseek-v4-flash. Apply via chezmoi. Verify with hermes config show 
and hermes doctor. Do NOT change the delegate_task or claude-code skill config.
```

---

## Open Issues to Address Separately

- `smart-mcp-proxy` SSE hang—switch proxy mode from `CALL_TOOL` to full MCP, or point Claude Code CLI directly at `hermes mcp serve` on its native port
- Aux slot toolset disabling (from your 26 May audit)—7 toolsets flagged safe to disable; still parked pending this diagnostic; can be done in the same `/goal` pass
- `goal_judge.model` trap—your 23 May config audit flagged this was previously set to `google/gemini-3-flash` after a Kanban crash; confirm it's not still pointing at a paid model outside OpenRouter
