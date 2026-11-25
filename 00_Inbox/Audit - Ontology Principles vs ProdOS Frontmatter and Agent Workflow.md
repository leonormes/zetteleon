---
title: Audit - Ontology Principles vs ProdOS Frontmatter and Agent Workflow
type: link_report
status: seed
conformant: true
created: 2026-11-25 10:00:00+00:00
modified: 2026-11-25 10:00:00+00:00
tags:
- domain/pkm
- topic/knowledge-architecture
- audit
permalink: llmeon/00-inbox/audit-ontology-principles-vs-prod-os-frontmatter-and-agent-workflow
---

## Audit - Ontology Principles vs ProdOS Frontmatter and Agent Workflow

Read-only audit run 2026-11-25 against five principles taken from Frank Coyle's talk "Why Agentic Systems Need Ontologies", as summarised in the request. The talk itself was not read, so the principles are the requester's summary. Items 1 and 2 of the recommendations were implemented the same day (see the last section).

Scope read: [[AGENTS.md]], [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]], [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]], [[SoT - Atomic Note Standard (The Proposition Card)]], `edge_lint.py`, both validators, the pre-commit hook, [[00 - Prompt Library Router]], and three loop-bearing prompts (Orphan Triage Sweep, Frontmatter Bulk Migration, Vault Graph Programme driver). The other `type/system` prompts were not read.

### Executive summary

The vault is stronger than a generic ontology approach on belief revision and human control, and weaker on one point: the deterministic gates were not running.

- **Stronger:** closed vocabularies, a ratchet with a `conformant: false` escape hatch, dated positions and `revises`, `own_words` protection, and prompts that stop for a yes.
- **Biggest gap (confidence: high):** git's `core.hooksPath` pointed at `~/.config/git/hooks`, whose hook never calls the vault's own `.git/hooks/pre-commit`. Commits succeeded while edge lint reported 4 errors.
- **Smaller gaps:** no domain/range typing of edges, protected-note rules enforced only in prose, and enums repeated across several files.

### Gap and strength matrix

| Principle | Current behaviour | Gap or advantage | Risk |
|---|---|---|---|
| 1. Neurosymbolic guardrails | LLM proposes; three scripts check type, status, `epistemic_status`, edge vocabulary, strength 1-5, dangling targets, cycles, SoT embeds | Advantage in the checks. Gap: nothing forced them to run | High |
| 2. Boundary typing and state validation | Validators run after the write; AGENTS.md 7.2 asks agents to run them | Relied on the agent remembering. No single command for all gates | Medium |
| 3a. Closed enums | `type` (16), `status` (5), `epistemic_status`, relations (7), `confidence` | Advantage. Each stated in 3-4 places; only `status` has a single source | Medium |
| 3b. Domain/range | `edge_lint.py` checks vocabulary, strength, resolution only | Gap: `synthesizes` should start only from an SoT, `contradicts` should join claims | Medium |
| 3c. Cardinality | List versus scalar checked; `superseded_by` required when superseded | Reciprocity of `supersedes` and `superseded_by` unchecked | Low-medium |
| 3d. Disjointness | `type` is one value; `status` and `prodos.lifecycle` overlap on `evergreen` | Title prefix versus `type` unchecked | Low |
| 4. Bounded loops | Orphan cron: 10 notes a day, max 2 UNSURE, stops at empty queue. Migration starts with a dry run. Session driver does one task per yes | Advantage where present. No vault-wide cap on validator-fix retries | Medium |
| 4b. Side-effect hygiene | Drafts go to `00_Inbox/` with `conformant: false`; promotion is human | Advantage | Low |
| 5. Reuse and scope | Typed-edge note rejects JSON-LD on purpose; Dataview, K-Plex and Metadata Menu reused | Advantage | Low |
| Protected notes | `own_words` and folder rules are prose only; no script or hook mentions `own_words` | Compliance relies on agent discipline | Medium-high |

### Recommended improvements, in priority order

1. **Make the gates fire.** Point this repo at a versioned hooks directory that also runs the global secret-scan hook. Check: a staged note with a dangling edge must fail the commit. Done 2026-11-25.
2. **One `check_all.py` over changed files**, covering frontmatter, shape, edges and status drift. Check: it exits non-zero when any single gate is seeded to fail. Done 2026-11-25.
3. **Extend `status.yaml` into a schema directory** holding `type`, `epistemic_status` and the relation vocabulary, read by the scripts, with the drift check covering all of them. Check: no enum literals remain in the three scripts.
4. **Edge domain/range table as warnings**, seven rows at most. Count violations first; promote to errors for new notes only. Check: the report lists real violations, not noise.
5. **Protected-note check in the gates.** Fail when a diff changes the body of a note with `own_words: true`, or an existing file under `01_journals/` or `20_Thinking/`, unless an override is set. Check: a staged body edit to a `20_Thinking` note fails.
6. **Two cheap consistency checks:** `supersedes`/`superseded_by` reciprocity, and title prefix against `type`.
7. **Run budget in the router's cross-cutting rules:** a maximum note count per run and at most 3 validator-fix retries, then stop and report.

### What to skip

- OWL, RDF or SHACL reasoners: seven relations and five enums do not need description-logic inference, and `edge_lint.py --audit` already covers justification gaps and cycles.
- JSON-LD or a triple store: rejected on purpose in the typed-edge note.
- Pydantic models: the contract changelog records that earlier Pydantic claims were false and removed.
- A runtime proxy validating every MCP write: the post-write checks plus working gates are enough at this scale.
- A formal ontology of GTD or ADHD concepts: the Proposition Card plus typed edges already carries it.
- Cardinality rules beyond list versus scalar, and embedding-based classification.

### Implemented 2026-11-25 (items 1 and 2)

- `10_System/scripts/check_all.py`: runs the gates over changed notes. Frontmatter is enforced for new notes only, shape for in-scope atomic notes, edge lint fails only on ERRORs in changed notes, and the status drift check is vault-wide.
- `10_System/hooks/pre-commit` chains the global secret-scan hook. `10_System/hooks/commit-msg` runs `check_all.py --staged`, and exempts commits whose message starts with "vault backup:".
- `git config core.hooksPath 10_System/hooks` was set in this repo's local config. It is not versioned, so a fresh clone needs the same command.
- Tested with a seeded note carrying a dangling edge and an invalid status: the gate failed, and a clean tree and a backup-style message both passed.
- Not covered: the quote gate (`verify_quote.py`) needs a Calibre id, so it stays manual. `shale precommit` is not wired into either hook.