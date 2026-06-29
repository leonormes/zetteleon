---
created: 2026-02-14 09:00:02+00:00
modified: 2026-02-16 09:35:44+00:00
title: playbook-template
permalink: llmeon/30-library/ops/playbook-template
---

## Trigger Condition

> When do you reach for this playbook?
> _Describe the observable symptom, alert, or Slack message that starts this flow._

```
<Example alert text, error message, or observed behaviour>
```

## Decision Context

> [!info] Before You Start
> - Execution origin: `<local | bastion | jumpbox>`
> - Required access: `<list credentials, VPN, kubeconfig contexts>`
> - Blast radius: `<read-only triage | mutating | destructive>`

## Flow

> [!tip] How to Read This
> Each step links to an Atomic Command note. Open the link, copy the command, run it.
> Decision points branch based on what you observe.

### Phase 1: Orient

> _Goal: Understand the current state before touching anything._

- [ ] Step 1 → [[atomic-command-note-1]]
      _Why:_ <one line on what this tells you>

- [ ] Step 2 → [[atomic-command-note-2]]
      _Why:_ <one line on what this tells you>

> [!question] Decision Point
> - If `<observed condition A>` → Continue to Phase 2
> - If `<observed condition B>` → Skip to [[other-playbook]] or Phase 3
> - If `<nothing looks wrong>` → See [[escalation-note]]

### Phase 2: Diagnose

> _Goal: Narrow to root cause._

- [ ] Step 3 → [[atomic-command-note-3]]
      _Why:_ <one line>

- [ ] Step 4 → [[atomic-command-note-4]]
      _Why:_ <one line>

> [!question] Decision Point
> - If `<root cause identified>` → Continue to Phase 3
> - If `<still unclear>` → Run [[deeper-diagnostic-command]]

### Phase 3: Act

> _Goal: Apply the fix. Mutating commands below._

> [!danger] Mutating Step—Confirm Context
> Run `kubectl config current-context` before proceeding.
> Expected: `<correct-cluster-context>`

- [ ] Step 5 → [[atomic-command-note-5]]
      _Why:_ <what this changes>

- [ ] Step 6 (Verify) → [[atomic-command-note-6]]
      _Why:_ <confirms the fix landed>

### Phase 4: Confirm & Close

- [ ] Step 7 → [[verification-command]]
      _Why:_ End-to-end confirmation that the system is healthy.

> [!success] Resolution Criteria
> The playbook is complete when:
> - `<observable condition 1 is true>`
> - `<observable condition 2 is true>`
> - `<no residual errors in logs for N minutes>`

## Rollback

> If Phase 3 made things worse:

- [ ] Rollback Step 1 → [[rollback-command-1]]
- [ ] Rollback Step 2 → [[rollback-command-2]]

## Post-Incident

- [ ] Update `last_verified` date on all Atomic Commands used
- [ ] If any command syntax changed, update the Atomic Command note
- [ ] If a new failure mode was discovered, create a new Atomic Command note
- [ ] Link this playbook run to your incident ticket: `<TICKET-ID>`

## Appendix: Related Playbooks

| Playbook | When to Use Instead |
|----------|-------------------|
| [[related-playbook-1]] | <condition> |
| [[related-playbook-2]] | <condition> |