---
title: 'HEAD Ingest Routing — three workbench captures routed into the LLM graph'
output_type: report
created: 2026-07-27 17:45:00+01:00
tags:
- output
- domain/llm
- topic/knowledge-graph
- ingest-routing
permalink: llmeon/output/2026-07-27-report-head-ingest-routing
---

> **Output Contract:** [[Protocol - Typed Answer Contract (TAC) for Vault Agents]].
> **Write scope:** `raw/` (append-only, §1), `raw/proposed-claims/` (§2.4), `wiki/` (§1), `output/` (§2.3). **No writes to `20_Thinking/` or `30_Library/`.** Zero typed edges written — see §5 for why.
> **Tooling tier: 3 (filesystem).** `obsidian-mcp-tools` unreachable; lexical matching only. `WebSearch` used for source corroboration.

## Verdict

Three HEADs in, and they are **not** of equal value. One is a substantial, independently-corroborated protocol change that materially affects a live project of yours. One contains a single new idea wrapped in a product listicle. One is a launch PR piece whose numbers trace to a single CEO interview.

Routed accordingly: **3 raw captures · 4 claim stubs · 1 wiki dossier substantially updated · 0 typed edges.**

The zero is deliberate and is the most informative number in this report. See §5.

---

## 1 · Classification

| HEAD | Corroboration | Verdict | Routed to |
|---|---|---|---|
| **MCP's biggest update removes the machinery many servers were built around** (The New Stack) | **HIGH** — confirmed against the official MCP blog, the spec changelog, and four independent write-ups. SEP numbers check out. | Substantial. Refines three existing MCP notes and **invalidates a live project's root cause**. | 1 raw capture · 3 stubs · wiki dossier |
| **5 Claude, OpenClaw and Hermes skills…** (MakeUseOf) | **LOW** — consumer listicle, affiliate framing, product claims unevidenced. | Mostly duplicate. One genuinely new claim. | 1 raw capture · 1 stub |
| **"Developers see this as the future": Pilot Protocol…** (The New Stack) | **LOW** — every figure traces to one interview with the CEO on launch day. | Watch, don't promote. | 1 raw capture with trust warning · **no stub** |

### Why the Pilot piece got no claim stub

Search on 2026-07-27 found no independent corroboration: only this article syndicated elsewhere, the vendor's own site, two GitHub repos of the same name under different owners, and `draft-teodor-pilot-protocol-01` — an **IETF individual draft**, which is a personal submission, not a working-group product. The 250,000 agents and 2 billion requests/day are CEO-sourced and unverified.

Three things in it warrant scepticism rather than extraction, and they're recorded in the raw capture:

1. **"Most without their owners' knowledge"** is presented as a growth metric. It describes autonomous agents transacting, spending from wallets and installing software without the awareness of the humans accountable for them.
2. **The security argument is a non-sequitur.** *"The one-line install has zero dependencies, so developers can send their agents off to market in the knowledge that they won't come home with some spurious Trojan horse."* A piped-shell installer is the canonical supply-chain risk pattern, not a defence against it. Zero dependencies bounds transitive risk; it says nothing about the installer.
3. **"100% of the developers he talks to"** — selection bias stated as a statistic.

AGENTS.md §6 and the vault's own discipline both apply: *do not treat blog popularity as truth.* The underlying *pattern* — agent-to-agent discovery and machine-to-machine payment as a substrate — is a real question the vault has no node for, and it's flagged in §4 as a tension worth recording. The vendor's numbers are not.

---

## 2 · Written to `raw/` (source captures, append-only)

| File | Contents |
|---|---|
| `raw/2026-07-27-thenewstack-mcp-spec-rewrite.md` | Claims grouped by removals / rationale / replacement mechanism / gateways / caching / governance / migration cost, with the stated caveats quoted rather than paraphrased. Corroboration note at the top. |
| `raw/2026-07-27-makeuseof-agent-skill-portability.md` | Two structural observations extracted; product recommendations deliberately **not** extracted. Explicit section listing what is already held in the vault. |
| `raw/2026-07-27-thenewstack-pilot-protocol.md` | Vendor claims recorded and labelled as such, plus a Reviewer Flags section. Trust warning callout in frontmatter and body. |

Every downstream claim below cites one of these. Nothing was asserted without a `raw/` citation.

---

## 3 · Written to `raw/proposed-claims/` (4 stubs, §2.4)

Ranked. If you only promote one, promote the first.

**1 · Protocol-level statelessness relocates agent state into explicit handles the model can reason about**
The strongest of the four. The source is explicit that the significance isn't only operational: *"Session state hidden in transport metadata was something the model could never reason about, whereas a handle in a tool result can be composed across tools and handed between workflow steps."* This is the same move as [[Targeting LLM Attention Requires Encoding Relevance as Structure]] in a different domain — make the thing structural and visible rather than hidden and searched-for. **Promoting this gives the LLM cluster a genuine, non-circular graph node.**

**2 · Operation-level protocol headers let a gateway authorize agent traffic without parsing request bodies**
Supports an existing claim. `Mcp-Method`/`Mcp-Name` headers lower the cost of exactly the governance layer [[Enterprise Agentic Systems Require Containerised Gateways with OAuth and RBAC]] argues for. Includes the source's own precondition — the backend must reject any header disagreeing with the body, or the header is a spoofable façade.

**3 · Deprecating client-mediated sampling converts tool servers into credential holders, billing parties and data processors**
The one with the sharpest consequences for your NHS-adjacent work. *"A server using client-mediated Sampling needed no provider credentials and generally did not carry the model bill."* The third role — separate processor of user data — makes the twelve-month deprecation window a compliance timeline, not just an engineering one.

**4 · A shared agent-skill specification makes the runtime swappable and relocates lock-in to the skill library**
The only new idea in the skills HEAD. Confirmed absent from [[SoT - AI Agent Skill Architecture]], which covers progressive disclosure, the Skill/MCP/Subagent distinction, triggering and distribution — but says nothing about cross-runtime portability. Weak source; the steelman does most of the work in this stub.

Each carries a `claim_statement`, a genuine `steel_man`, and `falsifiers`/`crux`/`confidence`/`counter_positions` left blank for you per §2.4.

---

## 4 · Updated: `wiki/projects/MCP Proxy Robustness and High Availability.md`

**This is the highest-value routing decision in the pass**, and it's the one a similarity-based system would have missed entirely — the HEAD never mentions your proxy.

Your dossier records, on 2026-05-28, that Hermes' MCP failures trace to streamable-HTTP requiring *"session negotiation, SSE, and correct `Accept` headers that sandbox `urllib` calls cannot provide"*, and on 2026-06-12 that LLMs take *"minutes to negotiate the connection."*

**The 2026-07-28 specification removes session negotiation entirely.** There is no handshake left to fail.

Added to the dossier, all cited to the raw capture:

- The spec change as a dated Key Fact, tied explicitly to the 2026-05-28 root cause
- The 2026-05-30 requirement that "proxy startup should be decoupled from LLM client startup" — now a protocol property rather than a workaround
- `ttlMs`/`cacheScope` and deterministic tool ordering as relevant to proxy latency
- The maintainers' own caveat: *"Statelessness at the protocol layer buys routability, not determinism"*
- Two timeline entries (RC freeze 21 May, final 28 July)

**One Open Question weakened, four new ones raised.** The sharpest:

> **Does `mcp-proxy` itself survive the spec change, or does it become unnecessary?** Much of what a local proxy provides — connection pooling, session persistence across clients, keeping servers warm — exists *because* the protocol demanded a session. If remote servers become ordinary stateless HTTP, the aggregation case collapses to tool-surface consolidation. **Worth answering before further investment in proxy HA.**

And a counterweight I added rather than letting the good news stand unqualified: your 2026-05-30 diagnostic found `mcp_mcp-proxy_*` tools **absent from the session entirely** (0 tools registered). That's a client-side registration bug, not a session-negotiation problem. The spec change fixes the *slow* failure, not the *silent* one.

---

## 5 · Typed edges written: ZERO

Deliberate, and worth understanding.

I looked for edges between notes that **already exist** and could be justified by the new content. I found none I'd defend:

- The three MCP notes (`Model Context Protocol (MCP)`, `…Standardises the LLM-to-Tool Interface`, `MCP Architecture Separates Host, Server, and LLM…`) are described by the source but their *relationship to each other* is not what the source establishes. Any edge there would be my inference, not the source's.
- The Pilot tension vs [[Enterprise Agentic Systems Require Containerised Gateways with OAuth and RBAC]] failed the contradiction test: both hold under different assumptions about deployment context (hobbyist swarm vs regulated production). **Prose tension, no edge** — and Pilot isn't a note anyway.
- Everything else the content licenses connects to claims that **do not exist yet as notes** — they're the four stubs above.

Two sessions ago the vault gained three `supports` edges pointing the wrong way, which made the compiler report three SoTs as grounded when nothing new grounded them. Writing an edge here to make this report look productive would be the same error. **A pipeline that returns zero when zero is correct is working.**

### What becomes writable on promotion

| Promote this stub | Then this edge becomes available |
|---|---|
| Statelessness → model-visible handles | `→ supports →` [[Targeting LLM Attention Requires Encoding Relevance as Structure]] (justification edge — moves the C1 list) |
| Operation-level headers | `→ supports →` [[Enterprise Agentic Systems Require Containerised Gateways with OAuth and RBAC]] (justification edge) |
| Sampling deprecation | `→ depends_on →` the statelessness claim once both exist |
| Skill portability | `→ extends →` [[SoT - AI Agent Skill Architecture]] (structural only — audit-invisible) |

**Two of the four are `supports` edges into existing claims.** That is the shape you want: new content grounding what the vault already holds, rather than accumulating beside it.

---

## 6 · What this test says about the pipeline

**It worked, and it worked for a reason that isn't obvious.** The MCP→proxy connection is the kind of hit that semantic similarity would have scored low — the article is about a protocol specification, the dossier is about a local chezmoi-managed process. What linked them was reading the dossier's *Open Questions* and noticing the spec change answered one and killed another. That is a comprehension step, not a retrieval step.

**Three honest limits:**

1. **Tier 3 throughout.** Lexical matching. I found the proxy dossier because I'd read it earlier in this session, not because search surfaced it. With a cold session and no semantic search, that connection is a coin flip. This is the strongest argument yet for getting 1MCP reachable.
2. **The human bottleneck is now four stubs deep.** Nothing reaches the graph until you promote them. That's the constraint I flagged earlier and this pass has just added to it — which is the honest cost of a propose-only design.
3. **Ratio check.** Three articles produced one substantial contribution, one moderate, and one that was correctly mostly rejected. Expect that ratio. A router that finds something valuable in every input isn't discriminating.

---

## Validation

- `edge_lint.py --path .` → **0 errors, 0 warnings** (2,315 notes, 297 edges). Graph unchanged, as intended.
- **Every `[[wikilink]]` in the seven files I authored was verified to resolve** against a 4,200-name index built from filenames, frontmatter `title`, and `aliases`/`alias`. One YAML quote-escaping artefact was caught and fixed. Zero dangling.
  *(Three pre-existing dangling links in the proxy dossier — `wiki/concepts/chezmoi`, `wiki/projects/Hermes Integration — Provider Adapter Setup`, and a `.md`-suffixed raw link — were **not** introduced by this pass and were left alone.)*
- No writes to `20_Thinking/` (read-only, §0) or `30_Library/` (§6).
- **Confidence: high** on the MCP routing and the corroboration assessment; **medium** on the skill-portability stub, whose source is weak; **high** on the decision to withhold the Pilot claims.
- **What would change my view:** if the Pilot figures get independent corroboration — an operator, a customer, or a third-party measurement — the agent-economy pattern becomes stub-worthy rather than watch-worthy. The trust assessment, not the pattern, is what's holding it back.
