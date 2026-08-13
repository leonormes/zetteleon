---
created: 2026-07-28T00:00:00+00:00
epistemic_status: medium
modified: 2026-08-13T10:54:51+00:00
permalink: llmeon/30-library/100-zettelkasten/privacy-tombstones-mark-sensitive-files-as-off-limits-to-ai-agents
tags: [domain/llm, topic/agent-architecture, topic/pkm, topic/privacy, topic/safety]
title: Privacy Tombstones Mark Sensitive Files as Off-Limits to AI Agents
type: claim
---

## Privacy Tombstones Mark Sensitive Files as Off-Limits to AI Agents

An AI agent with file system access will read whatever it encounters unless told otherwise. In a personal knowledge vault, that includes tax documents, medical records, or other sensitive files that happen to sit in the same folder tree as material meant for AI synthesis.

A privacy tombstone is an empty or minimal marker file that tells the system: "a file exists here locally, but it is not to be read, scanned, or included in any sync/push operation." The AI agent sees the marker, recognises the boundary, and skips the underlying sensitive file entirely.

### Distinct from Archival Tombstones

This is a different usage of the word "tombstone" from the link-redirect pattern used for archiving merged notes (a stub at the same title so wikilinks resolve rather than dangle). Both use minimal marker files, but the archival tombstone exists to preserve reachability after content is removed, while the privacy tombstone exists to block reachability of content that must never be processed. Same mechanism (marker file), opposite intent.

### Scope & Conditions

Applies to any AI-agent-managed vault or repository where:

1. Sensitive files must remain locally accessible to the human but never touched by the agent
2. The vault or its derivative outputs may be synced to a remote/shared location (GitHub, cloud backup)
3. Accidental inclusion carries real consequence (financial exposure, privacy breach, compliance violation)

### Evidence

Source: "I Built Karpathy's LLM Wiki in Claude Code (No Vector DB)" (Achuth G. Ramesh). Quote: "To prevent the AI from accidentally reading or uploading private files (like tax documents) to GitHub, the creator used 'tombstones'—empty markers that tell the system the files exist locally but shouldn't be accessed or scanned" [07:04].

### Implications

- Defense at the file layer, not the prompt layer: Relying on prompt instructions alone ("don't read tax files") is fragile; a structural marker the harness enforces is more reliable.
- Git/sync safety: Combined with `.gitignore`-style exclusion, tombstones provide a second layer of protection against accidental exposure.
- Discoverable but inert: Unlike outright exclusion (which hides the file from the agent entirely), a tombstone lets the agent know the boundary exists, which can aid auditing ("what am I not allowed to see?").

### Related

- [[SoT - Evolutionary Note System]]—contrast: the vault's own tombstone pattern serves the opposite purpose (preserving link reachability after archival, not blocking access).
- [[Canaries - Precise Trigger Alarms Reduce False-Positive Security Noise]]—complementary: canaries detect breach attempts; tombstones prevent them structurally.
- [[Agent Harness - Wrapping LLMs in Deterministic Software Controls]]—implements: the harness is what enforces tombstone boundaries.

### See Also

- [[SoT - LLM Wiki Pattern]]

%%[implements:: [[Agent Harness - Wrapping LLMs in Deterministic Software Controls]], strength=3, confidence=medium]%%
