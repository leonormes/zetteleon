---
created: 2026-04-19T11:53:23+00:00
modified: 2026-04-19T18:30:47+00:00
tags: [articles]
title: GitHub - RomyHaikgim Goal-in-Mind framework for deviation prevention and token usage reduction · GitHub
---

## GitHub - RomyHaik/gim: Goal-in-Mind Framework for Deviation Prevention and Token Usage Reduction · GitHub

![rw-book-cover](https://opengraph.githubassets.com/b789d067380dfaea31db2bfe28dd5e14f17adbab593bb7f57e8f8679fda48961/RomyHaik/gim)

### Metadata

- Author: [[https://github.com/RomyHaik/]]
- Full Title: GitHub - RomyHaik/gim: Goal-in-Mind framework for deviation prevention and token usage reduction · GitHub
- Category: articles
- Summary: GIM is a framework that captures project goals and reasons using a recursive WHY loop to prevent deviations and reduce token use. It passively evaluates tasks and requests against the goal, flagging issues like ambiguity or drift, and learns from user decisions to improve future calls. Claude Code integrates GIM smoothly with slash commands and auto-sync hooks to manage tasks and maintain alignment without manual CLI use.
- URL: <https://github.com/RomyHaik/gim>

### Full Document

#### RomyHaik/gim

main

Go to file

Code

Open more actions menu

#### GIM—Goal-in-Mind Framework

Why-oriented development for AI-assisted work.

GIM keeps your goal _and the reasons behind it_ in mind so you don't lose focus. A single orientation step distills your request into a goal plus the layered _why_, and from then on a passive evaluation loop watches the work for alignment, necessity, clarity, and intent—nudging only when something is off. Every resolution feeds back into GIM so the next call is smarter.

##### How it Works

```
 /gim-init                           Execution + passive loop
 ─────────                           ─────────────────────────
 capture request                     user works / runs tools
      │                                     │
      ▼                                     ▼
 extract goal (WHAT)              GIM passive evaluation
      │                             • alignment
      ▼                             • necessity
 recursive WHY loop                  • clarity
   ↻ infer next WHY                  • intent (when signal)
   ↻ stop when abstract /                   │
     low-novelty / ambiguous                ▼
      │                           issue?  ──no──> stay silent
      ▼                             │
 reason layers                      │ yes
   • operational (outcome)          ▼
   • strategic  (why it matters)   dispatch
   • confidence score                • ambiguity   → clarify
      │                              • drift       → nudge to goal
      ▼                              • overbuild   → simpler path
 propose GIM → user approves         • intent mismatch → surface pattern
      │                                    │
      ▼                                    ▼
 .gim.yaml + .gim/goal.md          user decision
      │                              • refocus   → aligned execution
      │                              • continue  → allow + optional
      └────────── execution ─────────          goal/mode update
                                                │
                                                ▼
                                       learning loop
                                       append rules/patterns
                                       back into GIM context

```

Orientation—`/gim-init` captures a freeform request, extracts the goal, and runs a bounded recursive WHY loop that stops when the next _why_ is too abstract, low-novelty, low-confidence, or spans multiple branches. The distilled result is three _reason layers_ (operational outcome, strategic motivation, confidence). You approve or edit, and GIM writes the goal + reasons to `.gim.yaml` and `.gim/goal.md`; the CLAUDE.md pointer ensures Claude loads them before substantive work.

Execution with a passive loop—while you work, GIM silently evaluates each request against the orientation. Four checks (alignment, necessity, clarity, intent) dispatch to four issue types (ambiguity, drift, overbuild, intent mismatch). No issue → silence. Issue → a targeted, minimal intervention.

Learning—how you resolve an intervention is itself data. A `--non-goal` or `--out-of-scope` resolution creates a boundary node; a `--override` creates a _rule_ node (`.gim/rules/rule-{id}.md`) that functions as a learned allowlist—the next request matching the same pattern passes without re-flagging.

Tool integration—external tools that generate artifacts (OpenSpec, task runners, spec writers, MCP servers) read the GIM context via `gim export` and can invoke the passive loop via `gim check --json`. See [Tool integration](https://github.com/RomyHaik/gim/#tool-integration) below for the contract.

##### Claude Code: Zero-friction Integration

`gim install claude-code` (project-level) ships three things and together they make Claude Code _adopt GIM's workflow_ without the user or Claude having to call the CLI manually:

1. Slash commands in `.claude/commands/`—`/gim-init`, `/gim-focus`, `/gim-check`, `/gim-goal`, `/gim-mode`, `/gim-scope`, `/gim-resolve`, `/gim-validate`, `/gim-brainstorm`.
2. CLAUDE.md pointer—a `<!-- GIM:START -->…<!-- GIM:END -->` block that tells Claude the vault is the source of truth and routes project-scoped facts to GIM instead of Claude's auto-memory.
3. Auto-sync hooks in `.claude/settings.json` + `.claude/hooks/`—two `PreToolUse` hooks the Claude Code harness runs on every relevant tool call:
	- TaskCreate mirror—every native `TaskCreate` also runs `gim task add`, so `.gim/tasks/` stays populated with a suggested token budget (computed from goal-relevance + mode + confidence). Claude keeps its in-session task UI; GIM owns the persistent record.
	- Auto-memory redirect—a `Write` to `~/.claude/projects/<slug>/memory/` with `type: project` frontmatter is intercepted; the content is redirected to `gim context add` (producing a `ctx-` node in `.gim/context/`) and the native write is denied with a reason string so Claude learns the redirect. User-/feedback-/reference-typed memory still passes through.

Net effect: once you run `gim install claude-code` in a project, tasks and project-typed auto-memory writes land in `.gim/` as a side effect of how Claude Code already works. Decisions, scope calls, overrides, and goal updates still go through explicit commands (`gim resolve`, `gim scope add-*`, `gim goal set`, `gim goal orient`)—either you or Claude invokes them, but the hooks don't auto-generate them.

For per-user global slash commands (no per-project hooks), run `gim install claude-code --global`.

##### Install

```
# From GitHub
npm install -g github:RomyHaik/gim

# Or clone locally
git clone https://github.com/RomyHaik/gim.git
cd gim && npm install -g .
```

##### Quick Start

###### 1. Initialize

Interactive orientation (recommended)—install the Claude Code slash commands first, then run `/gim-init` in a session. GIM captures your request, walks the recursive WHY loop, proposes reason layers (operational / strategic / confidence), and initializes the vault once you approve.

```
gim install claude-code     # one-time, per project
# then in Claude Code:
/gim-init launch working billing flow for SaaS users
```

One-shot CLI (scripting / CI / no LLM)—skip straight to a populated vault:

```
gim init --goal "Launch working billing flow" \
  --operational "Ship Stripe checkout behind the pricing page" \
  --strategic   "Validate the business model with paying signups" \
  --confidence  0.7
```

Either path creates the vault:

```
.gim/
  _index.md          # Graph index (auto-generated): goal, mode, stats, links
  goal.md            # Root node — description + reason layers
  mode.md            # Current operational mode
  tasks/             # Work items, auto-checked + auto-budgeted
  checks/            # Check results from the passive loop
  decisions/         # Resolution records
  boundaries/        # Non-goals + out-of-scope
  rules/             # Learned allowlist patterns (from --override)
  context/           # Domain knowledge, constraints

```

To refresh only the reason layers on an existing goal, run `gim goal orient --operational "…" --strategic "…" --confidence 0.85` (or use `/gim-init` again in a session).

###### 2. Add Tasks (auto-checked + auto-budgeted)

```
gim task add "set up Stripe SDK"
# Task added: set up Stripe SDK [active]
#   Budget: 2,500 tokens (suggested)
#   Why:    moderate goal link (relevance 0.50), focused-execution, confidence 0.70
#   File: .gim/tasks/task-m1abc.md

gim task add "build analytics dashboard"
# Task proposed: build analytics dashboard [proposed]
#   Flagged: drift
#   This is planned for v2 — we're in v0. "analytics dashboard"
#   Resolve: gim resolve chk-xxx --override | --non-goal | --out-of-scope
```

Every task creation does two things: the passive evaluation decides `active` vs `proposed`, and the budget estimator attaches a soft token budget computed from goal-relevance, mode, and confidence. The budget is a planning signal—it shows up in `gim task show`, `gim task list`, and `gim focus`, and is surfaced to the LLM via `CLAUDE.md`. Override with `--budget N` when you disagree:

```
gim task add "write Stripe checkout unit tests" --budget 1500
# Task added: write Stripe checkout unit tests [active]
#   Budget: 1,500 tokens (override; suggested 2,500)
```

Not a hard cap—an expectation-setter. Actual-vs-budget tracking is deferred to a later phase.

###### 3. Define Boundaries

```
gim scope add-non-goal "analytics dashboard" --reason "post-launch" --target-version v2
gim scope add-oos "custom payment processor" --reason "using Stripe"
```

Each boundary becomes a markdown node in `.gim/boundaries/` with a `parent: [[goal]]` edge and `learned-from: [[chk-xxx]]` when applicable.

###### 4. Run Checks

```
gim check "add Stripe checkout, retry queue, fallback system, and event-driven architecture"
# GIM Check: Overbuild  [chk-d4e5f6]
#   Issue: Bundles 4 items into one request — likely more than the goal requires right now.
#          "and" suggests scope beyond the goal's operational outcome.
#   Goal:  Launch working billing flow
#   Suggestion: Start with "add Stripe checkout" — smallest step toward
#               "Validate the business model with paying signups". Defer the rest.
#   Resolve: gim resolve chk-d4e5f6 --out-of-scope | --non-goal | --override
```

Five outcomes: `drift` (alignment fail—request doesn't serve the goal), `overbuild` (necessity fail—more than the goal requires right now), `ambiguity` (clarity fail—underspecified), `intent-mismatch` (intent fail—behavioural pattern suggests a non-goal driver), or `clear`.

###### 5. Resolve and Learn

```
# Narrow the learned boundary to just the off-goal parts:
gim resolve chk-d4e5f6 --out-of-scope "retry queue and fallback system"
# Learned as out-of-scope:
#   retry queue and fallback system
#   ID: oos-xxx
#   File: .gim/boundaries/oos-xxx.md
#   Decision: .gim/decisions/dec-xxx.md
```

Three learning paths on resolve:

- `--non-goal [description] [--target-version v2]` → creates a `.gim/boundaries/ng-{id}.md` (deferred feature).
- `--out-of-scope [description]` → creates a `.gim/boundaries/oos-{id}.md` (explicitly excluded).
- `--override` → creates a `.gim/rules/rule-{id}.md` (learned allowlist—a future request matching the same pattern short-circuits the passive loop to `clear`).

In every case, a `.gim/decisions/dec-{id}.md` records the resolution itself. Future checks for "retry queue" match the boundary instantly—the passive loop doesn't re-evaluate.

###### 6. See the Graph

```
gim graph tree
# goal.md — Launch billing flow [v0]
# ├── ○ task-m1abc.md  set up Stripe SDK
# │   └── chk-m1xyz.md  [clear]
# ├── ? task-m2def.md  build analytics dashboard
# │   └── chk-m2ghi.md  [drift]
# ├── NG →v2 ng-m3jkl.md  analytics dashboard
# └── OOS oos-m4mno.md  retry queue and fallback system

gim focus
# Goal: Launch billing flow
# Version: v0
# Mode: focused-execution
# Tasks: 1 active, 0 completed
#   · task-m1abc  set up Stripe SDK  — 2,500t
# Boundaries: 1 non-goals, 1 out-of-scope (1 learned)
# Vault: .gim/  •  index: .gim/_index.md
```

###### 7. Validate and Brainstorm

```
gim validate "add Stripe webhook handler"
# VALID    4/5 — Well-aligned

gim brainstorm "add payment receipt emails"
# Connections found:
#   [strong] Directly references goal concepts: payment, receipt
```

###### 8. Install into AI Tools

```
gim install claude-code            # project-level slash commands + auto-sync hooks
gim install claude-code --global   # available in all Claude Code sessions
gim install cursor                 # .cursorrules
gim install windsurf               # .windsurfrules
```

Claude Code auto-sync (project install only). `gim install claude-code` provisions two PreToolUse hooks in `.claude/settings.json` + hook scripts in `.claude/hooks/`. From then on, Claude Code populates GIM automatically:

- Every native TaskCreate silently mirrors into `.gim/tasks/` with a suggested token budget—no `gim task add` needed.
- Writes to `~/.claude/projects/<slug>/memory/` with `type: project` frontmatter are intercepted and redirected to `gim context add`, creating a `ctx-` node in `.gim/context/`. User/feedback/reference memory still lives in auto-memory.

Result: Claude Code adopts GIM's workflow without the user or Claude having to invoke the CLI manually. The global install (`--global`) only ships slash commands—hooks are project-scoped and git-tracked so teammates get the same auto-sync.

##### The Vault

Every node in `.gim/` is a `.md` file where:

- All data lives in YAML frontmatter—`type`, `id`, `description`, `tags`, and typed edges (`parent`, `resolves`, `learned-from`, `matched-non-goal`, etc.)
- Bodies are empty—keeps LLM token cost minimal when the vault is loaded into context
- Edges are wiki-link scalars (`[[goal]]`, `[[chk-xxx]]`)—queryable, traversable, first-class

###### `goal.md` And Reason Layers

The goal node carries the layered _why_ distilled from the `/gim-init` recursive WHY loop:

```
---
type: goal
version: v0
status: active
description: Launch working billing flow
operational-reason: Ship Stripe checkout behind the pricing page for the v0 launch
strategic-reason: Convert organic signups into paying customers to validate the business model
confidence: 0.7
criteria:
  - Users can subscribe to plans
  - Webhooks process payment events
---
```

The passive evaluation loop reads these layers to judge alignment (does a request serve the operational outcome?) and necessity (does it serve the strategic reason?).

###### File Types

| File | Location | Created by |
| --- | --- | --- |
| Goal | `.gim/goal.md` | `gim init` / `gim goal set` (reason layers via `/gim-init`) |
| Task | `.gim/tasks/task-{id}.md` | `gim task add` (auto-checked) |
| Check | `.gim/checks/chk-{id}.md` | `gim check` / task auto-check |
| Decision | `.gim/decisions/dec-{id}.md` | `gim resolve` |
| Non-goal | `.gim/boundaries/ng-{id}.md` | `gim scope add-non-goal` / learned |
| Out-of-scope | `.gim/boundaries/oos-{id}.md` | `gim scope add-oos` / learned |
| Rule | `.gim/rules/rule-{id}.md` | `gim resolve --override` (learned allowlist) |
| Context | `.gim/context/ctx-{id}.md` | `gim context add` |
| Index | `.gim/_index.md` | Auto-generated after every operation |
| Mode | `.gim/mode.md` | `gim mode set` |

###### Tag Hierarchy

```
gim/goal
gim/task
gim/check/{alignment,necessity,clarity,intent,clear}
gim/issue/{ambiguity,drift,overbuild,intent-mismatch}
gim/decision/{confirmed-non-goal,confirmed-out-of-scope,overridden,deferred}
gim/boundary/{non-goal,out-of-scope}
gim/context/{domain,technical,stakeholder,constraint}
gim/source/{manual,learned}
gim/status/{proposed,active,completed,rejected}

```

The four check types (alignment/necessity/clarity/intent) and four issue types (ambiguity/drift/overbuild/intent-mismatch) are the vocabulary of the passive evaluation loop. Old vaults with pre-v0.4 tags (`scope-creep`, `intent-drift`, `goal-misalignment`) are migrated on read—writes always use the new names.

###### The Why-graph

Every node's edges trace back to `goal.md`. Learned items preserve the full chain as first-class data: a fired check produces a decision, which produces either a boundary node (`.gim/boundaries/`) for `--non-goal` / `--out-of-scope` resolutions or a rule node (`.gim/rules/`) for `--override`. Use `gim graph tree` to walk the graph, or query the vault directly—every edge is a wiki-link scalar in frontmatter.

##### Config

`.gim.yaml` at your project root (minimal—the vault is the state):

```
version: v0
goal:
  description: "Launch working billing flow"
  reasonLayers:
    operational: "Ship Stripe checkout behind the pricing page"
    strategic: "Convert organic signups into paying customers"
    confidence: 0.7
  criteria:
    - "Users can subscribe to plans"
    - "Webhooks process payment events"
mode: focused-execution
```

##### CLI Commands

| Command | Description |
| --- | --- |
| `gim init --goal "…" [--operational … --strategic … --confidence 0..1]` | Initialize GIM vault (optionally with reason layers) |
| `gim goal set / show / orient` | Set goal, view goal, or update just the reason layers |
| `gim task add "…" [--budget N]` | Add a task (auto-checked + auto-budgeted; `--budget` overrides) |
| `gim task list / show / complete / reject` | Manage tasks (list + show display budgets) |
| `gim check "request"` | Run GIM checks |
| `gim resolve <id> --non-goal / --out-of-scope / --override` | Resolve a check, teach GIM |
| `gim scope show / add-non-goal / add-oos / remove` | Manage boundaries |
| `gim context add / list / remove` | Manage project context |
| `gim focus` | Show goal, version, mode, stats |
| `gim graph tree / stats` | View the knowledge graph |
| `gim validate "idea"` | Rate idea alignment 1-5 |
| `gim brainstorm "idea"` | Explore connections to the goal |
| `gim mode set / show / list` | Manage operational mode |
| `gim prompt system / claude-code / cursor` | Generate AI tool prompts |
| `gim install claude-code` | Install slash commands, CLAUDE.md pointer, and auto-sync hooks (project-level) |
| `gim install claude-code --global` | Install only slash commands, user-wide (no CLAUDE.md, no hooks) |
| `gim install cursor` / `gim install windsurf` | Write `.cursorrules` / `.windsurfrules` from the current orientation |
| `gim export [--pretty]` | Emit current orientation as JSON for external tools |
| `gim check --json --dry-run "…"` | Run the passive loop and return the result as JSON (no vault write) |

##### Tool Integration

External tools (OpenSpec, spec writers, task runners, MCP servers) hook into GIM through two stable surfaces. Both emit JSON and can be piped into any caller that speaks a shell.

###### 1. Read the orientation—`gim export`

```
gim export --pretty
```

Emits a versioned JSON payload (`schemaVersion: 1`) with the active goal, reason layers, mode, boundaries, and learned rules. Tools that generate artifacts should read this at the start of each run and include the relevant context in their output—typically the goal description plus the operational reason.

```
{
  "schemaVersion": 1,
  "version": "v0",
  "mode": "focused-execution",
  "goal": {
    "description": "Launch billing v0",
    "reasonLayers": {
      "operational": "Ship Stripe checkout behind the pricing page",
      "strategic": "Validate the business model with paying signups",
      "confidence": 0.7
    }
  },
  "boundaries": { "nonGoals": [...], "outOfScope": [...] },
  "rules": [...],
  "stats": { ... }
}
```

###### 2. Run the Passive Loop inline—`gim check --json`

```
gim check --json --dry-run "add retry queue, fallback system"
```

Returns one of five outcomes (`drift`, `overbuild`, `ambiguity`, `intent-mismatch`, `clear`) as a `CheckResult` JSON object. Use `--dry-run` inside generators so evaluation traffic doesn't pollute the vault; drop it when the user explicitly invokes a check and you want the result logged.

A tool generating, say, a spec file should run `gim check --json --dry-run` against each significant decision in the artifact and embed the result as an inline annotation or block comment. If any check returns a non-`clear` result, the tool should halt or flag before writing the artifact—the passive loop is the gate.

###### 3. Learn from Override

When a human reviewer overrides a flag your tool surfaced, call `gim resolve <check-id> --override` so the next generation skips the false positive. No additional hook is required.

##### Modes

| Mode | Scope sensitivity | When to use |
| --- | --- | --- |
| `focused-execution` | High—reject tangents | Heads-down building |
| `exploration` | Low—allow tangents | Investigating options |
| `planning` | Medium—flag ambiguity | Designing the approach |
| `review` | Medium—check completeness | Evaluating work done |
| `course-correction` | Low—goal is revisable | Adjusting direction |

##### Philosophy

Why-oriented development: every artifact traces back to the goal _and_ to the layered reason behind it—operational outcome, strategic motivation, confidence. Open any node in `.gim/` and its frontmatter tells you exactly why it exists and which of those layers it serves. The knowledge graph grows with your project: interventions become rules, resolved checks become boundaries, and the orientation sharpens every iteration—at minimal LLM token cost.

Three principles:

1. Keep the goal—and the why—in mind—every request is evaluated against a clear objective and the reasons it matters
2. Silent when clear—the passive loop only speaks up when alignment, necessity, clarity, or intent is off
3. Learn and evolve—resolutions become rules, checks become boundaries, the graph gets smarter

##### License

MIT
