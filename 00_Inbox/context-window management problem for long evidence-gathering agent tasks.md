*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Monday May 18, 2026 - 10:30 AM*
---
Good question — this is a fundamental context-window management problem for long evidence-gathering agent tasks. Here's exactly what's happening and how to fix it structurally.

## Why it degrades

Every tool call appends its **full output** to the conversation context. For your audit:
- `.gitlab-ci.yml` → hundreds of lines
- 100-pipeline API response → thousands of tokens of JSON
- Each job log tail → hundreds of lines

Hermes is at 62.7K/128K (49%) after 3 compressions. The compactor summarises earlier turns lossy — and for raw evidence (pipeline IDs, log lines, variable names), summaries destroy the exact data you need.

---

## The fix: separate sessions per phase, file as memory

The single-session mega-prompt is the root cause. **The output file IS the memory, not the context window.**

### Pattern: phase-per-session with file handoff

```
Session 1: Phase 1 only → appends to INSIGHTFILE_PIPELINE_REPORT.md → /new
Session 2: Phase 2 only → appends to file → /new
Session 3: Phase 3 only → appends to file → /new
...
Session N: Final synthesis → reads file → writes executive summary
```

Each session opens with:

```
Read INSIGHTFILE_PIPELINE_REPORT.md to understand what has already been
collected. Then execute ONLY Phase [N] below. Write all findings to that
file. Do NOT reproduce tool output inline in your responses — write to
file and confirm with: "Phase N complete: [section name], [N] rows written."
```

---

## Structural rules to add to every Hermes evidence-gathering prompt

Add these as a **WORKING CONSTRAINTS** preamble:

````markdown
## WORKING CONSTRAINTS (read before any tool call)

1. **Write-first, context-clear**: After every terminal command or file
   read, write the relevant data to the output file IMMEDIATELY.
   Do not hold raw output in your response — confirm only with a
   single line: "✓ Written: [section], [N] items."

2. **No inline reproduction**: Never paste tool output into your chat
   response. The file is the record. Your responses should contain
   only single-line confirmations and transitions between steps.

3. **One phase per session**: If you see a compaction warning
   (⚠ Session compressed), STOP, write a CHECKPOINT section to the
   output file with what's been collected, and instruct the user to
   run `/new` with the handoff prompt below. Do not continue
   across a compression boundary.

4. **Shell-level compression**: Design `jq` queries to emit minimal
   output (counts, keys, summary rows) rather than full JSON objects.
   Append directly to file using `>> output.md` in the command itself
   where possible.
````

---

## Shell-level fixes: reduce what enters context

Instead of loading a full 100-pipeline JSON response into context:

```bash
# BAD — full objects go into context
glab api "...pipelines?per_page=100" | jq '[.[] | {id, status, ref, ...}]'

# GOOD — summary only enters context, full data goes to file
glab api "...pipelines?per_page=100" \
  | jq '[.[] | {id, status, ref, created_at, duration}]' \
  > /tmp/pipelines.json \
  && echo "Wrote $(wc -l < /tmp/pipelines.json) lines" \
  && jq 'group_by(.status)|map({status:.[0].status,count:length})' /tmp/pipelines.json \
  | tee -a INSIGHTFILE_PIPELINE_REPORT.md
```

Context only ever sees the summary table (10 lines), not the 500-line JSON blob. The full data is on disk if needed.

---

## Hermes config — check the compaction threshold

Your config at `~/.config/glab-cli/config.yml` isn't the right place, but from your memory there's a Hermes config at:

```
/Users/leon.ormes/.local/share/chezmoi/private_dot_hermes/private_config.yaml
```

Check this for a `max_tokens`, `context_limit`, or `compaction_threshold` setting. If present, you may be able to raise the compaction trigger or set `auto_compact: false` (forcing manual `/compact` calls, which you can defer until after a phase completes and has been written to file).

---

## Revised prompt structure for this specific task

Break the 7-phase prompt into these separate handoff sessions:

| Session | Phase | Scope | Expected context load |
|---------|-------|-------|----------------------|
| 1 | 1 | Read `.gitlab-ci.yml` + templates | ~10K tokens |
| 2 | 2 | 90-day pipeline list + status counts | ~8K tokens |
| 3 | 3a | Enumerate failed pipeline jobs | ~6K tokens |
| 4 | 3b | Sample job logs for failure modes | ~10K tokens |
| 5 | 4 | Build stage × job coverage table from file | ~4K tokens |
| 6 | 5 + 6 | Variables, runners, cross-reference | ~6K tokens |
| 7 | 7 + synthesis | Read file → write executive summary | ~8K tokens |

Each session stays well under 30K tokens — no compression needed.

---

## Handoff prompt template (paste at start of each `/new` session)

```
HANDOFF: Continue the InsightFILE pipeline audit.

1. Read INSIGHTFILE_PIPELINE_REPORT.md — this is the running evidence
   record from prior sessions. Do not re-collect anything already present.
2. Your task this session: [PHASE N only — paste phase text here]
3. Append findings under "## Phase N" heading in the report file.
4. Confirm each step with a single line only — no inline output.
5. When phase is complete, write "## PHASE N COMPLETE" to the file and stop.
```

The key principle: **the file is the agent's externalised memory — not the context window.** A fresh `/new` session with a file read at the start reconstructs everything the agent needs without carrying the weight of prior tool outputs.