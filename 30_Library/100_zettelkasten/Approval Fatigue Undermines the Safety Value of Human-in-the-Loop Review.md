---
created: 2026-07-28T00:00:00+00:00
epistemic_status: medium
modified: 2026-08-08T10:29:15+00:00
permalink: llmeon/30-library/100-zettelkasten/approval-fatigue-undermines-the-safety-value-of-human-in-the-loop-review
proposition: Requiring manual approval for every individual agent action trains the
  "human to stop actually reading what they're approving — repeated, high-frequency"
  'clicking of "Approve" habituates the reviewer out of genuine scrutiny, which defeats'
  the purpose of having a human approval gate in the first place. This is a specific
  failure mode of human-in-the-loop review as a mechanism, distinct from the general
  argument that human review is necessary.
tags: [domain/llm, topic/human-oversight, topic/reliability]
title: Approval Fatigue Undermines the Safety Value of Human-in-the-Loop Review
type: claim
---

## Approval Fatigue Undermines the Safety Value of Human-in-the-Loop Review

Human-in-the-loop review is usually defended on the grounds that a human catches what automated checks miss. This claim identifies a mechanism by which that defense quietly fails: if the review gate fires too frequently, at too fine a grain, the human doesn't stay vigilant—they habituate. Clicking "Approve" dozens of times in a session trains exactly the behavior the gate was meant to prevent: rubber-stamping without reading. The gate still exists structurally, but it stops doing the work it was designed to do, because the human behind it has been conditioned into inattention by its own frequency.

This reframes "add a human approval step" as necessary but not sufficient for safety—the step also has to be calibrated (rare enough, high-stakes enough) to actually get read, or it becomes a structural fiction: a gate that always opens because the person operating it has stopped looking.

### Scope & Conditions

Applies to any workflow where a human is asked to approve individual agent actions at high frequency. Doesn't argue against human review generally—the fix implied is calibrating review frequency and stakes (fewer, higher-value checkpoints) rather than removing human review altogether.

### Evidence

Source: "The harness is all you need (mostly)" (github.blog, GitHub Copilot team). "If you have to approve everything the agent does, you might as well just do it yourself. Besides, that's a miserable user experience. Nobody wants to be relegated to sitting at a desk pressing the 'Approve' button all day. And pressing 'Approve' over and over just trains you not to read what you are being asked to approve, which defeats the purpose."

### Implications

- This is a specific failure mode of a mechanism the vault otherwise recommends: [[Human-in-the-Loop (HITL) as Mandatory Control Layer for High-Stakes LLM Applications]] and [[Mandatory Manual Code Review Before Deployment]] both argue for human review as a control layer; this note identifies a way that exact mechanism can silently fail if implemented at too fine a grain, without contradicting the case for human review itself.
- It's the underlying justification for why this vault's boundary-compression and single-checkpoint patterns work: [[Engineer Involvement Compresses to Planning and Review as Agentic Workflows Mature]], [[The Slow Loop Pattern - Constrained Off-Hours Agent Loops Produce a Single PR for Async Human Review]], and [[Automated CI Pipelines Wire an Adversarial LLM Reviewer Into Branch-and-Rebase Before Human Review]] all concentrate human review into a small number of higher-stakes checkpoints rather than continuous micro-approvals—this note supplies the mechanistic reason why that concentration is not just efficient but necessary for the review to remain genuine.
- It applies to the vault's other AI-driven elicitation mechanisms too: [[Systematic AI Clarifying Questions Surface Edge Cases During Planning]] explicitly warns against "accepting every suggestion from the AI"—the same habituation risk this note describes, applied to a planning/questioning gate rather than a final-approval gate.

### Related

- [[Human-in-the-Loop (HITL) as Mandatory Control Layer for High-Stakes LLM Applications]]—tension: identifies a way the recommended mechanism can silently fail without arguing against the mechanism itself.
- [[Mandatory Manual Code Review Before Deployment]]—related: same tension—this note explains a failure mode of the review gate that mandate depends on.
- [[Engineer Involvement Compresses to Planning and Review as Agentic Workflows Mature]]—supports: gives the mechanistic reason why concentrating review at boundaries (rather than continuous micro-approval) is necessary, not just efficient.
- [[The Slow Loop Pattern - Constrained Off-Hours Agent Loops Produce a Single PR for Async Human Review]]—supports: the single-PR checkpoint design is a direct countermeasure to the habituation risk this note describes.

### See Also

- [[Full-Autonomy Agent Execution Requires Sandboxing for Safety and Data Privacy, Not Just Concurrency]]

%%[supports:: [[Engineer Involvement Compresses to Planning and Review as Agentic Workflows Mature]], strength=3, confidence=medium]%%

%%[supports:: [[The Slow Loop Pattern - Constrained Off-Hours Agent Loops Produce a Single PR for Async Human Review]], strength=3, confidence=medium]%%
