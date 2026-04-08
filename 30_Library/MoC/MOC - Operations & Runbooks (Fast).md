---
aliases: [Ops Index, Runbooks Index, On-Call Index]
created: 2026-04-08T00:00:00+00:00
status: seedling
tags: [moc, ops, triage]
title: MOC - Operations & Runbooks (Fast)
type: map
---

## Navigation Hub: Operations & Runbooks (Fast)

Purpose: fast entry points into the *most-used* ops notes (by inbound links across the vault), plus a routing rubric for new ops notes.

### 1) High-frequency “go-to” notes (~15)

#### Netshoot / cluster triage

- [[cmd-k8s-run-netshoot]]
- [[pb-netshoot-deployment]]
- [[pb-cross-cluster-connectivity-triage]]

#### ArgoCD / VSO / registry auth

- [[cmd_argocd_refresh_app]]
- [[cmd-k8s-describe-argocd-app]]
- [[cmd_argocd_get_app]]
- [[playbook_argocd_vso_oci_registry_auth_failure]]
- [[playbook_vso_secret_debugging]]
- [[kb_vso_metadata_identifiers]]
- [[cmd_kubectl_argocd_find_repo_secrets]]
- [[cmd_kubectl_argocd_get_secret_creds]]
- [[cmd_kubectl_get_image_pull_secret_creds]]
- [[cmd_kubectl_restart_argocd_repo_server]]
- [[cmd_kubectl_argocd_get_app_operation_state]]

#### Network testing

- [[cmd-net-mtr-tcp]]
- [[cmd-net-nmap-check-filtered]]
- [[cmd-net-get-egress-ip]]

---

## Routing rubric for new ops notes (binary decisions)

### Step 0 — Is this an action, a procedure, or knowledge?

- If it is a **single command** you’ll copy/paste: create `cmd-<area>-<verb>-<object>.md`
- If it is a **multi-step procedure** with decision points: create `pb-<symptom-or-goal>.md` (playbook)
- If it is **stable explanation / identifiers / invariants**: create `kb-<topic>.md`

### Step 1 — Choose the prefix (pick exactly one)

- `cmd-` = one primary command (may include small variants and flags)
- `pb-` = incident workflow (symptoms → checks → branches → resolution)
- `kb-` = reference knowledge that makes other notes shorter
- `playbook_` / `cmd_` = only use if you are deliberately keeping legacy naming (otherwise prefer the short prefixes above)

### Step 2 — Required sections (minimum viable structure)

#### For `cmd-*`

- **When to use**
- **Command**
- **Expected output / success signal**
- **Failure modes** (2–5 bullets)
- **Safety / blast radius** (what it changes, if anything)

#### For `pb-*`

- **Trigger** (symptoms, alerts, user impact)
- **Goal state** (what “fixed” means)
- **Triage steps** (ordered; each step ends with a yes/no branch)
- **Resolution paths** (2–4 named paths)
- **Escalation / stop conditions**

#### For `kb-*`

- **Definition**
- **Identifiers / invariants**
- **Common confusions**
- **Links to the cmd/pb notes that depend on it**

### Step 3 — Mandatory routing links (make it navigable)

- Add a backlink to: [[MOC - Operations & Runbooks (Fast)]] (or your canonical ops MoC)
- Link out to exactly one “parent area” anchor:
  - ArgoCD / GitOps
  - Kubernetes
  - Networking
  - Secrets / VSO
  - Deployments (if applicable)

### Step 4 — Naming test (if it fails, rename)

- Could you find it in 2 seconds by typing 3–5 letters?
- Does the filename encode **scope + action** (for cmd/pb) or **topic** (for kb)?
- Is it consistent with existing high-frequency notes?

## Next action

- [ ] Pick the canonical ops hub name (this “Fast” MoC vs a fuller one), then ensure every new `cmd-*` / `pb-*` / `kb-*` links back to it.

