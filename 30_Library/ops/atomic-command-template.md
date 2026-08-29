---
created: 2026-02-14T09:00:02+00:00
modified: 2026-08-29T09:36:46+00:00
permalink: llmeon/30-library/ops/atomic-command-template-1
title: atomic-command-template
---

## Purpose

> One sentence. What does this command tell you or change?
> Example: "Shows which nodes each pod in a deployment is scheduled on."

## Prerequisites

> [!warning] Execution Context: `{{hop_level}}`
> This command must be run from: `{{hop_level}}`

| # | Prerequisite | Link |
|---|-------------|------|
| 1 | Active tunnel to cluster | [[establish-ssh-tunnel]] |
| 2 | `kubeconfig` context set | [[set-kube-context]] |
| 3 | additional as needed | [[note-link]] |

## Command

```shell
# ── <What this does> ──
export TARGET_IP=<target_ip_address>

<command> \
  --flag <PLACEHOLDER_PURPOSE> \
  $TARGET_IP
```

### Placeholders

| Placeholder             | Description              | Example     |
| ----------------------- | ------------------------ | ----------- |
| `<PLACEHOLDER_PURPOSE>` | What this value controls | `my-value`  |
| `<PLACEHOLDER_TARGET>`  | What this targets        | `my-target` |

## Verification

> How do you know it worked?

```sh
# ── Verify: <expected outcome> ──
<verification-command>
```

Expected output pattern:

```
<what good looks like — a representative snippet>
```

> [!fail] Failure Signature
> If you see `<error pattern>`, this means `<root cause>`. See [[relevant-troubleshooting-note]].

## Context & Why

> _Why does this command exist? What principle does it encode?_
> _This section is your future self's "remind me why I care" block._

## Related

- Next step → [[next-logical-command]]
- Rollback → [[undo-or-rollback-command]]
- Playbook → [[parent-playbook-name]]
- [[playbook-template]]
