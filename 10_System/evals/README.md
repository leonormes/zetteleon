---
title: README
type: note
permalink: llmeon/10-system/evals/readme
---

# ProdOS Evaluation & Regression Cases

Seed of the vault's evaluation layer, built 2026-09-14 as part of [[prodos-agent-architecture-upgrade]] (`30_Library/200_Projects/prodos-agent-architecture-upgrade.md`) — closing a gap identified against Meta's "organizational agents" four-layer pattern (knowledge / reasoning / evaluation / self-improvement). Before this, ProdOS had no accumulating eval corpus at all: TAC enforces per-response discipline, and `edge_lint.py`/`validate_note_frontmatter.py` are deterministic checks, but nothing tied a documented past failure to a stored, repeatable test.

Tooling fixtures/config, same category as `10_System/scripts/*.py` — not part of the typed knowledge graph (no `prodos.kind`, TAC's type-specific schemas don't apply, not meant to be linked from canonical notes). Obsidian's own automation stamps a minimal `title`/`type: note`/`permalink` frontmatter block onto any `.md` file it discovers (this README and the `behavioral/*.md` cases included) — that's cosmetic housekeeping, not this folder opting into note-graph status. `structural/*.yaml` cases are untouched by it, being non-Markdown.

## Two tiers — be honest about which one is actually automated

### `structural/` — deterministic, machine-run

Each `.yaml` case is a **self-contained fixture** (inline note content, no dependency on live vault content) plus an expected set of findings. Run all of them:

```bash
uv run --with pyyaml python3 10_System/scripts/edge_lint.py --regress
```

Exit code is non-zero if any case fails — safe to wire into CI or a pre-commit hook alongside `edge_lint.py`'s own `--audit`.

**Case format:**

```yaml
id: short-stable-id
title: One-line description of the invariant being protected
description: >
  Why this matters — which spec section it protects, what would silently
  break if the check regressed.
fixtures:
  - name: source.md          # first fixture is "primary" — lint_file() runs on it
    content: |
      ---
      title: ...
      type: claim
      tags: [test]
      conformant: true
      ---
      body content, e.g. an edge to test
  - name: dest.md             # optional — extra fixtures the primary can resolve against
    content: |
      ...
expect:
  - level: ERROR | WARN
    contains: "substring expected in the finding's message"
```

Matching is a strict one-to-one: every `expect` entry must match exactly one finding (same level, substring match), and no finding may go unmatched. The case fails — and `--regress` prints exactly what was missing or unexpected — if either side has leftovers.

**Add a case when:** a future edit to `edge_lint.py` could plausibly loosen or break a structural invariant you've already relied on (target resolution, vocabulary enforcement, bare-link detection, etc.).

### `behavioral/` — documented only, not machine-run

Judgment-quality cases — did the agent pick the right recipe, ask before deciding something that needed a human, correctly classify an inbox capture as non-authoritative. Nothing in this vault can mechanically grade these yet (that would need an LLM-judge harness, which is future work, not built here). Each case is a plain `.md` file: what happened, why it was wrong, what the correct behaviour looks like. Treat these as a **manual review checklist** for now — read them before starting a `Recipe: Diagnose a failure` pass, and before trusting an agent to self-assess its own prior output.

**Add a case when:** a human correction reveals a recurring category of agent mistake — see [[Protocol - Diagnose an Agent Failure]] for the root-cause taxonomy to classify it against first.

## What this is not (yet)

- Not CI-wired. Nothing currently runs `--regress` automatically on a commit or a schedule — that's a reasonable next step once the structural corpus has more than 3 cases, not done here.
- Not a frontmatter-conformance regression suite. `validate_note_frontmatter.py` (`10_System/scripts/validate_note_frontmatter.py`) is a second real deterministic validator that could grow its own case format the same way — out of scope for this pass, flagged so it isn't forgotten.
- Not model-graded. `behavioral/` cases are read by a human or by an agent doing a diagnose-a-failure pass, not scored automatically.