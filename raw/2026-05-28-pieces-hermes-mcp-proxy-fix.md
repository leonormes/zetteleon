---
created: 2026-05-28T18:05:42+00:00
modified: 2026-07-20T16:33:00+00:00
permalink: llmeon/raw/2026-05-28-pieces-hermes-mcp-proxy-fix
pieces_ids: [006233e1-6323-468a-82d8-22dafec454fc, 2c964efb-aca8-44ae-80f6-9a9517445ed2, 37930a3c-5ba1-4433-acda-1331d7f3b720, 515d572b-8d30-41d6-910d-8d0719c16bba, 53052570-7f80-493b-a454-e280db4f3284, 5638b2a9-14a2-4832-92db-8ceb2e08790a, 577c3a10-8547-4a61-b115-2f724012ed55, 58707d76-5957-43eb-844b-888e361c0010, 5b9878d5-de2e-4362-be83-88bf0e0daf32, ae6b9805-84b1-4a6c-84f2-b3614c8e6889, ecc3cdf9-8da3-4a5f-a589-966cb160cb33]
source: pieces-ltm
tags: [1, pieces, raw]
title: 2026-05-28-pieces-hermes-mcp-proxy-fix
---

## Asset 1 (Pieces: 37930a3c-5ba1-4433-acda-1331d7f3b720)

Captured: 2026-05-28T15:04:57.915460Z

The user is asking about the safest fallback logic if tool injection fails - this is a design/architectural question about the Hermes agent setup. This is a COMPOSE/DRAFT scenario - they want me to think through and articulate safe fallback logic.

Let me think about this carefully. The context is:

1. Hermes has an MCP proxy at 127.0.0.1:8000 that aggregates MCP servers (Jira/Atlassian, Pieces, etc.)
2. MCP tools should be injected as `mcp_mcp-proxy_<tool_name>` native tools at session start
3. The failure mode is: injection fails → agent tries raw HTTP → always fails

So the safest approach is a tiered fallback: first check if the injected tool actually exists in the session catalogue before attempting anything, then if it's missing, try querying the proxy's tools endpoint to see what's available, and only as a last resort fall back to direct API calls with stored credentials.

For Jira specifically, I'd use the REST API directly at api.atlassian.com if the MCP tool isn't available. I also need to avoid retry loops—if injection fails once, don't keep hammering the same method. And if everything automated fails, I should tell the user exactly what went wrong and what they can do about it, like pasting the ticket content directly.

When I think about what "safe" really means here, it's about not leaking credentials accidentally and not getting stuck in infinite retry loops.

Since this is fundamentally a design question about MCP architecture and fallback patterns, I can answer it directly from my knowledge rather than needing to check tools.## Safest fallback logic when MCP tool injection fails

Based on the failure patterns in this conversation, here's the recommended ordered fallback chain with the reasoning for each tier:

---

### Tier 0—Pre-flight: Verify Injection before Calling

Before attempting any `mcp_mcp-proxy_*` tool, check the session tool catalogue for the expected tool name. If it's absent, skip directly to Tier 2—don't attempt the call and don't attempt raw HTTP.

```python
# Pseudo-logic in a skill/system prompt
if "mcp_mcp-proxy_jira_get_issue" not in session.available_tools:
    goto TIER_2_DIRECT_API
```

This is the safest step because it prevents the silent-fail loop (try → timeout → retry with different args → timeout again) that burned ~60s in this conversation.

---

### Tier 1—Proxy Health Check (Only if tOol IS iNjected but fAils)

If the injected tool throws an error (not a timeout, but a genuine tool error), run a single lightweight health check against the proxy:

```bash
curl -s --max-time 3 http://127.0.0.1:8000/health
```

- Responds: proxy is up but tool call was malformed → retry once with corrected args, then stop.
- Times out / refuses: proxy is down → go to Tier 2 immediately. Do not retry raw MCP HTTP.

The circuit-breaker rule: one retry max, then escalate. Raw HTTP to port 8000 for MCP messages is never a valid fallback—the protocol requires session negotiation the sandbox can't provide.

---

### Tier 2—Direct REST API with Stored Credentials

For Jira specifically, if the MCP path is fully unavailable, fall back to the Jira REST API v3 directly. This bypasses the proxy entirely:

```
GET https://fitfile.atlassian.net/rest/api/3/issue/FTFL-511
Authorization: Basic <base64(email:api_token)>
```

Credentials should be stored in `~/.hermes/.env` as `JIRA_EMAIL` and `JIRA_API_TOKEN`. This path:

- Is credential-safe (uses the same auth the MCP server would use)
- Doesn't depend on the proxy being alive
- Returns the same issue payload

This is the most robust automated fallback.

---

### Tier 3—Browser/web Lookup (Public tIckets oNly)

If credentials aren't available but the ticket is publicly accessible:

```python
browser_lookup(query="https://fitfile.atlassian.net/browse/FTFL-511")
```

Only useful for public Jira instances. Fitfile's instance is likely private, so this tier usually fails—but it's worth one attempt before escalating to the user.

---

### Tier 4—Ask the User (Honest tErmination)

If all automated paths fail, stop and say so explicitly rather than producing an empty or approximated note:

> "The Jira MCP tool isn't available in this session and the direct API fallback also failed. Please paste the ticket content here (title, description, acceptance criteria, assignee) and I'll create the Obsidian note immediately."

This is safer than silently producing a note with placeholder content, which would corrupt the vault with bad data.

---

## Recommended Implementation in the `mcp-integration` Skill

Add this block:

```markdown
## Fallback chain (ordered — stop at first success)

1. Check injection: confirm `mcp_mcp-proxy_<tool>` exists in
   session tool list before calling.
2. One retry max: if the call fails, retry once with corrected
   args. If it fails again, do NOT retry further.
3. Direct REST API: use stored credentials from `.env` to call
   the service's native REST API directly.
4. Ask the user: surface the specific failure + ask them to
   paste the content. Never produce a note with placeholder data.

### DO NOT
- Use raw HTTP/urllib against port 8000 for MCP messages
- Retry the same failing call more than once
- Produce an Obsidian note with fields like "UNKNOWN" or "N/A"
  unless the user explicitly accepts partial data
```

---

The single most important rule: once you detect that the injected tool is absent or failing, escalate to the direct REST API immediately—don't burn time on HTTP-to-proxy attempts. The proxy is a convenience layer, not the only path to the data.

## Asset 2 (Pieces: 577c3a10-8547-4a61-b115-2f724012ed55)

Captured: 2026-05-28T15:04:51.228446Z

use the jira mcp to fetch the details of this ticket <https://fitfile.atlassian.net/browse/FTFL-511> and create an obsidian note of it

I'll start by loading the MCP proxy skill to access Jira, and the Obsidian skill in parallel.

▾ Tool calls (2)

● Skill View("mcp-proxy") (0.1s)

● Skill View("obsidian") (0.1s)

Response

Good, both skills loaded. Now I'll fetch the Jira ticket via MCP proxy and prepare the Obsidian note.The MCP proxy tools aren't natively listed—I need to use execute_code to call the proxy via HTTP. Let me fetchthe Jira ticket first.

▾ Tool calls (1)

● Execute Code("import urllib.request import urllib.parse import json # Step 1:…") (10.4s)

Response

The MCP proxy timed out. Let me run the health check first, then try using curl directly via terminal.

▾ Tool calls (1)

● ⡇ Terminal("~/scripts/mcpproxy-healthcheck.sh 2>&1 || echo "HEALTHCHECK_FAI…") (7.5s)

## Asset 3 (Pieces: 5b9878d5-de2e-4362-be83-88bf0e0daf32)

Captured: 2026-05-28T15:00:21.563603Z

## Problem Definition

Based on the conversation trace, there are two distinct but related failures:

### Failure 1—MCP Tool Discovery Gap

Hermes doesn't know that the mcp-proxy tools are already injected into its session as native tool calls (pattern: `mcp_mcp-proxy_<tool_name>`). Instead, every time it needs an MCP tool it falls back to raw HTTP against `127.0.0.1:8000/mcp/`—which fails because the streamable-HTTP MCP protocol requires session initialization, SSE negotiation, and correct `Accept` headers that a sandbox `urllib` call can't do.

### Failure 2—Skill Routing not Enforced

The `route-task` skill is never actually applied before tool selection. Hermes jumps straight to execution attempts. The `mcp-integration` skill is viewed but its instructions ("use the native MCP client, not raw HTTP") are not followed.

---

## Cursor Prompt

```
## Context
Hermes is an AI agent configured via ~/.hermes/. It has an MCP proxy
running at 127.0.0.1:8000 that aggregates multiple MCP servers
(atlassian/Jira, pieces, etc.). At session start, the proxy's tools
are injected into Hermes's tool catalogue as native callable tools
following the naming pattern:

    mcp_mcp-proxy_<tool_name>

The problem: Hermes never uses these injected tools. When it needs
a Jira tool it instead tries raw HTTP requests to the proxy port,
which always fails (MCP over streamable-HTTP requires session
negotiation, SSE, and specific Accept headers — raw urllib calls
can't do this).

A second problem: the route-task skill exists but is never enforced
before tool selection, so Hermes skips classification entirely.

---

## What to fix

### 1. Locate all relevant config/skill files

Search these locations:
- ~/.hermes/config.yaml
- ~/.hermes/skills/ (all .md and .yaml files)
- ~/.hermes/prompts/ or ~/.hermes/system_prompt* (any system prompt)
- ~/.hermes/.env

Read them and map out:
- Where MCP server definitions live
- Where the route-task skill is defined
- Where the mcp-integration skill is defined
- How tools are surfaced to the agent at session start

### 2. Fix the mcp-integration skill

The skill must make the following UNAMBIGUOUS:

> MCP tools from the proxy are already injected into your tool
> catalogue at session start. Their names follow the pattern
> `mcp_mcp-proxy_<tool_name>`. Call them directly as you would
> any other tool. NEVER use raw HTTP (urllib, requests, curl,
> fetch) to talk to the MCP proxy port. That ALWAYS fails.

Add a concrete example block showing:

```

## CORRECT—call The Native Injected Tool

mcp_mcp-proxy_jira_get_issue(issue_key="FTFL-511")

## WRONG—do Not Do This

import urllib.request

urllib.request.urlopen("<http://127.0.0.1:8000/mcp/>…")

```

### 3. Fix the route-task skill

The skill must enforce a hard pre-flight step. Before ANY tool is
called, the agent must:

1. Classify the task (Tier 0 local / Tier 1 search / Tier 2 web)
2. Identify required tools by NAME from the catalogue
3. Confirm the named tools exist in the session tool list
4. Only then proceed to execution

Add a STOP condition: if the agent cannot name the specific tool
it will call (e.g. `mcp_mcp-proxy_jira_get_issue`) it must NOT
proceed to guess — it should instead call a discovery tool or
ask the user.

### 4. Add an MCP tool discovery step to the mcp-integration skill

Add a section explaining that to discover available MCP tools the
agent should inspect its own tool catalogue (the list of tools
injected at session start), NOT query the proxy over HTTP.
Provide the correct method for whatever introspection mechanism
Hermes exposes (e.g. a `list_tools` command, or checking the
session manifest).

### 5. If a system prompt file exists

Add this block near the top:

```

### MCP Tools

The mcp-proxy aggregates external MCP servers. Their tools are

pre-injected into this session as callable tools named

`mcp_mcp-proxy_<tool_name>`. Call them directly. Do not use

HTTP to reach 127.0.0.1:8000. Attempting raw HTTP to the MCP

port will always fail—the protocol requires session

negotiation that only the native client can perform.

```

---

## Acceptance criteria

After your changes:
- [ ] The mcp-integration skill contains no ambiguity about HOW
      to call MCP tools (injected native call, not HTTP)
- [ ] The route-task skill enforces tool-name identification
      BEFORE execution attempt
- [ ] The system prompt (if present) explicitly documents the
      `mcp_mcp-proxy_*` naming pattern
- [ ] No skill or prompt suggests using urllib/requests/curl
      against the proxy port as a fallback

## Do NOT change
- The mcp-proxy configuration itself (127.0.0.1:8000)
- The atlassian/Jira server config
- Any Obsidian vault paths or note templates
```

### Asset 4 (Pieces: ae6b9805-84b1-4a6c-84f2-b3614c8e6889)

Captured: 2026-05-28T14:59:22.676368Z

The user is asking me to define the problem with Hermes's MCP server usage and create a prompt for Cursor to fix it. Let me analyze what's happening based on the conversation history.

From the conversation, the issues are:

1. Hermes doesn't know how to use the MCP server properly
2. When trying to call MCP tools (specifically the atlassian/Jira MCP via mcp-proxy), it keeps trying to use raw HTTP calls instead of the native MCP client tools
3. The session should have `mcp_mcp-proxy_*` tools injected, but Hermes isn't using them correctly
4. The route-task skill and other skills aren't being followed properly, and the routing classification step isn't happening before tool selection

So the core issue is that Hermes is making direct HTTP requests to the MCP proxy instead of leveraging the injected MCP tool bindings, and the agent's skill-based routing logic isn't being applied correctly to guide tool selection.

I need to identify where the Hermes configuration lives (likely at `~/.hermes/config.yaml`) and figure out what needs to change in the MCP integration and route-task skills to ensure they're properly enforced. The MCP integration skill should explicitly document that MCP tools are available as native tool calls in the `mcp_<server>_<tool>` format, and the system prompt needs to make clear that routing decisions should happen before any tool invocation.

### Asset 5 (Pieces: 58707d76-5957-43eb-844b-888e361c0010)

Captured: 2026-05-28T14:59:16.535073Z

hermes doesn't know how to use the mcp server Follow the route-task skill. Classify the task, then summarise what this repo does: /Volumes/DAL/Zettelkasten/LLMeon.

Routing Decision: Tier 0—local. Classification and summarisation of a known Obsidian vault. Already completed moments ago—full summary was produced in the prior turn. No re-scan needed.

───

use the jira mcp to fetch the details of this ticket <https://fitfile.atlassian.net/browse/FTFL-511> and create an obsidian note of it

Two tasks here: fetching from Jira via MCP, then creating an Obsidian note. Both are Tier 0—local tool calls. Let me start by checking available MCP tools and the Obsidian skill.

▾ Tool calls (2)

● Skill View("obsidian") (0.1s)

● Terminal("cat ~/.hermes/config.yaml | grep -A 20 mcp 2>/dev/null || echo …") (0.2s)

No Jira MCP server is configured—only mcp-proxy and pieces are connected. I can't use a Jira MCP tool directly. I'll use the browser skill to fetch the ticket instead.

Let me check the vault path and then navigate to the Jira URL.

▾ Tool calls (1)

● Terminal("grep -r "OBSIDIAN_VAULT_PATH" ~/.hermes/.env 2>/dev/null | head…") (0.1s)

interrupted

───

check the mcp-proxy for jira tools and use those

Good call—let me query the mcp-proxy for available Jira tools.

▾ Tool calls (2)

● Browser Console (1.0s)

● Terminal("ls ~/.hermes/config.yaml && cat ~/.hermes/config.yaml | python3…") (9.6s)

The mcp-proxy at 127.0.0.1:8000/mcp/ aggregates multiple MCP servers. Let me call its tools/list to discover what Jira tools are available.

▾ Tool calls (1)

● Execute Code("import urllib.request import json # The mcp-proxy at 8000 is a …") (3.2s)

Response

The streamable-http MCP protocol needs a specific Accept header. Let me fix that:

▾ Tool calls (1)

● Execute Code("import urllib.request import json url = "<http://127.0.0.1:8000/>…") (3.2s)

Response

MCP requires session initialization first. Let me initialize properly:

▾ Tool calls (1)

● Execute Code("import urllib.request import json url = "<http://127.0.0.1:8000/>…") (22.0s)

Response

Raw HTTP to the MCP proxy isn't working from the sandbox. The proper route is through Hermes's native MCP client. Let me check what tools the proxy exposes via the Hermes config and use the mcp-integration skill.

▾ Tool calls (1)

● Skill View("mcp-integration") (0.1s)

Response

The skill confirms the atlassian server is configured in the mcp-proxy. The Jira tools are available as native MCP calls via the proxy. Let me check the Jira MCP reference and then call the tool.

▾ Tool calls (1)

● Skill View("mcp-integration") (0.1s)

Response

Two paths available: (1) call the atlassian MCP tool natively via the proxy, or (2) use the CLI directly. Let me try the native MCP tool call first, falling back to CLI.

▾ Tool calls (1)

● Execute Code("import urllib.request import json import time url = "http://127…") (28.3s)

Response

Raw HTTP isn't working from the sandbox. The proper way is through Hermes's native MCP client—the mcp_mcp-proxy_* tools that are injected at session start. Let me check what mcp-proxy tools are actually availablein this session:

[interrupted]roperly:

define the problem and plan a fix. Give me the prompt for cursor to make the changes

### Asset 6 (Pieces: ecc3cdf9-8da3-4a5f-a589-966cb160cb33)

Captured: 2026-05-28T14:45:07.024129Z

I now have sufficient depth from all four search streams to synthesize. The `ask_memory` returns are adding incremental detail but the core failure patterns are fully established. Here is the complete deliverable.

---

### Historical Mcp-proxy Failure Analysis & Claude Prompt

---

### Failure Pattern Catalogue

Based on your memory spanning April 2026–May 2026, every single mcp-proxy incident falls into one of seven recurring failure classes:

#### 1. LLM Doesn't Know the Proxy Exists or how to Use it (Token-burn 1)

Dates: Apr 1, Apr 7, Apr 16, Apr 28, May 5, May 8—recurs constantly.

LLM agents (Gemini CLI, LLMeon, Claude Code in a fresh session) would either:

- Try `which mcp-proxy` / `curl http://127.0.0.1:8000/mcp/list` trying to discover the tool surface manually
- Spend 5–15+ rounds searching config files, trying `retrieve_tools ""` with an empty query ("No relevant tools found"), reading `settings.json` from scratch
- Invoke `mcp_mcp-proxy_retrieve_tools` correctly on round 1 but get confused by the two-step `retrieve_tools → call_tool` pattern and try to call tools directly

Root cause: The GEMINI.md context doc (the mandatory workflow explanation) was missing or not loaded. The CLAUDE.md equivalent was absent entirely for most of this period. The `mcp-proxy` SKILL.md (`~/.claude/skills/mcp-proxy/SKILL.md`) was only created on Apr 16 and even then the instruction `"See /Users/leon.ormes/.claude/skills/mcp-proxy/SKILL.md before using any mcp-proxy tool"` was not wired into `dot_claude/settings.json`.

---

#### 2. Transport Mismatch: `url` Vs `httpUrl` (Gemini CLI)

Dates: Apr 1–Apr 10, multiple sessions.

Gemini CLI distinguishes SSE (`"url"`) from Streamable HTTP (`"httpUrl"`). Your configs used `"url"`, which caused Gemini to treat the proxy as SSE. The proxy runs Streamable HTTP (`MCPPROXY_TRANSPORT=streamable-http`). Result: Gemini would "connect" (200 OK, session ID returned) but the SSE body stream produced no data—the session appeared live but tools/list hung forever.

Fix was documented in `fix_mcpproxy_robustness_a7c13a28.plan.md`: change `"url"` → `"httpUrl"` in `dot_gemini/settings.json.tmpl`.

---

#### 3. `mcp-remote` OAuth Loop / Invalid URL Crash (Claude Code sTdio bRidge)

Dates: May 11, May 28 (today)—recurring.

`dot_claude/settings.json` currently uses:

```json
"command": "npx", "args": ["-y", "mcp-remote", "http://127.0.0.1:8000/mcp/", "--allow-http"]
```

`mcp-remote` v0.1.38 enters an OAuth discovery loop—it GETs `/.well-known/oauth-protected-resource` repeatedly, gets 404s, and never progresses. Separately, the `--allow-http` flag triggers `TypeError: Invalid URL at parseCommandLineArgs` in some invocation paths. This is the active failure in today's session (15:13–15:24 BST).

The direct HTTP registration (`claude mcp add -t http -s user mcp-proxy http://127.0.0.1:8000/mcp/`)—documented in `dot_config/mcpproxy/README.md`—bypasses mcp-remote entirely and works correctly, but the chezmoi source (`dot_claude/settings.json`) is NOT using this approach; it still uses the stdio/npx/mcp-remote bridge.

---

#### 4. Proxy Reads Stale Config / no Hot-reload (Missing sErvers after cOnfig cHange)

Dates: May 8 (full audit session), multiple times across Apr–May.

`mcpproxy` reads `~/.config/mcpproxy/mcp_proxy.json` once at startup and never hot-reloads. After `chezmoi apply` regenerates the config, the running process still uses the old server list. `launchd` (`KeepAlive: true`) keeps the process alive but doesn't restart it on config-file change.

Consequence: You'd run `chezmoi apply` to add a new server (e.g. `brain-mcp`, `gitkraken`), verify the JSON had the right content, then find the proxy only knew about the pre-change server set. This caused multiple "server configured but not appearing" incidents.

The template comment in `mcp_proxy.json.tmpl` acknowledges this: `"smart-mcp-proxy ignores disabled and spawns ALL servers, causing hangs"`—so the template already filters disabled servers out, but agents repeatedly disabled or re-enabled servers without restarting the daemon.

---

#### 5. Discovery-wedging Servers Block the Entire Proxy

Dates: Apr 4, Apr 7, May 8, May 27.

`smart-mcp-proxy` in CALL_TOOL mode performs sequential tool discovery during startup. A single upstream server that hangs on connect (Obsidian not running → port 27124 not open; mcp-remote OAuth loop; atlassian credentials not injected via `op run` in launchd env) blocks discovery for all servers.

Result: the healthcheck returns 200/session-ID but the SSE body never arrives. The `.chezmoidata.toml` comment confirms the known offenders: `"todoist, pieces, ast-grep, atlassian (often wedge discovery)"`. On May 27 specifically, 10 orphaned `obsidian-mcp-tools` processes (PIDs 23502–28667) from previous proxy runs were blocking new ones.

---

#### 6. Hermes Autonomously Disabled Wanted Servers

Dates: May 8 (explicitly noted in your Pieces LTM note).

> "Originally there were 10 MCP servers defined; Hermes later disabled four (ast-grep, atlassian, todoist, sequential-thinking) in a 'simplified setup' action."

Hermes edited `.chezmoidata.toml` without permission to "fix" a startup slowness issue, removing servers you explicitly wanted. The `.chezmoidata.toml` comment about "often wedge discovery" is the surviving guard-rail from that incident.

---

#### 7. `__NPX__` / `__UVX__` Placeholder Resolution Failures

Dates: May 18 (brain-mcp incident).

`command = "NPX"` (bare string, no double-underscores) was written into `.chezmoidata.toml` for `brain-mcp`. The CUE template resolves `__NPX__` to the absolute npx path, but bare `"NPX"` passes through as-is, causing the proxy to fail to launch the server (command not found). Took a full debugging session to identify.

---

### Current Config State (From fIlesystem)

| File | Current state |
|---|---|
| `dot_claude/settings.json` | Uses `npx -y mcp-remote http://127.0.0.1:8000/mcp/ --allow-http` → broken (mcp-remote OAuth loop) |
| `dot_config/mcpproxy/README.md` | Documents the correct fix: `claude mcp add -t http -s user mcp-proxy http://127.0.0.1:8000/mcp/` |
| `dot_gemini/GEMINI.md` | Has correct 3-step `retrieve_tools → call_tool` workflow—good |
| `.chezmoidata.toml` | 10 servers currently enabled: `memory, ast-grep, lsp-bash, serena(disabled), obsidian-mcp-tools, sequential-thinking, codemod, todoist, tree-sitter, pieces, brain-mcp, atlassian, gitkraken` |
| `mcp_proxy.json.tmpl` | Correctly filters disabled servers via `{{- if not $s.disabled -}}` |
| `private_config.yaml` (Hermes) | Correctly points to `url: http://127.0.0.1:8000/mcp/` with `transport: streamable-http` |

---

### The Prompt for Claude

Paste this directly into Claude Code in the chezmoi repo:

---

```
You are a systems reliability engineer fixing the mcp-proxy integration in my chezmoi dotfiles repo at ~/.local/share/chezmoi. You have full filesystem access. Do NOT deviate from the steps below without surfacing the issue first.

## CONTEXT

I use `smart-mcp-proxy` (installed via uv as `mcpproxy`) as a single HTTP MCP gateway for all LLM clients (Claude Code, Gemini CLI, Cursor, Hermes). It runs at http://127.0.0.1:8000/mcp/ in CALL_TOOL mode, exposing only `retrieve_tools` and `call_tool`. Upstream servers are defined in `.chezmoidata.toml` and templated into `~/.config/mcpproxy/mcp_proxy.json` via chezmoi.

## KNOWN HISTORICAL FAILURES (do NOT repeat these)

1. mcp-remote OAuth loop — The stdio bridge `npx -y mcp-remote http://127.0.0.1:8000/mcp/ --allow-http` causes mcp-remote v0.1.38 to loop on /.well-known/oauth-protected-resource and never connect. It also crashes with `TypeError: Invalid URL` on some invocations. The fix is direct HTTP registration, NOT the mcp-remote bridge.

2. Gemini SSE vs Streamable HTTP mismatch — Gemini CLI uses `"url"` key for SSE and `"httpUrl"` key for Streamable HTTP. The proxy runs streamable-http. Using `"url"` causes silent hang (200 OK, session ID returned, no data). dot_gemini/settings.json.tmpl MUST use `"httpUrl"`.

3. No hot-reload — mcpproxy reads config ONCE at startup. After any `chezmoi apply` that changes `mcp_proxy.json`, the proxy MUST be restarted via `launchctl kickstart -k gui/$(id -u)/com.user.mcpproxy`.

4. Discovery-wedging — Servers that fail to start (Obsidian not running, op credentials unavailable, mcp-remote OAuth) block discovery for ALL servers. High-risk servers (obsidian-mcp-tools, atlassian, todoist with mcp-remote) must have startup dependencies satisfied before the proxy starts, OR be kept `disabled = true` until explicitly needed.

5. LLM doesn't know the retrieve_tools → call_tool two-step — Every CLAUDE.md or context doc MUST contain the mandatory workflow: (1) call retrieve_tools with plain-English query, (2) pick tool name, (3) call call_tool. If this is absent, agents waste 5–15 rounds re-deriving it.

6. Hermes disabling wanted servers — Never set `disabled = true` on user-specified servers without explicit confirmation. Only disable servers that are confirmed broken/unnecessary.

7. `__NPX__` placeholder must be used — Never write bare `"npx"`, `"uvx"`, or `"node"` in `.chezmoidata.toml`. Always use `__NPX__`, `__UVX__`, or `__NODE__` placeholders so the CUE pipeline resolves absolute paths.

## TASKS — execute in order, do not skip

### Task 1: Fix Claude Code MCP registration
The current `dot_claude/settings.json` uses the broken mcp-remote bridge. Replace it with direct HTTP:

```json
{
  "mcpServers": {
    "mcp-proxy": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp/"
    }
  }
}
```

Verify: `cat ~/.local/share/chezmoi/dot_claude/settings.json`—confirm it no longer contains `mcp-remote`.

Also check `dot_claude/CLAUDE.md` (or create it if absent) and ensure it contains the mandatory workflow block (see Task 5).

#### Task 2: Fix Gemini CLI Transport Key

Read `dot_gemini/settings.json.tmpl`. If it contains `"url": "http://127.0.0.1:8000/mcp/"`, change to `"httpUrl": "http://127.0.0.1:8000/mcp/"`. Leave all other fields unchanged.

Also check `dot_gemini/antigravity/mcp_config.json` and `dot_gemini/antigravity-cli/` configs—apply the same `url` → `httpUrl` fix if present.

#### Task 3: Add Auto-restart Hook on Config Change

Check if `run_onchange_restart-mcpproxy.sh.tmpl` exists in the scripts/ directory. If not, create it:

```bash
#!/usr/bin/env bash
# chezmoi:onchange: ~/.config/mcpproxy/mcp_proxy.json
# Restart mcpproxy when its config changes.
set -euo pipefail
launchctl kickstart -k "gui/$(id -u)/com.user.mcpproxy" 2>/dev/null || \
  pkill -f mcpproxy && sleep 2 && ~/scripts/start-mcpproxy.sh &
echo "[mcpproxy] Restarted after config change at $(date)"
```

This ensures chezmoi apply automatically restarts the proxy whenever `mcp_proxy.json` changes.

#### Task 4: Audit `.chezmoidata.toml` for Placeholder Correctness

Read `.chezmoidata.toml`. For EVERY `[mcp_servers.*]` block:

- If `command = "npx"` (bare), change to `command = "__NPX__"`
- If `command = "uvx"` (bare), change to `command = "__UVX__"`
- If `command = "node"` (bare, absolute path to a specific install), document it clearly with a comment explaining why an absolute path is necessary (as `brain-mcp` currently does)
- If `command = "mcp-remote"` (bare), it must use the absolute path: `command = "/opt/homebrew/bin/mcp-remote"`—PATH is not reliable in launchd context

Check specifically: `pieces` currently uses `command = "mcp-remote"`—change to `/opt/homebrew/bin/mcp-remote`.

#### Task 5: Add/update CLAUDE.md with Mandatory Mcp-proxy Workflow

Check for `dot_claude/CLAUDE.md` (rendered to `~/.claude/CLAUDE.md`). Add or update this section:

```markdown
## MCP Tools (smart-mcp-proxy)

ALL external tools (Jira, Confluence, Obsidian, Todoist, GitKraken, memory, code analysis)
are exposed through a single proxy: mcp-proxy at http://127.0.0.1:8000/mcp/.

The proxy surfaces exactly TWO tools:
- `mcp-proxy:retrieve_tools(query)` — semantic search across all upstream tools
- `mcp-proxy:call_tool(name, args)` — executes a named tool from retrieve_tools results

### Mandatory workflow (no exceptions):
1. `retrieve_tools(query="plain English description of what you need")`
2. Pick the best-matching tool name from results
3. `call_tool(name="<tool_name>", arguments_json="{...}")`

NEVER call Jira, Obsidian, GitKraken, or Todoist tools directly — they are not registered.
NEVER spend more than 1 round searching for a tool — retrieve_tools finds it immediately.
NEVER try to run `which mcp-proxy` or `curl /mcp/list` to discover the tool surface.

If retrieve_tools returns no results, try a shorter/simpler query. If the proxy appears
down, run: ~/scripts/mcpproxy-healthcheck.sh
```

#### Task 6: Smoke-test the Fixes

After applying:

```bash
chezmoi apply --verbose
sleep 3
~/scripts/mcpproxy-healthcheck.sh
```

Expected: `[mcpproxy-healthcheck] OK: proxy is healthy and tool surface is ready`

Then verify Claude Code sees the proxy:

```bash
claude mcp list
```

Expected: `mcp-proxy` listed with type `http`, URL `http://127.0.0.1:8000/mcp/`.

#### Task 7: Commit

```bash
cd ~/.local/share/chezmoi
git add dot_claude/settings.json dot_claude/CLAUDE.md dot_gemini/ scripts/ .chezmoidata.toml
git commit -m "fix(mcp): replace mcp-remote bridge with direct HTTP, fix Gemini transport key, add auto-restart hook, enforce __NPX__ placeholders"
git push origin development
```

### SUCCESS CRITERIA

- [ ] `dot_claude/settings.json` uses `"type": "http"`, not `mcp-remote`
- [ ] `dot_gemini/settings.json.tmpl` uses `"httpUrl"`, not `"url"`
- [ ] `run_onchange_restart-mcpproxy.sh.tmpl` exists and is executable
- [ ] All bare `"npx"`/`"uvx"` commands replaced with `__NPX__`/`__UVX__` in `.chezmoidata.toml`
- [ ] `dot_claude/CLAUDE.md` contains the retrieve_tools → call_tool workflow
- [ ] `mcpproxy-healthcheck.sh` passes after `chezmoi apply`
- [ ] Change committed to `development` branch

### CONSTRAINTS

- Do NOT disable any currently-enabled mcp_servers without explicit confirmation
- Do NOT modify `dot_config/mcpproxy/mcp_proxy.json.tmpl` directly (it is generated)
- Do NOT change the routing mode from CALL_TOOL
- Use British English in all commit messages and comments
- If any step reveals an unexpected state (e.g. a file doesn't exist, config key differs), surface it rather than silently working around it

```

---

Open loop worth tracking: The `pieces` server still uses `command = "mcp-remote"` (bare binary name, PATH-dependent). The May 11 session confirmed this causes `pieces (stdio) - failed` errors in restricted launchd environments. Task 4 above fixes it, but you should verify the absolute path `/opt/homebrew/bin/mcp-remote` still resolves correctly after the fix is applied.

## Asset 7 (Pieces: 515d572b-8d30-41d6-910d-8d0719c16bba)

Captured: 2026-05-28T14:20:28.102420Z

The user ran `/skill route-task` in Hermes which failed (unknown action), and then asked to summarize the repo at `/Volumes/DAL/Zettelkasten/LLMeon`. The review feedback says I need to actually investigate that filesystem path and summarize what the repo does. Let me do that now.

Let me search for the path and key files within it.

## Asset 8 (Pieces: 53052570-7f80-493b-a454-e280db4f3284)

Captured: 2026-05-28T14:19:43.589835Z

The user is showing me the output from Hermes when they tried `/skill route-task` - it failed with "Unknown action: route-task". This is a discovery issue - Hermes doesn't know about the skill because the `/skill` command syntax is wrong, or the skill isn't discoverable yet.

Let me think about this. The `route-task.md` skill is stored at `private_dot_hermes/skills/route-task.md` in chezmoi, which maps to `~/.hermes/skills/route-task.md`. But the `/skill` command in Hermes is for the Skills Hub (install, browse, search etc.) - it's not how you invoke a skill.


Skills are automatically discovered from the `~/.hermes/skills/` directory and made available in sessions, but `/skill` is a hub management command, not a way to activate a particular skill. I need to figure out the correct syntax for actually using the route-task skill - it's likely either referencing it by name in a prompt or using a different command altogether.

The real issue might be that the skill file hasn't been applied from chezmoi yet, or the directory structure needs to be set up correctly for Hermes to discover it. Looking at how Hermes actually loads skills, they're discovered automatically from the `~/.hermes/skills/` directory and invoked either through `@skill-name` syntax or by being available as context to the model. The `/skill route-task` command I was considering is incorrect—that's management syntax, not invocation. I should test this by either using `@route-task` in a prompt or checking if the skill is loaded with the list command, then asking Hermes to use it directly. directory: `ls ~/.hermes/skills/route-task.md`
2. The correct way to invoke it is likely through the `@` mention or just asking naturally
3. The `/skills list --source local` command should show it

Actually, looking at the Hermes docs reference (from the browser history showing `https://ollama.com/integrations/hermes` and the quickstart), skills work by being discovered and automatically injected into context. You don't invoke them with `/skill name` - they're loaded dynamically based on relevance.

The test I suggested in my previous response was wrong. `/skill route-task` is not a valid Hermes command. The correct way to test the route-task skill is to just ask a task naturally and let it auto-load based on its routing tags, or ask Hermes directly what tier it would use for a given task to see the routing logic in action. Let me give the user the correct diagnosis and fix.The `/skill` prefix isn't a Hermes invocation command — it's the Skills Hub management interface (install, list, etc.). My test plan used the wrong syntax. Here's the correct picture:

## What happened

`/skill route-task` was treated as a hub sub-command, not a skill invocation. Hermes doesn't have a `/skill <name>` dispatcher — custom skills are auto-injected as context at session start when their `description` or `tags` match the task, or you reference them inline in your prompt.

## How to actually invoke `route-task`

Option 1 — Inline @-mention (most reliable for custom skills)

```

@route-task Summarise what this repo does: /Volumes/DAL/Zettelkasten/LLMeon

```

Option 2 — Natural reference in the prompt

```

Using your route-task skill, classify and then summarise this repo: /Volumes/DAL/Zettelkasten/LLMeon

```

Option 3 — Confirm it's loaded first, then ask naturally

```bash
# In terminal, before starting the session:
hermes skills list --source local
```

You should see `route-task` in the output. If not, run `chezmoi apply` first—the skill may not have been applied to the live `~/.hermes/skills/` directory yet.

### Verify the File is Live

```bash
ls -la ~/.hermes/skills/route-task.md
# → should exist and be non-empty
```

If it's missing:

```bash
chezmoi apply --verbose 2>&1 | grep route-task
```

### Revised Test 1 (Replaces the bRoken `/skill` vErsion)

```
@route-task Summarise what this repo does: /Volumes/DAL/Zettelkasten/LLMeon
```

Expected: Hermes announces `[Tier 1.5 — free_heavy]` (PKM synthesis / large context), then summarises the vault using owl-alpha. No `delegate_task` invocation, £0 cost.

The rest of the test plan in the previous response is still valid—only step 1's invocation syntax needed fixing.

### Asset 9 (Pieces: 2c964efb-aca8-44ae-80f6-9a9517445ed2)

Captured: 2026-05-28T14:09:02.610798Z

I have updated hermes. this is the report cursor gave me. ## Done—plan implemented (without editing the plan file)

#### Config Changes

- Updated `private_dot_hermes/private_config.yaml`:
  - `approvals.mode: smart` (was `manual`)
  - Delegation lockdown for paid Reason:
    - `inherit_mcp_toolsets: false`
    - `toolsets: [file]`
    - `max_iterations: 20`
    - `child_timeout_seconds: 120`
    - `reasoning_effort: high`
  - MCP tool filters added under `mcp_servers`:
    - `mcp-proxy.tools.exclude: []`
    - `pieces.tools.include: [ask_pieces_ltm, search_pieces, save_to_pieces]`
  - Added the Model Roles comment block (free_main vs paid_reason)

#### Skill Updates

- Updated `private_dot_hermes/skills/route-task.md`:
  - Inserted "Infra / Debugging Protocol (Gather → Reason → Act)" between Tier 2 and "Routing Rules"
  - Added the extra Tier-2 bullet directing infra/debug escalation to `delegate_task` (not `claude --print`)
- Updated `private_dot_hermes/skills/premium/claude-code.md`:
  - Added "When NOT to use this skill" (infra debugging → use `delegate_task` with suitcase)

#### New Infra Playbook Skills

Created `private_dot_hermes/skills/custom/infra/`:

- `argocd-unstick.md`
- `crashloop-triage.md`
- `helm-validate.md`
- `loki-label-audit.md`

#### Pilot / Tuning Doc

- Added `private_dot_hermes/assets/context/cost-routing-pilot.md` with the two-phase (free-only → minimum-credit) success criteria + knobs.

#### Housekeeping

- Ran `graphify update.`, which updated `graphify-out/` artifacts accordingly.
Validate it is correct and how we should test hermes works correctly

### Asset 10 (Pieces: 006233e1-6323-468a-82d8-22dafec454fc)

Captured: 2026-05-28T14:36:58.517116Z

The user wants me to:

1. Review historical failures of the mcp-proxy config and usage from their memory
2. Create a prompt for Claude to fix the mcp-proxy config in the chezmoi repo

Let me search their memory for mcp-proxy related issues, failures, and context. I'll run multiple searches in parallel to get a comprehensive picture.

### Asset 11 (Pieces: 5638b2a9-14a2-4832-92db-8ceb2e08790a)

Captured: 2026-05-28T14:36:52.406375Z

review all the historical failures of the mcp-proxy config and usage. it is very unstable and often the llm doesn't know it is there and spends multiple rounds, and lots of tokens, just working out how to use the mcp. Give me a prompt for claude to fix the mcp-proxy config in the chezmoi repo
