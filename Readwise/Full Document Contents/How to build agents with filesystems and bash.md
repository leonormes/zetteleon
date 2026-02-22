# How to build agents with filesystems and bash

![rw-book-cover](https://assets.vercel.com/image/upload/contentful/image/e5382hct74si/htPohxP7MYbZKG3LP6iK7/65e0dfe1c2ed26aa4a28bb9e5db1cc86/slack-imgs.png)

## Metadata
- Author: [[Ashka Stephen, Software Engineer]]
- Full Title: How to build agents with filesystems and bash
- Category: #articles
- Summary: Building agents using filesystems and bash lets models use familiar code tools to find exact information efficiently. This approach improves quality, reduces costs, and keeps data organized in natural folder structures. It also makes agents easier to debug, secure, and maintain without complex custom code.
- URL: https://share.google/8rGFgIYuvHD6DcqbQ

## Full Document
The best agent architecture is already sitting in your terminal

Many of us have built complex tooling to feed our agents the right information. It's brittle because we're guessing what the model needs instead of letting it find what it needs. We've found a simpler approach. We replaced most of the custom tooling in our internal agents with a filesystem tool and a bash tool. Our sales call summarization agent went from ~$1.00 to ~$0.25 per call on Claude Opus 4.5, and the output quality improved. [We used the same approach for d0](https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools), our text-to-SQL agent.

The idea behind this is that LLMs have been trained on massive amounts of code. They've spent countless hours navigating directories, grepping through files, and managing state across complex codebases. If agents excel at filesystem operations for code, they'll excel at filesystem operations for anything. Agents already understand filesystems.

Customer support tickets, sales call transcripts, CRM data, conversation history. Structure it as files, give the agent bash, and the model brings the same capabilities it uses for code navigation.

The agent runs in a sandbox with your data structured as files. When it needs context, it explores the filesystem using Unix commands, pulls in what's relevant, and sends that to the LLM.

The agent and its tool execution run on separate compute. You trust the agent's reasoning, but the sandbox isolates what it can actually do.

The typical approach to agent context is either stuffing everything into the prompt or using vector search. Prompt stuffing hits token limits. Vector search works for semantic similarity but returns imprecise results when you need a specific value from structured data.

Filesystems offer a different tradeoff.

**Structure matches your domain.** Customer records, ticket history, CRM data. These have natural hierarchies that map directly to directories. You're not flattening relationships into embeddings.

**Retrieval is precise.** `grep -r "pricing objection" transcripts/` returns exact matches. When you need one specific value, you get that value.

**Context stays minimal.** The agent loads files on demand. A large transcript doesn't go into the prompt upfront. The agent reads the metadata, greps for relevant sections, then pulls only what it needs.

Let's look at some concrete examples of how different domains map to filesystem structures.

**Example 1: Customer support system**

Instead of throwing raw JSON into your agent, structure it:

When a customer asks "What was the resolution to my issue?", the agent can `ls` the tickets directory, `grep` for "resolved", and read only the relevant file.

**Example 2: Document analysis system**

Raw inputs in one place, processed outputs in structured directories. The agent can reference previous analysis without reprocessing.

We built a [sales call summary template](https://vercel.com/templates/ai/call-summary-agent) using this architecture. The agent analyzes sales call transcripts and generates structured summaries with objections, action items, and insights.

The agent sees this file structure:

The agent explores this like a codebase:

The intuition is that the agent treats the transcript like a codebase. It searches for patterns, reads sections, and builds context just like it would debug code. No custom retrieval logic. The agent decides what context it needs using tools it already knows how to use. It handles edge cases we never anticipated because it's working with the raw information, not parameters we defined.

We'll have another post diving deeper into the sales call summary agent.

**Native model capabilities.** grep, cat, find, awk. These aren't new skills we're teaching. LLMs have seen these tools billions of times during training. They're native operations, not bolted on behaviors.

**Future-proof architecture.** As models get better at coding, your agent gets better. Every improvement in code understanding translates directly. You're leveraging the training distribution instead of fighting against it.

**Debuggability.** When the agent fails, you see exactly what files it read and what commands it ran. The execution path is visible. No black box.

**Security through isolation.** The sandbox lets the agent explore files without access to production systems. You trust the reasoning, not the execution environment.

**Less code to maintain.** Instead of building retrieval pipelines for each data type, you write files to a directory structure. The agent handles the rest.

Every agent needs filesystem and bash. If you're building an agent, resist the urge to create custom tools. Instead, ask: can I represent this as files?

We recently open-sourced [bash-tool](https://vercel.com/changelog/introducing-bash-tool-for-filesystem-based-context-retrieval), a dedicated tool that powers this pattern.

The future of agents might be surprisingly simple. Maybe the best architecture is almost no architecture at all. Just filesystems and bash.
