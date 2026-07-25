---
title: llm-codebase-context
type: note
permalink: llmeon/00-inbox/llm-codebase-context
---

## Direct Answer

The industry has converged on a layered stack of techniques — repo maps/AST indexing, semantic RAG over embeddings, LSP-based symbol tools, and standardized "context files" like AGENTS.md/CLAUDE.md — to give LLMs top-down codebase understanding despite finite context windows, plus MCP-based memory servers and portable markdown/graph stores to carry that context across sessions and models [^1][^2][^3].

## Why Top-Down Understanding Is Hard for LLMs

Context windows are a token *budget*, not a solved problem — even 1M-token models like Gemini 3.0 or GPT-5 suffer from "lost in the middle" degradation and high latency/cost when you dump an entire repo in [^4]. This means tools can't just paste in all the code; they need to compress and prioritize what the model sees, which is exactly what the tools below do [^4].

## Repo Maps and Static Analysis

Aider pioneered the "repo map" pattern: it parses the whole repository with `ctags`/tree-sitter to extract every class, function, and signature, then builds a dependency graph and runs PageRank to rank which symbols matter most, fitting the highest-value symbols into a small token budget (default ~1k tokens) [^1][^5]. This gives the LLM a skeleton view of the entire codebase — file structure, signatures, call relationships — without loading full file bodies, and the LLM can then ask to "expand" specific files into full context when needed [^1][^6]. Community forks have improved on this by resolving actual import graphs (following what a target file imports) rather than relying purely on citation-frequency heuristics, since pure PageRank can over-weight generic utility functions in large monorepos [^7]. Lightweight standalone tools like `llmcat` and `RepoMapper` extract this same "outline" pattern for use in any agent or for pasting into ChatGPT/Claude directly [^8][^9].

**Pattern for you:** run something like `aider --show-repo-map` or `llmcat --outline .` before a big analysis session to get a compact structural primer, then paste that primer plus your specific question into whichever model you're using.

## Semantic RAG Over Code

Retrieval-Augmented Generation treats the codebase as a searchable knowledge base rather than a text blob: code is chunked (ideally by tree-sitter into function/class-level units rather than fixed-length text splits), embedded with code-aware models (OpenAI `text-embedding-3-large`, Voyage `voyage-code-2`), stored in a vector database (Pinecone, Chroma, Qdrant), and retrieved by semantic similarity at query time [^2]. This is what powers Cursor's codebase indexing and GitHub Copilot's workspace indexing under the hood [^2]. The current best-practice pattern industry-wide is "search then reason" — a hybrid two-step flow: an agent semantically searches the index to find the 5-10 actually-relevant files, then loads only those full files into the high-reasoning model's context window, combining retrieval speed with full-file accuracy [^4]. On top of retrieval, teams also apply "contextual pruning" — skeletonizing untouched functions down to signatures, stripping unused imports, and substituting dependency graphs for raw file dumps to squeeze more useful signal into the same token budget [^4].

## Graph-Based / LSP Semantic Tools (More Precise Than Embeddings)

A newer and increasingly favored alternative to vector RAG is symbol-level graph navigation via the Language Server Protocol. Serena, an open MCP server, gives agents IDE-grade tools — `find_symbol`, `find_referencing_symbols`, `replace_symbol_body` — across 30+ languages, letting the model trace a function call across five files precisely instead of relying on fuzzy vector similarity [^10][^11]. Because it indexes the AST/call graph exactly rather than approximating with embeddings, it eliminates a class of RAG hallucination risk and is notably more token-efficient, since only the strictly necessary symbol is fetched, not a full surrounding chunk [^12]. Sourcegraph's Cody Context Engine takes a similar structural approach at enterprise scale: it pre-indexes the entire repo into a persistent semantic graph (structural indexing → embeddings → call/type/test dependency graph) that updates incrementally on every commit, so Cody queries the graph rather than re-scanning the repo per session [^13][^14]. Aider originally used the same non-vector idea — AST/call-graph ranking rather than embeddings — and this contributed to its high scores on SWE-bench without doing any code RAG at all [^15].

| Approach | Mechanism | Strength | Best for |
|---|---|---|---|
| Repo map (Aider) | AST + PageRank on symbols | Compact, cheap, no infra | Quick top-down orientation |
| Vector RAG | Embeddings + vector DB | Scales to huge repos, semantic queries | "Where is X logic?" discovery |
| LSP/graph (Serena, Cody) | Language server / dependency graph | Precise, low hallucination, token-efficient | Refactors, tracing call chains |
| Long-context stuffing | Raw file dump into 1M-token window | Simple, no tooling | Small-to-medium repos only |

## Standardized "Context Files": AGENTS.md / CLAUDE.md

For persistent, human-curated project context (not just structural maps), the ecosystem has rallied around a generic markdown convention: `AGENTS.md` (adopted by OpenAI Codex, AMP, and increasingly others) alongside tool-specific variants like `CLAUDE.md` (Claude Code), `GEMINI.md` (Gemini CLI), and rule directories like `.cursor/rules` or `.clinerules` [^3]. These files typically capture six things: tech stack and architecture, coding conventions, build/test commands, directory layout, "do not touch" boundaries, and known gotchas — the industry standard practice (per GitHub's analysis of 2,500+ repos) is to keep them concise and evolve them from real friction points rather than write them upfront as theory [^16]. Since your use case is multiple LLM assistants, the strongest cross-model pattern is:

- Write a single canonical `AGENTS.md` at repo root with all project context.
- Point every tool-specific file at it via reference or symlink: `CLAUDE.md` containing `@AGENTS.md`, `GEMINI.md` containing the same reference, or literal symlinks (`ln -s AGENTS.md CLAUDE.md`) [^17][^3].
- Use the `@file` include syntax where supported (Claude Code) rather than symlinks if you need the content to survive context compaction — several practitioners report symlinked files get dropped after Claude's auto-compact, while `@AGENTS.md` reference syntax survives it [^17].
- Add nested `AGENTS.md` files in subdirectories for module-specific context, since agents check the nearest one in the directory tree first, keeping the root file lean [^17].

This solves cross-model sharing directly: since Codex, Claude Code, Cursor, Cline, and Gemini CLI all auto-load some variant of this file, one well-maintained root document becomes the shared "top-down understanding" primer for every assistant you run [^3][^18].

## Cross-Session Persistent Memory (MCP Servers)

For memory that needs to persist beyond a single markdown file — decisions made, bugs fixed, architectural rationale — the Model Context Protocol (MCP) has become the standard transport for pluggable memory servers that any MCP-compatible client (Claude Code, Cursor, Continue, OpenCode) can query [^19]. Notable patterns:

- **Local semantic memory** — servers like the "Memory" MCP server run fully on your hardware using Ollama embeddings plus Qdrant vector search, so memory, embeddings, and search never leave your machine [^19].
- **Lightweight SQLite memory** — Apex Memory stores architectural decisions and code patterns in a local SQLite DB with full-text search and optional cloud sync, so multiple tools/sessions on different machines can share the same memory store [^20].
- **Knowledge-graph memory** — `mcp-memory-graph` goes beyond flat vector search by adding authority weighting and conflict detection between memories, so when two sessions leave contradictory notes, higher-priority/more-recent notes win rather than confusing the retrieval [^21].
- **Shared team memory** — tools like "Memory Notes" (built on fast-mcp) explicitly support a shared workspace concept: your agent leaves a note today, a teammate's agent (or a different model) sees it tomorrow and avoids repeating the mistake [^22].

**Practical setup for your stack:** run one MCP memory server (Serena for symbol navigation + a lightweight SQLite/graph memory server for decisions) and register it identically in the config files for each assistant (Claude Code's `~/.claude.json`, Cursor's MCP settings, etc.), so all your LLMs read/write the same underlying store [^19][^20].

## How Claude Code Itself Manages This Internally

It's worth understanding the internal reference architecture, since it illustrates the state-of-the-art pattern combination. Claude Code assembles context from nine ordered sources (CLAUDE.md hierarchy, auto-memory, conversation history, tool pool, etc.) and runs five sequential "compaction shapers" before every model call — budget reduction, snip, microcompact, context collapse, and full auto-compact as a last resort — trading off cost against losing detail [^23][^24]. Notably, its memory system is deliberately file-based markdown rather than a vector database: retrieval is done by an LLM scanning memory-file headers and picking up to five relevant files, prioritizing full inspectability and version-control-ability over embedding-based fuzziness [^23]. Subagent delegation is the other key mechanism: a subagent explores a large chunk of code, but only a compact summary — not its full verbose transcript — is returned to the parent's context, protecting the main session from exploratory noise [^23]. This is a useful pattern to borrow manually even outside Claude Code: dispatch a "scout" pass (repo map + targeted file reads) to summarize a subsystem, then bring only that summary into your main working session.

## Recommended Combined Workflow for Your Use Case

Given you run multiple LLM coding assistants and want top-down understanding plus cross-session/cross-model continuity, a practical stack is:

1. Maintain one root `AGENTS.md` (plus nested per-module ones) as the canonical, version-controlled context primer, referenced by `CLAUDE.md`/`GEMINI.md` via `@AGENTS.md` includes [^17][^3].
2. Run Serena (or Aider's repo map) as a shared MCP/CLI tool so any assistant can request symbol-level navigation instead of guessing from raw text [^10][^11].
3. Stand up one local MCP memory server (SQLite or graph-based) that every assistant is configured to use identically, so debugging notes and architectural decisions persist across sessions and are visible to whichever model you switch to next [^20][^21].
4. For very large repos, layer in a proper RAG index (Sourcegraph Cody-style or a custom tree-sitter + vector DB pipeline) so discovery queries ("where is the billing logic?") don't require you to manually locate files before the LLM can reason about them [^13][^2].

Given your existing Azure/Terraform/ArgoCD/Kubernetes stack and heavy CLI/automation habits, this maps cleanly onto infra you already run: Serena and a lightweight SQLite MCP memory server can live in a container alongside your other tooling, and `AGENTS.md` fits naturally into your existing GitOps repos as version-controlled config.

---

## References

1. [Repository map](https://aider.chat/docs/repomap.html) - Aider uses a map of your git repository to provide code context to LLMs.

2. [Aider .aiderignore — Reducing Repo Map Noise and Token Cost in ...](https://www.iamraghuveer.com/posts/aider-aiderignore/) - Before Aider can answer questions or make edits, it builds a “repo map” — a compressed representatio...

3. [AGENTS.md becomes the convention - P Note](https://pnote.eu/notes/agents-md/) - Context files were popularized by Anthropic through their agentic coding assistant, Claude Code. Whe...

4. [GitHub - pdavis68/RepoMapper: A tool to produce a map of a codebase within a git repository. Based entirely on the "Repo Map" functionality in Aider.chat](https://github.com/pdavis68/RepoMapper) - A tool to produce a map of a codebase within a git repository. Based entirely on the "Repo Map" func...

5. [Improving GPT-4's codebase understanding with ctags](https://aider.chat/docs/ctags.html) - Using ctags to build a “repository map” to increase GPT-4’s ability to understand a large code base.

6. [Repository Mapping | Aider-AI/aider | DeepWiki](https://deepwiki.com/Aider-AI/aider/2.5-repository-mapping) - Repository Mapping is a core feature in Aider that creates an intelligent contextual representation ...

7. [Improving aider's repo map to do large, simple refactors ...](https://engineering.meetsmore.com/entry/2024/12/24/042333) - Introduction aider is an LLM based tool you can run on your command line and ask it to write code fo...

8. [GitHub - everestmz/llmcat: Render LLM-friendly maps of repositories](https://github.com/everestmz/llmcat) - Render LLM-friendly maps of repositories. Contribute to everestmz/llmcat development by creating an ...

9. [FAQ](https://aider.chat/docs/faq.html) - Frequently asked questions about aider.

10. [serena — Agent Skill — MCP.Directory](https://mcp.directory/skills/serena) - This skill provides symbol-level code understanding and navigation using Language Server Protocol (L...

11. [Using Serena | GitHub Agentic Workflows](https://github.github.com/gh-aw/reference/serena/) - Configure the Serena MCP server for semantic code analysis and intelligent code editing in your agen...

12. [Meet Serena: The Open-Source Agent That "Indexes" Your Code (MCP Explained)](https://www.youtube.com/watch?v=r5E5ebl-d6M) - Most AI coding tools are just fancy text predictors. We break down Serena, the new MCP-based agent t...

13. [AI Code Assistant That Understands Your Entire Codebase - AIWire](https://aiwire.ai/articles/sourcegraph-cody-context-engine-entire-codebase) - Sourcegraph's new Cody Context Engine indexes entire codebases into a persistent semantic graph, let...

14. [Code Graph - Sourcegraph docs](https://sourcegraph.com/docs/cody/core-concepts/code-graph) - Documentation for Sourcegraph, the code intelligence platform.

15. [Hacker News](https://news.ycombinator.com/item?id=41002519)

16. [CLAUDE.md and Agents.md Explained: Stop Repeating Yourself to AI](https://www.youtube.com/watch?v=4m8AgfeK6kU) - Stop re-explaining your tech stack to AI.
CLAUDE.md and agents.md give your AI tools persistent proj...

17. [Pointing CLAUDE.md to AGENTS.md : r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/comments/1r9zx34/pointing_claudemd_to_agentsmd/) - ** All AI agent context has been centralized into a single file: **[AGENTS.md]( AGENTS.md )** . Plea...

18. [CLAUDE.md, AGENTS.md, and Every AI Config File Explained](https://dev.to/deployhq/claudemd-agentsmd-and-every-ai-config-file-explained-4pde) - Every AI coding tool now reads a configuration file from your project. Claude Code looks for...

19. [Local Persistent Semantic Memory for AI Agents](https://mcpmarket.com/server/memory-47) - Memory provides persistent, local semantic memory for AI agents through Model Context Protocol. Enjo...

20. [Apex Memory: Persistent Context & ...](https://mcpmarket.com/server/apex-memory) - Apex Memory is an ultra-lightweight Model Context Protocol (MCP) server designed to give AI coding a...

21. [mcp-memory-graph](https://mcpservers.org/servers/retrorobai/mcp-memory-graph) - Persistent memory for AI agents using a semantic knowledge graph. Store, retrieve, and connect memor...

22. [Try It Yourself](https://medium.com/@chmel_4702/give-your-ai-agents-a-memory-building-a-persistent-context-layer-with-fast-mcp-6071136881c4) - Large language models are capable of amazing things, but they suffer from one big limitation: they f...

23. [README.md - VILA-Lab/Dive-into-Claude-Code - GitHub](https://github.com/VILA-Lab/Dive-into-Claude-Code/blob/main/README.md) - A Systematic Analysis and Discussion of Claude Code for Designing Today's and Future AI Agent System...

24. [Dive into Claude Code: The Design Space of Today's and Future AI Agent ...](https://arxiv.org/html/2604.14228v1)