---
title: gcx CLI Setup — FITFILE Grafana Stacks
created: 2026-05-19T22:29:21+00:00
source: pieces-ltm
pieces_ids:
  - a4bd5558-c9be-4226-bb84-1db404eea34f
  - 7832f531-dad9-4bda-9629-4b0d7dbfa199
  - 2474c2e1-ac86-4e73-b774-e3a8d6619e6d
  - ab317018-890b-47e2-ae7b-7ca195f6118a
  - 6b5a24ff-c41d-43f8-b0af-6cde6f90ae79
tags: [raw, pieces]
---

## Asset 1 (Pieces: a4bd5558-c9be-4226-bb84-1db404eea34f)
*Captured: 2026-05-19T08:52:37.633965Z*

help me set up and authenticate the gcx cli tool 
gcx --help

   █████╗   █████╗██╗  ██╗
  ██╔═══╝  ██╔═══╝╚██╗██╔╝
  ██║  ███╗██║     ╚███╔╝
  ██║   ██║██║     ██╔██╗
  ╚██████╔╝╚█████╗██╔╝ ██╗
   ╚═════╝  ╚════╝╚═╝  ╚═╝
  Grafana CLI


  gcx is a unified CLI for managing Grafana resources, dashboards,
  datasources, alerting, and Cloud product APIs (SLO, IRM, Synthetic
  Monitoring, Fleet, k6, and more).


Usage:
  gcx [command]

Available Commands:
  agent            Agent mode utilities
  aio11y           Manage Grafana AI Observability resources
  alert            Manage Grafana alert rules and alert groups
  api              Make direct HTTP requests to the Grafana API
  appo11y          Manage Grafana App Observability settings
  assistant        Interact with Grafana Assistant
  commands         List all commands with rich metadata for agent consumption
  completion       Generate the autocompletion script for the specified shell
  config           View or manipulate configuration settings
  dashboards       Manage Grafana dashboards
  datasources      Manage and query Grafana datasources
  dev              Manage Grafana resources as code
  fleet            Manage Grafana Fleet Management pipelines and collectors
  frontend         Manage Grafana Frontend Observability resources
  help             Help about any command
  help-tree        Print a compact command tree for agent context injection
  irm              Manage Grafana IRM (OnCall + Incidents)
  k6               Manage Grafana k6 Cloud projects, load tests, and schedules
  kg               Manage Grafana Knowledge Graph rules, entities, and insights
  login            Log in to a Grafana instance
  logs             Query Loki datasources and manage Adaptive Logs
  metrics          Query Prometheus datasources and manage Adaptive Metrics
  profiles         Query Pyroscope datasources and manage continuous profiling
  providers        Manage registered providers
  resources        Manipulate Grafana resources
  setup            Onboard and configure Grafana Cloud products.
  slo              Manage Grafana SLO definitions and reports
  stacks           Manage Grafana Cloud stacks (list, create, update, delete)
  synthetic-monitoring Manage Grafana Synthetic Monitoring checks and probes
  traces           Query Tempo datasources and manage Adaptive Traces
  version          Print version information.

Flags:
      --agent              Enable agent mode (JSON output, no color). Auto-detected from CLAUDECODE, CLAUDE_CODE, CURSOR_AGENT, GITHUB_COPILOT, AMAZON_Q, or GCX_AGENT_MODE env vars.
      --context string     Name of the context to use (overrides current-context in config)
  -h, --help               help for gcx
      --log-http-payload   Log full HTTP request/response bodies (includes headers — may expose tokens)
      --no-color           Disable color output
      --no-truncate        Disable table column truncation (auto-enabled when stdout is piped)
  -v, --verbose count      Verbose mode. Multiple -v options increase the verbosity (maximum: 3).
      --version            version for gcx

Use "gcx [command] --help" for more information about a command.

I want to have my llm be able to read details from both of my grafana stacks

## Asset 2 (Pieces: 7832f531-dad9-4bda-9629-4b0d7dbfa199)
*Captured: 2026-05-19T08:52:48.206672Z*

The user wants to set up and authenticate the `gcx` CLI tool and configure it to work with both of their Grafana stacks, so their LLM can read details from both. Let me search their memory for any relevant context about their Grafana setup, stacks, credentials, etc.

Let me search for Grafana-related information in their memory.

## Asset 3 (Pieces: 2474c2e1-ac86-4e73-b774-e3a8d6619e6d)
*Captured: 2026-05-19T08:56:39.759974Z*

All three searches are now exhausted (two returned `sufficient`, one returned `sufficient` on the Grafana stack cursor). Here is the complete setup guide, grounded in what's actually in your memory:

---

## `gcx` Setup & Authentication Guide for Your Two Grafana Stacks

### What you're working with

From your memory, your FITFILE Grafana Cloud org has two stacks on a **Grafana Cloud Pro** subscription:

| Context name | Stack URL | Purpose |
|---|---|---|
| `fitfileprod` | `https://fitfileprod.grafana.net` | Production |
| `fitfiletest` | `https://fitfiletest.grafana.net` | Testing / Non-prod |

Your access policies are managed at [grafana.com/orgs/garethhailes/access-policies](https://grafana.com/orgs/garethhailes/access-policies). Relevant policies that already exist include:

- `terraform-automation-policy` (ID: `72ce4489-8442-47ad-b130-2aa7a3ecf3ba`) — scoped to all stacks, with `stacks:read`, `stack-service-accounts:write`, etc.
- `terraform-automation-policy-gcx` (ID: `fd0b4719-f6a3-49b6-815b-7742e5f95642`) — a dedicated `gcx` policy
- `Leon_Local` policy (ID: `d932809b-691c-49f2-80e8-0c8ec75297d1`)
- **Production** and **Non-Production** Grafana Agent Write OBS policies for ingestion

---

### Step 1 — Create a service account token per stack

For LLM / agent use, **service account tokens are the right choice** — browser OAuth requires interactive login. Your memory confirms you've seen the prompt:

```
> Auth (browser) - recommended for cloud stacks; experimental on some configurations
> Service account token (requires permissions for managing service accounts)
```

For each stack, navigate to the stack's Grafana UI and create a service account token with the minimum scopes your LLM needs (typically `datasources:read`, `dashboards:read`, `explore`):

- **fitfileprod** → `https://fitfileprod.grafana.net` → Administration → Service Accounts → New token
- **fitfiletest** → `https://fitfiletest.grafana.net` → Administration → Service Accounts → New token

Alternatively, create a **Grafana Cloud Access Policy token** at [grafana.com/orgs/garethhailes/access-policies](https://grafana.com/orgs/garethhailes/access-policies) scoped to each specific stack. Your existing `terraform-automation-policy-gcx` policy already exists — you could add a new token under it, or create a separate per-stack policy for the LLM.

---

### Step 2 — Configure `gcx` contexts

`gcx` uses a named-context config model. Run this once per stack:

```bash
# Production stack
gcx config set contexts.fitfileprod.grafana.server https://fitfileprod.grafana.net
gcx config set contexts.fitfileprod.grafana.token <your-fitfileprod-service-account-token>

# Test stack
gcx config set contexts.fitfiletest.grafana.server https://fitfiletest.grafana.net
gcx config set contexts.fitfiletest.grafana.token <your-fitfiletest-service-account-token>
```

No `org-id` needed — that's only required for OSS/Enterprise instances. Grafana Cloud stacks don't need it.

To set a **default context** (so bare `gcx` calls go to one stack by default):

```bash
gcx config set current-context fitfiletest
```

---

### Step 3 — Alternative: `gcx login` (browser OAuth)

Your memory shows you previously tried `gcx login --context fitfiletest` and it presented the OAuth vs service-account-token choice but you aborted. For interactive use, this path works:

```bash
gcx login --context fitfileprod
gcx login --context fitfiletest
```

Choose **Auth (browser)** — it opens a browser, authenticates via Microsoft SSO (which is how your Grafana Cloud org is linked), and stores tokens in the config. **Caveat from the docs:** after OAuth login, `cloud.stack` and `cloud.api-url` may not be populated for non-prod stacks — verify with `gcx config view` and patch manually if missing.

---

### Step 4 — Verify both stacks

```bash
# Check config is correct
gcx config check

# List dashboards on prod
gcx --context fitfileprod dashboards list

# List dashboards on test
gcx --context fitfiletest dashboards list

# Query Loki datasources (you did this previously on fitfiletest)
gcx --context fitfiletest logs labels -d grafanacloud-logs --label cluster

# List datasources (returns UIDs for logs, prom, etc.)
gcx --context fitfiletest api /api/datasources
gcx --context fitfileprod api /api/datasources
```

Your memory from May 1 shows this validation worked on `fitfiletest`, confirming:
- `grafanacloud-fitfiletest-logs` → `grafanacloud-logs`
- `grafanacloud-fitfiletest-prom` → `grafanacloud-prom`

---

### Step 5 — Expose both contexts to your LLM

For your LLM to read from **both** stacks, give it both context names. The `--context` flag works per command:

```bash
gcx --context fitfileprod stacks list
gcx --context fitfiletest metrics query --expr 'up' -d grafanacloud-prom
```

Or set `GCX_AGENT_MODE=1` (auto-detected from `CLAUDECODE`, `CURSOR_AGENT`, etc.) for JSON output with no colour, which is easier for an LLM to parse:

```bash
export GCX_AGENT_MODE=1
gcx --context fitfileprod dashboards list
```

---

### Gotcha to watch for

From the docs (cross-referenced with your history): if you used `gcx login` to set up `fitfiletest` and the OAuth path was used, run `gcx config view` to confirm `cloud.stack` is populated. If it's missing, set it manually:

```bash
gcx config set contexts.fitfiletest.cloud.stack fitfiletest
gcx config set contexts.fitfileprod.cloud.stack fitfileprod
```

This is needed for Cloud-specific subcommands like `gcx stacks`, `gcx slo`, and `gcx synthetic-monitoring`.

## Asset 4 (Pieces: ab317018-890b-47e2-ae7b-7ca195f6118a)
*Captured: 2026-05-19T08:58:11.982450Z*

The final pagination pages have returned — both are now `sufficient` or only repeating known content. The `gcx login` page surfaced the same `fitfiletest` context attempts seen earlier plus some unrelated results; no new stack URLs, token names, or config details appeared that weren't already captured.

---

## `gcx` Setup & Authentication Guide for Your Two Grafana Stacks

Here's the complete, grounded guide tailored to your environment.

---

## Your stacks

From your Grafana Cloud portal ([grafana.com/orgs/garethhailes](https://grafana.com/orgs/garethhailes)):

| Context name | Stack URL |
|---|---|
| `fitfiletest` | `https://fitfiletest.grafana.net` |
| `fitfileprod` | `https://fitfileprod.grafana.net` |

Your org is **FITFILE** (`garethhailes`), on **Grafana Cloud Pro**, cluster `prod-gb-south-0` (GCP europe-west2).

---

## Step 1: Create service account tokens for each stack

Your memory shows you already have an **Access Policies** setup at [grafana.com/orgs/garethhailes/access-policies](https://grafana.com/orgs/garethhailes/access-policies), including a dedicated `gcx` policy (`terraform-automation-policy-gcx`, ID `fd0b4719-f6a3-49b6-815b-7742e5f95642`).

For LLM/agent use, **service account tokens are the right auth method** — not browser OAuth (which you saw abort in your terminals on 12 May). Here's how to generate one per stack:

1. Go to each stack's Grafana UI:
    - `https://fitfiletest.grafana.net` → **Administration → Service accounts → Add service account**
    - `https://fitfileprod.grafana.net` → same path
2. Grant it the **Viewer** role (read-only for your LLM use case) or **Admin** if you need write access.
3. Click **Add service account token** → copy the token value. Store both securely (1Password is your vault of choice).

---

## Step 2: Register the two contexts in `gcx`

There are two methods. **Method A (browser OAuth)** is what you've been attempting — it works interactively but has been aborting for you. **Method B (explicit token config)** is the stable path for agent/LLM use.

### Method B — explicit config (recommended for LLM access)

```bash
# --- fitfiletest context ---
gcx config set contexts.fitfiletest.grafana.server https://fitfiletest.grafana.net
gcx config set contexts.fitfiletest.grafana.token <your-fitfiletest-service-account-token>

# --- fitfileprod context ---
gcx config set contexts.fitfileprod.grafana.server https://fitfileprod.grafana.net
gcx config set contexts.fitfileprod.grafana.token <your-fitfileprod-service-account-token>

# Set one as the default (optional)
gcx config set current-context fitfiletest
```

### Method A — browser OAuth (interactive, if you prefer it)

```bash
# For fitfiletest
gcx login --context fitfiletest
# Select "OAuth (browser)" when prompted
# Browser will open → authenticate with your Microsoft account
# (Grafana Cloud is linked to Microsoft SSO for your org)

# For fitfileprod
gcx login --context fitfileprod
```

> **Note from your history:** You ran `gcx login --context fitfiletest` multiple times on 12 May (Zellij session `mellifluous-river`) and it aborted at the auth method prompt. If the browser flow keeps failing, fall back to Method B with a service account token.

---

## Step 3: Verify both stacks are reachable

```bash
# Check current config
gcx config view

# Test fitfiletest
gcx --context fitfiletest stacks list

# Test fitfileprod
gcx --context fitfileprod stacks list

# Or query datasources directly (confirms API connectivity)
gcx --context fitfiletest api /api/datasources
gcx --context fitfileprod api /api/datasources
```

From a prior validation run in your memory (1 May, Zellij session `chatty-capsicum`), the `fitfiletest` stack returned these datasource UIDs when queried:
- `grafanacloud-fitfiletest-logs` → UID `grafanacloud-logs`
- `grafanacloud-fitfiletest-prom` → UID `grafanacloud-prom`

---

## Step 4: Give your LLM access to both stacks

For an LLM (agent mode), pass `--agent` or set `GCX_AGENT_MODE=true`. This switches `gcx` to JSON output with no colour — ideal for programmatic consumption:

```bash
# Agent-mode example: query logs on both stacks
GCX_AGENT_MODE=true gcx --context fitfiletest logs labels -d grafanacloud-logs --label cluster
GCX_AGENT_MODE=true gcx --context fitfileprod logs labels -d grafanacloud-logs --label cluster

# Or dashboards
GCX_AGENT_MODE=true gcx --context fitfiletest dashboards list
GCX_AGENT_MODE=true gcx --context fitfileprod dashboards list
```

---

## Access policy context

Your existing **Terraform Automation Policy** (`72ce4489-8442-47ad-b130-2aa7a3ecf3ba`) covers `garethhailes (all stacks)` with broad scopes including `stacks:read`, `stack-plugins:read`, `stack-service-accounts:write`. You could reuse a token from this policy for `gcx` if you don't want to create new service account tokens per-stack — just be aware it's a broad-permission token originally intended for Terraform automation.

---

## Current state issue

Your most recent `gcx` activity (today, session `tenacious-glockenspiel`, working in `CUH-DP`) shows `gcx` errors alongside Terraform initialisation. If `gcx` is erroring in that context, it may be because no `fitfileprod`/`fitfiletest` context is configured for that Zellij session. Running the `gcx config set` commands above will persist the contexts to your config file globally.

## Asset 5 (Pieces: 6b5a24ff-c41d-43f8-b0af-6cde6f90ae79)
*Captured: 2026-05-19T08:59:16.683322Z*

Both cursors are now exhausted — `recommendation: sufficient` on the `gcx login` chain, and the credentials chain hit a circuit-breaker (too many similar calls, meaning the engine already has all the data it can provide).

No additional `gcx`-relevant details emerged from either final page — just Cloudflare DNS records and Vault auth debugging unrelated to the setup guide. The task is complete.

---

Here is the complete `gcx` setup guide, grounded in your actual stacks and access policies:

## Setting up and authenticating `gcx` for both FITFILE Grafana stacks

### Your stacks

You have two Grafana Cloud stacks under the **FITFILE** org (`garethhailes`):

| Context name | Stack URL | Purpose |
|---|---|---|
| `fitfileprod` | `https://fitfileprod.grafana.net` | Production |
| `fitfiletest` | `https://fitfiletest.grafana.net` | Testing / Non-prod |

---

### Step 1 — Authenticate each stack

The `gcx login` command offers two methods. Your memory shows you've already attempted this with `--context fitfiletest` and seen the interactive prompt:

```bash
# For the test stack
gcx login --context fitfiletest
```

When prompted, choose either:
- **OAuth (browser)** — recommended for Cloud stacks; opens a browser window linked to your Microsoft SSO (how FITFILE Grafana Cloud auth is configured)
- **Service account token** — more stable for automation; requires a token with appropriate permissions

Repeat for prod:

```bash
gcx login --context fitfileprod
```

---

### Step 2 — Configure contexts via service account tokens (recommended for LLM use)

For an LLM agent to reliably read both stacks without browser flows, use **service account tokens**. Your Grafana Cloud org already has structured access policies at [grafana.com/orgs/garethhailes/access-policies](https://grafana.com/orgs/garethhailes/access-policies) including:

- **Terraform Automation Policy** (`72ce4489-8442-47ad-b130-2aa7a3ecf3ba`) — realm: all stacks, broad scopes
- **terraform-automation-policy-gcx** (`fd0b4719-f6a3-49b6-815b-7742e5f95642`) — a `gcx`-specific policy already exists
- **Production Grafana Agent Write OBS Policy** (`1baf5dd2-ac74-430d-b5c7-261fd6f7d606`)
- **Non Production Grafana Agent Write OBS Policy**

For read-only LLM access, the cleanest approach is to create a new token under the existing `terraform-automation-policy-gcx` policy, or create a dedicated read-scoped access policy. Then configure both contexts:

```bash
# fitfiletest context
gcx config set contexts.fitfiletest.grafana.server https://fitfiletest.grafana.net
gcx config set contexts.fitfiletest.grafana.token <your-fitfiletest-service-account-token>

# fitfileprod context
gcx config set contexts.fitfileprod.grafana.server https://fitfileprod.grafana.net
gcx config set contexts.fitfileprod.grafana.token <your-fitfileprod-service-account-token>

# Set fitfiletest as default (since that's what you've been working with)
gcx config set current-context fitfiletest
```

---

### Step 3 — Verify both stacks

```bash
# Verify test stack
gcx --context fitfiletest stacks list

# Verify prod stack
gcx --context fitfileprod stacks list

# Check datasources on test (confirmed working from your prior session)
gcx --context fitfiletest api /api/datasources
```

Your memory from 1 May 2026 (Zellij session `chatty-capsicum`) shows these datasource UIDs on `fitfiletest` that are already confirmed working:

- `grafanacloud-fitfiletest-logs` → UID `grafanacloud-logs`
- `grafanacloud-fitfiletest-prom` → UID `grafanacloud-prom`

```bash
# Query labels on test (confirmed working)
gcx --context fitfiletest logs labels -d grafanacloud-logs --label cluster
```

---

### Step 4 — Using both stacks from an LLM agent

To give your LLM read access to both stacks, expose the context flag in your tool configuration or system prompt. Example pattern:

```bash
# Query logs from test
gcx --context fitfiletest logs query '{cluster="testing"}'

# Query metrics from prod
gcx --context fitfileprod metrics query 'up{job="alloy"}'

# List dashboards on either stack
gcx --context fitfiletest dashboards list
gcx --context fitfileprod dashboards list
```

You can also set `GCX_AGENT_MODE=true` (or `--agent` flag) to get clean JSON output suitable for LLM consumption.

---

### Known issue to be aware of

From the `gcx` GitHub issue tracker: `gcx login` against Cloud stacks sometimes does **not** populate `cloud.stack` and `cloud.api-url` in the config. If you hit this, manually set them after login:

```bash
gcx config set contexts.fitfiletest.cloud.stack fitfiletest
gcx config set contexts.fitfileprod.cloud.stack fitfileprod
```

---

### Where to get service account tokens

Go to [grafana.com/orgs/garethhailes/access-policies](https://grafana.com/orgs/garethhailes/access-policies) → click **Add token** on either the existing `gcx` policy or a new read-scoped policy you create — scopes needed for LLM reads: `metrics:read`, `logs:read`, `traces:read`, `dashboards:read`, `datasources:read`.
