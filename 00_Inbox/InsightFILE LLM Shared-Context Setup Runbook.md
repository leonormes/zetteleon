---
title: InsightFILE LLM Shared-Context Setup Runbook
type: note
permalink: llmeon/00-inbox/insight-file-llm-shared-context-setup-runbook
---

# InsightFILE — LLM Shared-Context Setup Runbook

**Target repo:** `/Volumes/DAL/Fitfile/gitlab/FITFILE/Application/InsightFILE`
**Audience:** an LLM coding agent (Claude Code, Cursor, Codex CLI, or Antigravity/Gemini) executing this plan step by step.
**Goal:** give every LLM assistant a consistent, top-down, cross-session understanding of this repo, using the patterns from the reference report (repo maps, LSP/graph tools, `AGENTS.md` convention, MCP memory) — layered correctly on top of Leon's existing global tooling rather than duplicating it.

---

## 0. Pre-flight findings (already confirmed — don't re-discover these)

An audit of the repo and the local machine found:

| Item | Status |
|---|---|
| Repo-root `AGENTS.md` / `CLAUDE.md` / `GEMINI.md` | **Do not exist yet** |
| `.gitignore` | Already contains `AGENTS.md` and `/.serena/project.yml` — **both are currently un-tracked/local-only** |
| `.serena/project.yml` | **Exists**, project already named `InsightFILE`, LSP backend, indexing whole repo root |
| `.claude/settings.local.json` | Grants `mcp__mcp-proxy__*` and a couple of `Bash` permissions — confirms this repo already talks to the MCP proxy |
| `~/.claude.json` (global) | Two MCP servers registered: `1mcp`, `semble` |
| `~/.cursor/mcp.json` (global) | Same `1mcp` (SSE, `?app=cursor`) + `semble` |
| `~/.claude/CLAUDE.md` and `~/.gemini/GEMINI.md` (global, chezmoi-managed) | **Identical** "Global LLM Rules" file — generic machine/behaviour rules, no project content. Says: *all* external tools (Jira, Confluence, Obsidian, Todoist, GitKraken, **memory**, **code analysis**) are exposed through **1MCP** at `http://127.0.0.1:3050/mcp?app=<client>` |
| Repo stack | Yarn 3 (Berry) TypeScript monorepo. `apps/`: `ffcloud`, `fitconnect`, `frontend`, `scheduler-service`, `tasks`, `workflows-api`. `packages/`: `service-common`, `types`, `graphql-mocks`, `mockrest`, `rest-scheduler`, `eslint-config`, `es-import-move`, `tsconfig-paths-references`. GraphQL + OpenAPI codegen, GitLab CI, Docker, ArgoCD/k8s local dev (`devspace.yaml`), Sonar, Renovate |

**Implication:** Leon already has the *global* cross-model rules file and an MCP aggregator (1MCP) solved. What's missing is entirely **repo-level**: a canonical project primer, the cross-tool include wiring, and turning the already-gitignored Serena/AGENTS.md setup into something the whole team (and every future session) actually shares via git.

---

## 1. Audit step (run this first, even though the table above is a starting point — confirm nothing has changed)

```bash
cd /Volumes/DAL/Fitfile/gitlab/FITFILE/Application/InsightFILE

# Any existing context files?
find . -maxdepth 2 -not -path "*/node_modules/*" -not -path "*/.git/*" \
  \( -iname "AGENTS.md" -o -iname "CLAUDE.md" -o -iname "GEMINI.md" -o -ipath "*cursor/rules*" -o -iname "*.mcp.json" \)

# Serena state
cat .serena/project.yml | head -20
ls .serena/memories 2>/dev/null   # any memories already written for this project?

# What's gitignored that shouldn't be, for a *shared* context setup
grep -iE "claude|serena|cursor|agents|gemini|mcp" .gitignore

# Confirm 1MCP is actually reachable and see what it proxies
curl -s http://127.0.0.1:3050/health | jq .servers

# Confirm Serena is (or isn't) one of the proxied servers
curl -s http://127.0.0.1:3050/health | jq '.servers | keys' | grep -i serena
```

Decision output you need before continuing:
- **If Serena already appears behind 1MCP** → skip per-client Serena registration in Phase 4; just make sure InsightFILE is the *active* Serena project when working in this repo.
- **If not** → Serena needs to be registered directly as an MCP server for whichever client is in use (Claude Code / Cursor project-level `.mcp.json`), since it isn't reaching this repo through the proxy.

---

## 2. Write the canonical `AGENTS.md` (repo root)

This file must contain **only project-specific facts that the global chezmoi-managed rules don't already cover** — do not repeat behaviour/output rules from `~/.claude/CLAUDE.md` / `~/.gemini/GEMINI.md`, that would fight the single-source-of-truth goal.

Create `AGENTS.md` at repo root with these sections (fill in from `README.md`, `.gitlab-ci.yml`, `package.json`, and `docs/`):

```markdown
# InsightFILE — Agent Context

## Stack
- Yarn 3.8.7 (Berry) monorepo, managed via corepack. Node version pinned — check with `volta` / `.nvmrc` if present.
- TypeScript throughout. GraphQL + OpenAPI schemas (see `codegen.ts`, `codegen-ffcloud.ts`, `.graphqlrc.yml`, `redocly.yaml`).
- Apps (each built/run independently): `apps/ffcloud`, `apps/fitconnect`, `apps/frontend`, `apps/scheduler-service`, `apps/tasks`, `apps/workflows-api`.
- Shared packages: `packages/service-common` (build this first — other packages depend on it), `packages/types`, `packages/graphql-mocks`, `packages/mockrest`, `packages/rest-scheduler`, `packages/eslint-config`, `packages/es-import-move`, `packages/tsconfig-paths-references`.
- Datastores: MongoDB, MSSQL, PostgreSQL, Elasticsearch/OpenSearch, SpiceDB (see `scripts/run-*.sh`).
- Deploy: Docker (`Dockerfile.*` per service), GitLab CI (`.gitlab-ci.yml`), ArgoCD + k8s local dev via `devspace.yaml` / `devspace_start.sh`.

## Build / test / lint
- Install: `./scripts/yarn-config.sh && yarn install`
- Build shared lib first: `yarn workspace @fitfile/service-common build`
- Test: `yarn workspace @fitfile/<package-name> test`
- Lint: `yarn workspace @fitfile/<package-name> lint`
- Local run: `docker-compose up` from root, OR `scripts/run-dbs.sh` + `scripts/run-servers.sh` + frontends individually.

## Directory map
(Keep this brief — Serena's symbol index handles fine-grained navigation; this is only the top-level orientation.)
- `apps/*` — deployable services/frontends, one per subfolder.
- `packages/*` — shared libraries consumed via yarn workspaces.
- `deployment/` — CI/CD pipeline config.
- `docs/` — OpenAPI/GraphQL schema docs, Mesh sandbox setup, rate limiting.
- `scripts/` — local dev bootstrap (DBs, seeders, mesh mocks).

## Do-not-touch / high-risk areas
- Migration squashing (see README "Squashing migrations") — irreversible without the Azure Blob backup; never run outside the documented `dump-dbs.sh` flow.
- `GIT_AUTH_TOKEN` / `.yarnrc.yml` — do not commit tokens.
- Seed data changes go through the ArgoCD `seed-data` app, not manual DB edits.

## Known gotchas
- Yarn version mismatches between local and CI usually mean corepack isn't picking up the pinned version — re-run `scripts/yarn-config.sh`.
- Volta doesn't integrate with Corepack automatically — needs the manual `corepack enable --install-directory ~/.volta/bin` step (see README).

## Navigation tools available in this repo
- **Serena** (LSP-based symbol navigation) is already configured for this project — `.serena/project.yml`. Use `find_symbol` / `find_referencing_symbols` instead of guessing from raw text or grepping across `apps/*`.
- For a fast top-down orientation at the start of a new session, request a repo-map/outline pass before diving into a specific package (see Phase 6 of the setup runbook for how this is wired).
```

Cite real values pulled from the repo files, don't invent them — read `README.md`, `package.json`, `.gitlab-ci.yml` directly rather than guessing.

---

## 3. Wire the cross-model include pattern

Every assistant Leon runs needs to land on the same `AGENTS.md` without duplicating it:

- **Codex CLI**: reads `AGENTS.md` natively — no extra file needed.
- **Claude Code**: create repo-root `CLAUDE.md` containing only:
  ```
  @AGENTS.md
  ```
  (Use the `@file` include syntax, not a symlink — symlinked files have been reported to drop out after Claude's auto-compact, the `@include` reference survives it.) This *layers on top of* the existing global `~/.claude/CLAUDE.md`, it doesn't replace it.
- **Gemini CLI / Antigravity**: create repo-root `GEMINI.md`. Verify whether the installed Gemini CLI version supports the same `@AGENTS.md` include syntax; if not, mirror the content with a one-line note `"See AGENTS.md — kept in sync manually"` rather than diverging content. Check `~/.gemini/config/` for the actual mechanism in use (Antigravity is configured there per the global `GEMINI.md`).
- **Cursor**: Cursor does not always auto-load `AGENTS.md`. Add `.cursor/rules/agents.mdc` (or equivalent rule file for the installed Cursor version) with a one-line pointer/include to `AGENTS.md` so Cursor's rule engine picks up the same content.

---

## 4. Fix the git-ignore gap (this is the actual "shared context" blocker)

Right now `AGENTS.md` and `/.serena/project.yml` are in `.gitignore`, meaning nothing built in steps 2–3 would ever reach teammates or a fresh checkout — it'd stay a personal, local-only setup.

**Flag this explicitly before changing it** (it affects every contributor, not just Leon) — but the recommended change for "shared context" is:

```bash
# In .gitignore, remove/adjust these lines:
# AGENTS.md              <- remove: this should be committed and shared
# /.serena/project.yml   <- remove: this should be committed and shared

# Add instead (keep generated/session data out of git):
echo ".serena/cache/" >> .gitignore
echo ".serena/memories/*.local.md" >> .gitignore   # personal scratch memories only
```

Keep `.serena/memories/` itself trackable if the team wants durable architectural notes in git (see Phase 5) — only exclude clearly personal/scratch files.

Then:
```bash
git add AGENTS.md CLAUDE.md GEMINI.md .cursor/rules/agents.mdc .serena/project.yml .gitignore
git commit -m "chore(ai-context): add shared AGENTS.md primer and cross-model includes"
```

---

## 5. Confirm/finish the LSP tool (Serena)

1. Activate the project and let it build its symbol index:
   ```bash
   # from whichever client's Serena MCP tool, or the Serena CLI directly
   serena project activate InsightFILE   # or the equivalent MCP call
   ```
2. Run an initial onboarding pass so Serena writes baseline memories (architecture summary, module boundaries) into `.serena/memories/` — review them for accuracy before trusting them.
3. Confirm Serena is reachable from **every** client Leon actually uses on this repo:
   - If step 1's health check showed Serena behind 1MCP → nothing more to do, just make sure the InsightFILE project is active there.
   - If not → add a project-scoped `.mcp.json` (or the client-specific equivalent) registering Serena directly for this repo, mirroring how `1mcp` is already registered in `~/.cursor/mcp.json`.

---

## 6. Cross-session persistent memory (architectural decisions)

1MCP already proxies a generic **"memory"** server. Before adding a second memory system, check whether it's project-scoped:
```bash
curl -s http://127.0.0.1:3050/health | jq '.servers.memory'
```
- **If it supports per-project namespacing** → use it for InsightFILE-specific decisions (bug root causes, architectural rationale), tagging entries with `project: InsightFILE` so they don't blend with Leon's personal/other-project memories.
- **If it's global/unscoped only** → use Serena's own `.serena/memories/*.md` files as the project-scoped decision log instead (already file-based, git-trackable, and inspectable — consistent with how Claude Code itself prefers markdown memory over vector stores). Commit the durable ones per Phase 4.

Either way, document which one is canonical inside `AGENTS.md` so every assistant knows where to read/write decisions, rather than letting each tool default to a different store.

---

## 7. Repo map / RAG — only if actually needed

This repo is a multi-package monorepo but not exceptionally large, and Serena (graph/LSP-based) already gives precise symbol navigation, which is preferred over vector RAG for the reasons in the reference report (fewer hallucinations, no infra). **Do not stand up a vector DB by default.**

Instead:
- For a quick top-down primer at the start of a session, generate an outline/repo-map on demand (e.g. `aider --show-repo-map` or an equivalent outline tool) and paste it in — no persistent infra required.
- Only revisit a full embeddings/vector-RAG pipeline (Phase 7+) if the team later reports that "where is X logic?"-style discovery queries across `apps/*` are consistently painful even with Serena + `AGENTS.md` in place.

---

## 8. Nested `AGENTS.md` for high-complexity modules (incremental, not upfront)

Per the "evolve from friction points" convention, don't front-load nested files for every app/package. Start with none beyond root; add a nested `apps/<name>/AGENTS.md` only after the first time an assistant gets a module wrong (e.g. `ffcloud`, `fitconnect`, and `workflows-api` are the most likely candidates given their domain complexity). Each nested file should cover only what's different from the root file — module-specific conventions, external integrations, non-obvious contracts.

---

## 9. Verify end-to-end before calling this done

1. Open a fresh session in **two different clients** (e.g. Claude Code and Cursor) against this repo.
2. Confirm both surface the `AGENTS.md` content (ask each "what's the build command for service-common?" — it should answer correctly without you pasting anything).
3. Confirm both can call Serena's symbol tools (`find_symbol` on something in `packages/service-common`).
4. Write a throwaway note via the chosen memory mechanism (Phase 6) in one client, then confirm the other client can read it back in a new session.
5. Commit any fixes discovered during verification back into `AGENTS.md`/nested files.

---

## Summary checklist

- [ ] Re-run the Phase 1 audit and confirm findings still hold
- [ ] Write repo-root `AGENTS.md` with real project specifics (not duplicated global rules)
- [ ] Add `CLAUDE.md` (`@AGENTS.md` include), `GEMINI.md`, `.cursor/rules/agents.mdc`
- [ ] Un-ignore and commit `AGENTS.md` + `.serena/project.yml`; add scratch-memory ignores
- [ ] Confirm Serena is active and reachable from every client used on this repo
- [ ] Decide canonical memory store (1MCP `memory` vs Serena memories) and document it in `AGENTS.md`
- [ ] Skip vector RAG unless discovery pain is proven
- [ ] Add nested `AGENTS.md` only reactively, starting with `ffcloud`/`fitconnect`/`workflows-api` if needed
- [ ] Run the two-client verification pass and fix gaps found