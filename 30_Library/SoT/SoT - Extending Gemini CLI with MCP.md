---
aliases: [Gemini MCP, MCP]
conformant: false
created: 2025-12-21T00:00:00+00:00
last_reviewed: '2025-12-21'
modified: 2026-08-29T09:36:36+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-extending-gemini-cli-with-mcp
status: evolving
tags: [extensions, gemini-cli, mcp, SoftwareEngineering/Architecture, tools]
title: SoT - Extending Gemini CLI with MCP
type: sot
updated: null
---

## 1. Definitive Statement: "MCP Architecture"

---

## 2. Configuration & Setup

MCP servers are defined on a per-project basis within a local configuration file.

- Configuration File: `.gemini/settings.json`
- Structure: The JSON file contains an `mcp` array, where each object specifies the `command` and `args` needed to launch a specific MCP server.
- Environment Management: It is best practice to run each MCP server in its own sandboxed virtual environment (e.g., using `uv` or `python -m venv`) to manage dependencies and avoid conflicts.

### Example `settings.json`

```json
{
  "mcp": [
    {
      "command": "/path/to/your/project/.venv/bin/python",
      "args": ["-m", "my_mcp_server"]
    }
  ]
}
```

- Discovery: Once configured, the Gemini CLI automatically starts these servers in the background upon launch. You can verify which tools are active by running `/mcp list`.

---

## 3. Use Cases & Examples

MCPs can bridge the gap to almost any external service.

1. Alternative Search Tools (e.g., DuckDuckGo): Can be used to bypass the limitations of the built-in Google Search, such as retrieving raw, direct URLs without redirection.
2. Third-Party APIs (e.g., Hugging Face): Allows the model to send data to external models or services. An example workflow is passing an image URL to a Hugging Face Space that "giflifies" it and having the CLI download the result locally.
3. Up-to-Date Documentation (e.g., Context 7): Provides the model with the latest documentation for a specific library or framework. This is crucial for ensuring that generated code uses current APIs and avoids deprecated functions.
4. Custom Application Control (e.g., Obsidian): An MCP server can be built to expose the Obsidian REST API, allowing the Gemini agent to directly read, write, and search notes within a vault, forming the basis of the "Thinking Machine" architecture.

---

## 4. Official & Custom Extensions

Google is building an ecosystem of official extensions that streamline this process.

- Installation: Extensions are typically installed into the `~/.gemini/extensions/` directory.
- Jules Extension: An autonomous background agent that can perform complex, asynchronous tasks like cloning a repo, installing dependencies, fixing bugs, and submitting a pull request while the user continues to work in the main CLI session.
- Code Wiki CLI: A tool that scans an entire codebase on demand to generate a searchable, up-to-date wiki, providing architectural overviews and documentation automatically.
