---
aliases: []
tags: []
title: "GitHub - GMaN1911/claude-cognitive: Working memory for Claude Code - persistent context and multi-instance coordination"
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2026-01-03T08:59:30+00:00
modified: 2026-01-03T10:19:48+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

# GitHub - GMaN1911/claude-cognitive: Working memory for Claude Code - persistent context and multi-instance coordination

![rw-book-cover](https://opengraph.githubassets.com/e5d6304ea69fee0a0ce49ef2efe41440291497646fa214626ac6e9e94fc6c1e6/GMaN1911/claude-cognitive)

## Metadata

- Author: [[https://github.com/GMaN1911/]]
- Full Title: GitHub - GMaN1911/claude-cognitive: Working memory for Claude Code - persistent context and multi-instance coordination
- Category: #articles
- Summary: Claude Cognitive gives Claude Code persistent working memory so instances keep relevant files in context and avoid redoing work. It uses an attention-based Context Router (HOT/WARM/COLD file injection) and a Pool Coordinator to share multi-instance state. Results: big token savings, fewer hallucinations, and smoother long-running or multi-user workflows.
- URL: https://github.com/GMaN1911/claude-cognitive

## Full Document

### GMaN1911/claude-cognitive

main

Go to file

Code

Open more actions menu

### Claude Cognitive

>  Working memory for Claude Code—persistent context and multi-instance coordination

[![License: MIT](https://camo.githubusercontent.com/fdf2982b9f5d7489dcf44570e714e3a15fce6253e0cc6b5aa61a075aac2ff71b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4d49542d79656c6c6f772e737667)](https://opensource.org/licenses/MIT)

[![Status: Production](https://camo.githubusercontent.com/d5ac9a88c3f18f47070b4de8904f0e6de967909976858a049cc0576cc8b1e4df/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374617475732d50726f64756374696f6e2d677265656e2e737667)](https://github.com/GMaN1911/claude-cognitive/blob/main)

#### The Problem

Claude Code is powerful but stateless. Every new instance:

* **Rediscovers** your codebase from scratch
* **Hallucinates** integrations that don't exist
* **Repeats** debugging you already tried
* **Burns tokens** re-reading unchanged files

With large codebases (50k+ lines), this becomes painful fast.

#### The Solution

**Claude Cognitive** gives Claude Code working memory through two complementary systems:

##### 1. Context Router

**Attention-based file injection** with cognitive dynamics:

* **HOT** (>0.8): Full file injection - active development
* **WARM** (0.25-0.8): Headers only - background awareness
* **COLD** (<0.25): Evicted from context

Files **decay** when not mentioned, **activate** on keywords, and **co-activate** with related files.

##### 2. Pool Coordinator

**Multi-instance state sharing** for long-running sessions:

* **Automatic mode**: Detects completions/blockers from conversation (every 5min)
* **Manual mode**: Explicit `pool` blocks for critical coordination
* Works with persistent sessions (days/weeks), not just short bursts

#### Results

**Token Savings:**

* Cold start: **79%** (120K → 25K chars)
* Warm context: **70%** (80K → 24K chars)
* Focused work: **75%** (60K → 15K chars)

**Average: 64-95% depending on codebase size and work pattern.**

**Developer Experience:**

* ✅ New instances productive in **first message**
* ✅ Zero hallucinated imports/integrations
* ✅ No duplicate work across 8+ concurrent instances
* ✅ Persistent memory across days-long sessions

**Validated on:**

* 1+ million line production codebase (3,200+ Python modules)
* 4-node distributed architecture
* 8 concurrent Claude Code instances
* Multi-day persistent sessions

#### Quick Start

##### 1. Install Scripts

```
# Clone to your home directory
cd ~
git clone https://github.com/GMaN1911/claude-cognitive.git .claude-cognitive

# Copy scripts
cp -r .claude-cognitive/scripts ~/.claude/scripts/

# Set up hooks (adds to existing config)
cat .claude-cognitive/hooks-config.json >> ~/.claude/settings.json
```

##### 2. Initialize Your Project

```
cd /path/to/your/project

# Create .claude directory
mkdir -p .claude/{systems,modules,integrations,pool}

# Copy templates
cp ~/.claude-cognitive/templates/* .claude/

# Edit .claude/CLAUDE.md with your project info
# Edit .claude/systems/*.md to describe your architecture
```

##### 3. Set Instance ID

```
# Add to ~/.bashrc for persistence:
export CLAUDE_INSTANCE=A

# Or per-terminal:
export CLAUDE_INSTANCE=B
```

##### 4. Verify It's Working

```
# Start Claude Code
claude

# First message - check for context injection:
# Should see: "ATTENTION STATE [Turn 1]" with HOT/WARM/COLD counts

# Query pool activity:
python3 ~/.claude/scripts/pool-query.py --since 1h
```

##### 5. Customize Keywords (Optional, Recommended)

**The scripts work immediately with MirrorBot example keywords** (50-70% savings).

**For 80-95% savings:** Customize keywords to match your codebase.

**Quick customization:**

```
# Edit the keyword section
nano ~/.claude/scripts/context-router-v2.py

# See full guide:
cat ~/.claude-cognitive/CUSTOMIZATION.md
```

**Full setup guide:** [SETUP.md](https://github.com/GMaN1911/claude-cognitive/blob/main/SETUP.md) **Customization guide:** [CUSTOMIZATION.md](https://github.com/GMaN1911/claude-cognitive/blob/main/CUSTOMIZATION.md)

#### How It Works

##### Context Router

**Attention Dynamics:**

```
User mentions "orin" in message
    ↓
systems/orin.md → score = 1.0 (HOT)
    ↓
Co-activation:
  integrations/pipe-to-orin.md → +0.35 (WARM)
  modules/t3-telos.md → +0.35 (WARM)
    ↓
Next turn (no mention):
  systems/orin.md → 1.0 × 0.85 decay = 0.85 (still HOT)
    ↓
3 turns later (no mention):
  systems/orin.md → 0.85 × 0.85 × 0.85 = 0.61 (now WARM)

```

**Injection:**

* HOT files: Full content injected
* WARM files: First 25 lines (headers) injected
* COLD files: Not injected (evicted)

##### Pool Coordinator

**Automatic Mode:**

```
Instance A completes task
    ↓
Auto-detector finds: "Successfully deployed PPE to Orin"
    ↓
Writes pool entry:
  action: completed
  topic: PPE deployment to Orin
  affects: orin_sensory_cortex/
    ↓
Instance B starts session
    ↓
Pool loader shows:
  "[A] completed: PPE deployment to Orin"
    ↓
Instance B avoids duplicate work

```

**Manual Mode:**

```
```pool
INSTANCE: A
ACTION: completed
TOPIC: Fixed authentication bug
SUMMARY: Resolved race condition in token refresh. Added mutex.
AFFECTS: auth.py, session_handler.py
BLOCKS: Session management refactor can proceed
```

```

#### Architecture

```

claude-cognitive/

├── scripts/

│   ├── context-router-v2.py      # Attention dynamics

│   ├── pool-auto-update.py       # Continuous pool updates

│   ├── pool-loader.py            # SessionStart injection

│   ├── pool-extractor.py         # Stop hook extraction

│   └── pool-query.py             # CLI query tool

│

├── templates/

│   ├── CLAUDE.md                 # Project context template

│   ├── systems/                  # Hardware/deployment

│   ├── modules/                  # Core systems

│   └── integrations/             # Cross-system communication

│

└── examples/

    ├── small-project/            # Simple example

    ├── monorepo/                 # Complex structure

    └── mirrorbot-sanitized/      # Real-world 50k+ line example

```

**Hooks:**

* `UserPromptSubmit`: Context router + pool auto-update
* `SessionStart`: Pool loader
* `Stop`: Pool extractor (manual blocks)

**State Files:**

* `.claude/attn_state.json` - Context router scores
* `.claude/pool/instance_state.jsonl` - Pool entries

**Strategy:** Project-local first, `~/.claude/` fallback (monorepo-friendly)

#### Documentation

##### Concepts

* [Attention Decay](https://github.com/GMaN1911/claude-cognitive/blob/main/docs/concepts/attention-decay.md) - Why files fade
* [Context Tiers](https://github.com/GMaN1911/claude-cognitive/blob/main/docs/concepts/context-tiers.md) - HOT/WARM/COLD theory
* [Pool Coordination](https://github.com/GMaN1911/claude-cognitive/blob/main/docs/concepts/pool-coordination.md) - Multi-instance patterns
* [Fractal Documentation](https://github.com/GMaN1911/claude-cognitive/blob/main/docs/concepts/fractal-docs.md) - Infinite zoom strategy

##### Guides

* [Getting Started](https://github.com/GMaN1911/claude-cognitive/blob/main/docs/guides/getting-started.md) - First 15 minutes
* [Large Codebases](https://github.com/GMaN1911/claude-cognitive/blob/main/docs/guides/large-codebases.md) - 50k+ lines
* [Team Setup](https://github.com/GMaN1911/claude-cognitive/blob/main/docs/guides/team-setup.md) - Multiple developers
* [Migration](https://github.com/GMaN1911/claude-cognitive/blob/main/docs/guides/migration.md) - Adding to existing project

##### Reference

* [Template Syntax](https://github.com/GMaN1911/claude-cognitive/blob/main/docs/reference/template-syntax.md) - Markers and tags
* [Pool Protocol](https://github.com/GMaN1911/claude-cognitive/blob/main/docs/reference/pool-protocol.md) - Technical spec
* [Token Budgets](https://github.com/GMaN1911/claude-cognitive/blob/main/docs/reference/token-budgets.md) - Optimization guide

#### Use Cases

##### Solo Developer - Large Codebase

**Problem:** 50k+ line Python project, Claude forgets architecture between sessions

**Solution:**

* Context router keeps architecture docs HOT when mentioned
* Token usage drops 79% (120K → 25K chars)
* New sessions productive immediately

##### Team - Monorepo

**Problem:** 4 developers, each running Claude in different terminals, duplicate work

**Solution:**

* Each dev sets `CLAUDE_INSTANCE=A/B/C/D`
* Pool coordinator shares completions/blockers
* Zero duplicate debugging

##### Long-Running Sessions

**Problem:** Keep Claude open for days, it forgets what happened 2 days ago

**Solution:**

* Pool auto-updates write history continuously
* Context router maintains attention across days
* Temporal coherence preserved

#### Enterprise

Need multi-team coordination, compliance features, or custom setup?

**Contact:** [gsutherland@mirrorethic.com](mailto:gsutherland@mirrorethic.com)

**Services available:**

* Custom implementation for your codebase
* Team training and onboarding
* Integration with existing tooling
* Priority support and SLA

#### Roadmap

**v1.0 (Current - Production)**

* ✅ Context router with attention dynamics
* ✅ Pool coordinator (auto + manual)
* ✅ Project-local strategy
* ✅ CLI query tools

**v1.1 (Next)**

* Nemotron compression for pool summaries
* Semantic relevance (embeddings vs keywords)
* Auto-instance ID assignment
* Web dashboard (optional)

**v2.0 (Future)**

* Conflict detection (multiple instances, same file)
* Action confirmations (critical operations)
* Integration with ES-AC learning (context preferences)
* Oracle prediction (which files to pre-load)

#### Credits

**Built on production experience with:**

* 1+ million lines of production Python code across 3,200+ modules
* 4-node distributed architecture (Legion, Orin, ASUS, Pi5)
* 8+ concurrent Claude Code instances in daily use

**Created by:**

* Garret Sutherland, [MirrorEthic LLC](https://mirrorethic.com)

#### License

MIT License - see [LICENSE](https://github.com/GMaN1911/claude-cognitive/blob/main/LICENSE)

**Use it, modify it, ship it.**

#### Contributing

Issues and PRs welcome!

**Before submitting:**

1. Check [existing issues](https://github.com/GMaN1911/claude-cognitive/issues)
2. For features: Open issue first to discuss
3. For bugs: Include context router + pool logs

**Development:**

```

# Test locally

cd ~/your-project

export CLAUDE_INSTANCE=TEST

claude

# Check logs

tail -f ~/.claude/context_injection.log

python3 ~/.claude/scripts/pool-query.py --since 10m

```

**Questions?** Open an [issue](https://github.com/GMaN1911/claude-cognitive/issues)

**Updates?** Watch the [repo](https://github.com/GMaN1911/claude-cognitive) for releases
