---
aliases: []
created: 2026-02-14T09:02:32+00:00
modified: 2026-07-13T08:45:25+00:00
permalink: llmeon/30-library/ops/atomic-command-template
tags: []
title: Atomic Command Template
---

Excellent. We're going to treat your notes as an operational runtime, not documentation.

Your goal is not "remembering syntax."

Your goal is reducing Time to Command (TTC) under pressure.

We'll design:

1. ✅ An Atomic Command Template (single executable unit)
2. ✅ A Playbook Structure (composable execution graph)
3. ✅ A Context Model (explicit hop-state + prerequisites)

No folders. Only metadata and linking.

---

## 1️⃣ Atomic Command Template (Obsidian)

This is a single executable action, with explicit execution state and verification.

Copy this as your base template.

`````md
---
type: atomic_command
tool: <kubectl|argocd|ssh|aws|terraform|curl|jq|...>
hop_level: <local|bastion|cluster>
target_service: <argocd|k8s|network|dns|istio|app_name>
requires_tunnel: <true|false>
prerequisites:
  - [[Command - Establish Bastion Tunnel]]
tags: #atomic #<tool> #<target_service>
---

# <Action Name>

## 🎯 Intent

<What state are we trying to observe or change?>

---

## 🌍 Execution Context

Run from:

- [ ] Local machine
- [ ] Bastion host
- [ ] Inside cluster (kubectl exec)

Active requirements:

- [ ] KUBECONFIG set
- [ ] AWS_PROFILE set
- [ ] SSH tunnel active
- [ ] ArgoCD login active

---

## ⚡ Action

```bash
<copy-pasteable command with <placeholders>>
```

### Placeholders

- `<namespace>` — target namespace
- `<app_name>` — ArgoCD application
- `<pod_name>` — target pod
- `<profile>` — AWS profile
- `<region>` — AWS region

---

## ✅ Verification

```bash
<verification command>
```

Expected signal:

- <What confirms success?>
- <What confirms failure?>

---

## 🧠 Failure Modes

- <Common mistake>
- <Wrong context symptom>
- <Auth failure symptom>

---

## 🔗 Related

- [[Playbook - ArgoCD App Not Syncing]]
- [[Command - Get Pods By Node]]

---

### Why This Works

- Forces execution context declaration
- Forces prerequisite linking
- Forces verification
- Makes commands composable
- Prevents context drift

---

# 2️⃣ Example: Bastion Tunnel Command (Atomic)

````markdown
---
type: atomic_command
tool: ssh
hop_level: local
target_service: network
requires_tunnel: false
tags: #atomic #ssh #bastion
---

# Establish Bastion Tunnel to Private Cluster API

## 🎯 Intent

Create SSH tunnel to access private Kubernetes API endpoint.

---

## 🌍 Execution Context

Run from:

- [x] Local machine

- [ ] Bastion host



Active requirements:

- [ ] SSH key loaded

- [ ] VPN connected (if required)



---



## ⚡ Action



```bash

# 1. Set target

export TARGET_IP=<private_cluster_endpoint>



# 2. Establish tunnel

ssh -i ~/.ssh/<key.pem> \

    -L 6443:$TARGET_IP:443 \

    ec2-user@<bastion_public_ip>

```



---



## ✅ Verification



```bash

curl -k https://localhost:6443/version

```



Expected signal:

- JSON Kubernetes version response

Failure signal:

- Connection refused → tunnel not active
- Timeout → wrong endpoint

---

## 🔗 Related

- [[Command - Set Kubeconfig Context]]
````
`````

---

## 3️⃣ Example: ArgoCD Sync Command (With Tunnel Dependency)

````markdown
---
type: atomic_command
tool: argocd
hop_level: local
target_service: argocd
requires_tunnel: true
prerequisites:
  - [[Command - Establish Bastion Tunnel]]
tags: #atomic #argocd
---

# Force Sync ArgoCD Application

## 🎯 Intent

Force reconciliation of ArgoCD app with Git state.

---

## 🌍 Execution Context

Run from:

- [x] Local machine
- [ ] Bastion host

Active requirements:

- [ ] SSH tunnel active
- [ ] argocd login completed

---

## ⚡ Action

```bash
argocd app sync <app_name> --prune --timeout 300
```
````

---

## ✅ Verification

```bash
argocd app get <app_name>
```

Expected signal:

- Sync Status: Synced
- Health Status: Healthy

Failure signal:

- OutOfSync persists
- Degraded health

---

## 🔗 Related

- [[Playbook - ArgoCD App Not Syncing]]

````

---

## 4️⃣ Playbook Structure (Execution Graph)

Playbooks are state machines, not prose walkthroughs.

---

### Playbook Template

```markdown
---
type: playbook
target_service: argocd
incident_type: sync_failure
tags: #playbook #argocd
---

# ArgoCD App Not Syncing

## 🧭 Trigger Condition
- App stuck OutOfSync
- Health = Degraded

---

## 🧱 Execution Flow

1. [[Command - Establish Bastion Tunnel]]
2. [[Command - Argocd Login]]
3. [[Command - Get App Status]]
4. [[Command - Force Sync ArgoCD Application]]
5. [[Command - Get Pods By Node]]
6. [[Command - Describe Failed Pod]]

---

## 🔎 Decision Branches

### If Sync Fails:
→ [[Command - Get Application Events]]

### If Pods CrashLoop:
→ [[Command - Get Pod Logs]]

### If ImagePullBackOff:
→ [[Command - Check Image Registry Access]]

---

## 🧠 End State

Success =
- App Synced
- All Pods Running
- No CrashLoops
```

---

## 5️⃣ Critical Design Principles (For You)

### 1️⃣ No Nested Explanations

Only executable state.

### 2️⃣ Every Command Must Answer

- Where am I?
- What prerequisites?
- What confirms success?

### 3️⃣ TTC Optimization Rule

If you ever:

- Search for syntax twice → create atomic note.
- Forget which hop → enforce hop_level property.
- Forget verification → add explicit verification section.

---

## 6️⃣ Metadata Query Power (Obsidian Dataview Ready)

Later, you can query:

Show all bastion commands:

```dataview
table tool, target_service
from #atomic
where hop_level = "bastion"
```

Show all ArgoCD commands:

```dataview
table hop_level, requires_tunnel
from #atomic
where target_service = "argocd"
```

You are building a command runtime index, not notes.

---

## 7️⃣ The Mental Shift

You are not writing notes.

You are:

- Defining system transitions.
- Encoding network topology awareness.
- Building a command graph.
- Reducing cognitive reload time.

---

If you want, next we can:

- Add a Hop Transition Model (local → bastion → cluster)
- Build a K8s Node Drain Debug Playbook
- Or formalize a Command Naming Convention to eliminate ambiguity.
````
