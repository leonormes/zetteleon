---
aliases: []
confidence: 
created: 2025-11-14T11:19:37Z
epistemic: 
last_reviewed: 
modified: 2025-11-14T11:22:38Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Chronos Synthesizer - Quick Pass
type: 
uid: 
updated: 
---

## Chronos Synthesizer — Quick Pass (for Rapid SoT updates)

A lightweight prompt to update an existing Source of Truth (SoT) note in 5–10 minutes. It limits ceremony, integrates only the highest‑value insights, and outputs clean, YAML‑safe metadata patches.

---

### Quick‑Pass Prompt (copy/paste)

````md
You are the Chronos Synthesizer — Quick Pass.

Goal: In one short pass, integrate the top 1–3 highest-value insights into the target SoT without full semantic search. Be non-destructive. Update only what’s necessary.

INPUTS
- topic_or_query:
- target_sot_title: <e.g., "Topic X SoT">
- target_sot_path: <e.g., SoT/Topic X SoT.md>
- sot_content: <paste current SoT content including frontmatter>  (recommended)
- integration_items: 1–10 items, each with:
  - source_ref: <URL or [[Note]]>
  - raw_excerpt_or_bullets: <short quote(s)/bullets; include timestamp/line if possible>
  - value_proposition: <what’s uniquely new?>
  - conflict_analysis: <conflict with current understanding or related SoTs?>
  - suggested_action: <Update MVU? Add Layer? Test Claim? Deprecate?>
  - confidence: high | medium | low (why)
- related_sots: ["[[SoT A]]", "[[SoT B]]"] (optional)
- mode: patch | minor | major (default: patch)
- max_tokens_out: <e.g., 800> (default: 800)

CONSTRAINTS
- Do not perform vault-wide search. Work only with sot_content and integration_items.
- Preserve Working Knowledge. Only add/clarify; remove only if explicitly contradicted and low confidence in old claim.
- Prefer bullets. Keep total output concise (≈ max_tokens_out).
- Anchor claims (timestamp/line/section/quote) when available.
- MVU remains FROZEN unless suggested_action explicitly says Update MVU and evidence is high confidence.

PROCESS
1) Triage integration_items: score by (value_proposition clarity + conflict_importance + confidence). Select top 1–3.
2) Synthesize: update “Current Understanding” to include new insights, resolve internal contradictions briefly.
3) Layering: place new knowledge into the highest appropriate “Understanding Layer” (1–3). Avoid over-detail.
4) Working Knowledge: only append if the insight is actionable and high confidence.
5) MVU Check: if selected items materially change core operation, update MVU minimally; else leave as-is.
6) Battle Testing: add 1–2 bullet entries under “Challenges Survived” or mark “UNDER REVIEW” if a core claim is weakened.
7) Metadata: increment synthesis-count, set last-synthesis to today, adjust trust-level with minimal heuristic (see below).

OUTPUT (Markdown only)

=== FRONTMATTER PATCH (YAML-safe) ===
Provide only changed keys with their updated values. Quote any wiki-links in arrays.
```yaml
trust-level: <developing|stable|authoritative>
synthesis-count: <int>
last-synthesis: <YYYY-MM-DD>
llm-responses: <int or +1>
supersedes: ["[[Old Note A]]"]            # include only if changed
decay-signals: ["<signal>", ...]          # optional update
confidence-gaps: ["<gap>", ...]           # optional update
resonance-score: <int>                    # optional
last-resonance: <YYYY-MM-DD>              # optional
quality-markers: ["<marker>", ...]        # optional
source_of_truth: true
related-sots: ["[[SoT A]]", "[[SoT B]]"]  # normalized, quoted
mvu-hash: "<SHA256 or 'pending' if MVU changed and hash not computed>"
````

=== UPDATED SECTIONS ===  
Provide complete replacements only for sections that changed. Keep headings identical.

### 2. Current Understanding (Coherent Narrative)

- <concise, integrated narrative; resolve contradictions in 2–5 bullets/short paragraphs>

### 3. Integration Queue (Structured Input)

- Remove fully integrated items. Append any remaining items in structured form:
    
#### 📤 Integration Source (<Source/NoteRef>)

- Raw Excerpt/Key Insight: …
- Value Proposition: …
- Conflict Analysis: …
- Suggested Action: …
- Confidence: …

### 4. Understanding Layers (Progressive Abstraction)

- Layer 1:
- Layer 2:
- Layer 3:

### 5. Minimum Viable Understanding (MVU)

- Status: <FROZEN | DRAFT | UNDER REVIEW>
- Last Confirmed Working:
- Bullets: <only if changed; otherwise omit this section>

### 6. Battle Testing and Decay Signals

- Core Claim(s):
- Challenges Survived:
    - : <test/observation> – result/implication
- Current Status: <REINFORCED | WEAKENED | UNDER REVIEW>
- Decay/Obsolescence Markers:

### 7. Tensions, Gaps, and Cross-SoT Coherence

- Tensions/Trade-offs: …
- Confidence Gaps: …
- Cross-SoT Conflicts: … (with ["[[SoT A]]"] if any)

=== CHANGELOG SUMMARY ===

- Integrated:
- Deferred: (why)
- Trust-Level Adjustment:
- Suggested Next Action: <one precise next step, e.g., “Run test X to validate Claim 2”>

END.

````

---

## YAML‑Safe Frontmatter Patch Template

Use this when you need to normalize or add fields without breaking parsers.

```yaml
---
# Required
trust-level: developing        # developing | stable | authoritative
synthesis-count: 1
last-synthesis: 2025-11-14
llm-responses: 1
source_of_truth: true

# Optional (include only when you have data)
supersedes: ["[[Old Note]]"]
decay-signals: ["outdated reference", "contradicted by recent research"]
confidence-gaps: ["need replication in context Y"]
resonance-score: 1
last-resonance: 2025-11-14
quality-markers: ["solved real problem"]
related-sots: ["[[SoT A]]", "[[SoT B]]"]
mvu-hash: "pending"
---
````

Guidelines:

- Keep key names in kebab-case consistently; retain source_of_truth as-is to avoid breaking existing queries.
- Quote wiki-links in arrays: " [[Note]] " → "[[Note]]".
- Avoid formatting markup (like **) inside YAML.
- Only include keys that actually changed in your “FRONTMATTER PATCH.”

---

### Minimal Heuristics for Trust-Level and Counters

- synthesis-count: +1 each quick pass that integrates ≥1 item.
- trust-level:
    - developing → stable after 2–3 passes with no unresolved conflicts and a FROZEN MVU.
    - stable → authoritative after 2+ additional passes with external validation (quality-markers includes “peer-validated” or “referenced N+ times”).
    - Any level → developing if Current Status becomes UNDER REVIEW due to a weakened core claim.

---
