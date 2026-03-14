---
created: 2026-03-14T09:50:12+00:00
modified: 2026-03-14T11:09:30+00:00
tags: [articles]
title: Introducing MCP CLI A way to call MCP Servers Efficiently
---

## Introducing MCP CLI: A way to Call MCP Servers Efficiently

![rw-book-cover](https://www.philschmid.de/static/blog/mcp-cli/thumbnail.jpg)

### Metadata

- Author: [[Philipp Schmid]]
- Full Title: Introducing MCP CLI: A way to call MCP Servers Efficiently
- Category: articles
- Summary: Mcp-cli is a lightweight tool that helps AI agents use MCP servers efficiently by loading only the needed tool information, reducing token use by 99%. It supports local and remote servers, letting agents discover and call tools dynamically without context overload. This makes AI coding faster and cheaper while handling many servers and tools easily.
- URL: <https://share.google/JRbNUA1YhPM94WX82>

### Full Document

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/getting-started/intro) is an open standard for connecting AI agents to external tools, APIs, and data sources. However, as the ecosystem grows with more powerful MCP servers, developers and agent builders are hitting a scaling bottleneck: context window bloat.

[mcp-cli](https://github.com/philschmid/mcp-cli) is a lightweight CLI that allows dynamic discovery of MCP, reducing token consumption while making tool interactions more efficient for AI coding agents.

Key Features:

- 🪶 Built on [Bun](https://bun.sh/), `mcp-cli` compiles to a single standalone binary.
- 🔌 Works with both stdio (local) and HTTP (remote) MCP servers.
- 🔍 Glob-based search across all servers `mcp-cli grep *mail* -d`.
- 🤖 Designed for AI coding agents (Gemini CLI, Claude Code, etc.).
- 💡 Structured error messages with recovery suggestions.

Every MCP server comes with tool definitions schemas describing what each tool does, its parameters, types, and descriptions. Traditional MCP integration loads all of these schemas upfront into the agent's context window.

Here's what that looks like in practice:

![comparison](https://www.philschmid.de/static/blog/mcp-cli/comparison.jpeg)

| Setup | Tokens Used |
| --- | --- |
| 6 MCP servers, 60 tools | ~47,000 tokens |
| After dynamic discovery | ~400 tokens |

That is a 99% reduction in MCP-related token usage for this scenario.

When working with multiple MCP servers (GitHub, databases, browser automation—tool), definitions quickly consume a third or more of the effective context. This leads to:

- Reduced effective context length for actual reasoning and code generation.
- More frequent context compactions interrupting flow.
- Hard limits on the number of simultaneous MCP servers you can use.
- Higher API costs due to input token overhead.

The solution is dynamic context discovery. Instead of loading everything upfront (static context), agents pull in only the information they need, when they need it.

![](https://www.philschmid.de/static/blog/mcp-cli/dynamic-discovery.jpg)

`mcp-cli` implements this pattern for MCP:

- Step 1: "What servers exist?" → `mcp-cli`
- Step 2: "What are the params for tool X?" → `mcp-cli github/search`
- Step 3: Execute → `mcp-cli github/search '{"path": "README.md"}'`

Most Interactions only use a handful of tools, yet static loading consumes tokens for every tool definition. Dynamic discovery inverts this, you pay only for what you use.

#### Quick Start

[mcp-cli](https://github.com/philschmid/mcp-cli) allows dynamic discovery of MCP while making tool interactions more efficient for AI coding agents.

##### 1. Installation

```

curl -fsSL https://raw.githubusercontent.com/philschmid/mcp-cli/main/install.sh | bash
 

```

##### 2. Create a Config File

Create `mcp_servers.json` in your current directory or `~/.config/mcp/`:

```

      "url": "https://mcp.deepwiki.com/mcp"

```

##### 4. Call a Tool

##### 5. Execute the Tool

##### 6. Complex Commands

MCP CLI allows the model to generate commands that chain multiple tool calls together.

```

{"content": "Text with 'single quotes' and \"double quotes\""}

 

JSON='{"message": "Hello, it'\''s a test"}'

 

cat args.json | mcp-cli server/tool
 

jq -n '{query: "mcp", filters: ["active", "starred"]}' | mcp-cli github/search
 

mcp-cli filesystem/search_files '{"path": "src/", "pattern": "*.ts"}' --json | jq -r '.content[0].text' | head -1 | xargs -I {} sh -c 'mcp-cli filesystem/read_file "{\"path\": \"{}\"}"'
```

`mcp-cli` is designed to be used with AI Agents and bash tools. There are two main ways to integrate it:

##### Option 1: System Instructions Integration

Add this to your AI agent's system prompt for direct CLI access:

```

 

 

 

mcp-cli <server>/<tool>              # Get tool JSON schema and descriptions

 

 

 
1. Discover: Run `mcp-cli` to see available servers and tools or `mcp-cli grep "<pattern>"` to search for tools by name (glob pattern)
2. Inspect: Run `mcp-cli <server> -d` or `mcp-cli <server>/<tool>` to get the full JSON input schema if required context is missing. If there are more than 5 mcp servers defined don't use -d as it will print all tool descriptions and might exceed the context window.  

 

 

 

 

 

mcp-cli filesystem/search_files '{"path": "src/", "pattern": "*.ts"}' --json | jq -r '.content[0].text' | head -1 | xargs -I {} sh -c 'mcp-cli filesystem/read_file "{\"path\": \"{}\"}"'

 

 
1. Always check schema first: Run `mcp-cli <server> -d or `mcp-cli <server>/<tool>` before calling any tool

```

##### Option 2: Agent Skills

For AI agents that support [Agent Skills](https://agentskills.io/home) an upcoming standard for extending coding agents. mcp-cli ships with a ready-to-use skill definition.

Create `mcp-cli/SKILL.md` in your agent's skills directory:

```

description: Interface for MCP (Model Context Protocol) servers via CLI. Use when you need to interact with external tools, APIs, or data sources through MCP servers.

 

 
Access MCP servers through the command line. MCP enables interaction with external systems like GitHub, filesystems, databases, and APIs.
 

 

| `mcp-cli` | List all servers and tool names |

| `mcp-cli <server>/<tool> '<json>'` | Call tool with arguments |
| `mcp-cli grep "<glob>"` | Search tools by name |
 
Add `-d` to include descriptions (e.g., `mcp-cli filesystem -d`)
 

 
1. Discover: `mcp-cli` → see available servers and tools
2. Explore: `mcp-cli <server>` → see tools with parameters

 

 

 

 

 

 

 

 

 

 

 

mcp-cli filesystem/search_files '{"path": "src/", "pattern": "*.ts"}' --json | jq -r '.content[0].text' | head -1 | xargs -I {} sh -c 'mcp-cli filesystem/read_file "{\"path\": \"{}\"}"'

 
 

 

| `-r, --raw` | Raw text content |
| `-d` | Include descriptions |
 

 
- `0`: Success

- `2`: Server error (tool failed)

```

The AI Agent space is moving incredibly fast. `mcp-cli` tries to solve context tool discovery problem turning it into an iterative, just-in-time process. It allows agents to access a massive ecosystem of shared capabilities without the context bloat of static integration. Whether used within a Skill or as a standalone utility, it ensures your agent spends its tokens on reasoning, not configuration.

The project is open source and designed to fit into existing workflows. Give it a try and contribute at [github.com/philschmid/mcp-cli](https://github.com/philschmid/mcp-cli).

Thanks for reading! If you have any questions or feedback, please let me know on [Twitter](https://twitter.com/_philschmid) or [LinkedIn](https://www.linkedin.com/in/philipp-schmid-a6a2bb196/).
