---
captured: "2026-02-16T09:40:03+00:00 2026-02-16T09:40:03+00:00"
created: 2026-02-16T09:40:07+00:00
modified: 2026-02-16T09:50:34+00:00
source: "https://gemini.google.com/share/dde3b5331034"
status: "processing"
tags: ["input"]
title: Obsidian Commands and Playbooks
type: "head"
---

## The Architecture: Modular Knowledge

The core concept is to treat individual commands as reusable objects (Atomic Notes) and debugging sessions as orchestration (Playbooks).

---

## Component 1: The Atomic Command Template

This is the primitive unit of your knowledge base. It is designed to be completely self-contained. Even if you find this note in isolation 6 months from now, you will know exactly _where_ to run it and _how_ to check if it worked.

Filename Convention:`cmd_<tool>_<action>_<target>` (e.g., `cmd_argocd_sync_app`)

## Variables

- `<APP_NAME>`: The name of the ArgoCD application (e.g., `payment-service-prod`).
- `<ARGOCD_SERVER_IP>`: Internal IP of the ArgoCD server pod/service.
- `<ARGOCD_TOKEN>`: Your current session token (see [[cmd_argocd_get_token]]).

## 2. Verification

_Confirm the sync status is 'Synced' and health is 'Healthy'._

Expected Output:

> Sync Status: Synced Health Status: Healthy

## 3. Failure Mode Analysis

- Error:`dial tcp <IP>:443: connect: connection refused`
	- Fix: Check if the Bastion firewall allows egress to the K8s API.
- Error:`rpc error: code = Unauthenticated`
	- Fix: Token expired. Re-run [[cmd_argocd_login]].

```markdown
#### Key Design Elements:
1.  YAML Properties: Allows you to query commands using the Dataview plugin (e.g., "Show me all high-risk commands for ArgoCD").
2.  Transclusion Links (`[[...]]`): The `requires_tunnel` property links directly to the command needed to set up the network path.
3.  Atomic Copy/Paste: The code blocks are isolated.
4.  Verification Loop: You are forced to define success before you execute.

---

### Component 2: The Playbook Structure

A Playbook is not a wall of text. It is a checklist that transcludes (embeds) the Atomic Commands. This allows you to update a command in one place (the Atomic Note) and have it update in every Playbook that uses it.

Filename Convention: `playbook_<scenario_name>` (e.g., `playbook_argocd_out_of_sync`)

```markdown
---
type: playbook
target_service: argocd
trigger: "Alert: Application OutOfSync"
severity: p3
---

# Playbook: ArgoCD Application Out of Sync

## Phase 0: Context Establishment
*Ensure connectivity before attempting diagnosis.*

1. Establish Connectivity
   ![[cmd_ssh_bastion_login#1. The Command]]
   
2. Open ArgoCD Tunnel
   ![[cmd_ssh_tunnel_argocd_server#1. The Command]]

---

## Phase 1: Diagnosis
*Determine why the application has drifted.*

1. Check Diff
   ![[cmd_argocd_app_diff#1. The Command]]

2. Verify Cluster Connectivity (Is ArgoCD unable to talk to the target cluster?)
   ![[cmd_argocd_cluster_list#1. The Command]]

---

## Phase 2: Remediation
*Attempt to reconcile the state.*

> [!DANGER] Stop
> If the diff shows unexpected resource deletion, escalate to Principal Engineer before syncing.

1. Sync Application
   ![[cmd_argocd_sync_app]]

---

## Phase 3: Final Verification
*Confirm the system is stable.*

1. Verify Pod Health
   ![[cmd_kubectl_get_pods_selector#1. The Command]]

2. Verify Service Endpoints
   ![[cmd_curl_internal_healthcheck#1. The Command]]
```

### The Transclusion Magic

Notice the syntax `![[Note Name#Section]]`.

- In Obsidian, this renders the _content_ of the referenced note directly in the Playbook.
- You do not rewrite the command. You embed the "Single Source of Truth."
- If the syntax for `argocd app sync` changes, you update `cmd_argocd_sync_app`, and this Playbook updates automatically.

---

## Implementation Strategy: The "Dataview" Dashboard

To manage this library without folder structures, you will use the Dataview plugin to create a dynamic index. Create a note called `00_Command_Center`.

## High Risk Commands (Requires Peer Review)

## Playbooks by Service

You said

here is an existing note. break it down and give me the notes for this new system

## Argo CD Refresh & Debug Playbook (kubectl-first)

Purpose: Quick commands to refresh Argo CD Applications and identify why they are OutOfSync, Degraded, or stuck on failed sync attempts—using only kubectl (no argocd CLI required).

Scope: Clusters where Argo CD is installed in argocd namespace and Applications are CRs (application.argoproj.io).

---

### 1) Quick Mental Model

Argo evaluates an Application by:

1. Reading desired state (Git/Helm/Kustomize)
2. Comparing to live state in the cluster
3. Reporting:

- sync.status: Synced | OutOfSync | Unknown
- health.status: Healthy | Degraded | Progressing | Missing | Unknown
- conditions explaining failures (e.g., SyncError, ComparisonError)

A "Refresh" tells Argo to re-run comparison right now.

---

### 1) List Applications + Current Status

```sh
kubectl get applications -n argocd
```

If you want a concise table-like view with sync/health:

```sh
kubectl get applications -n argocd -o custom-columns=NAME:.metadata.name,SYNC:.status.sync.status,HEALTH:.status.health.status --no-headers
```

---

### 2) Force Argo to Refresh an Application

#### Soft Refresh (often enough)

```sh
kubectl annotate application -n argocd <app-name> argocd.argoproj.io/refresh=normal --overwrite
```

#### Hard Refresh (best when Debugging drift)

```sh
kubectl annotate application -n argocd <app-name> argocd.argoproj.io/refresh=hard --overwrite
```

Why:

- normal refreshes the app status and comparison.
- hard forces a deeper refresh (use when Argo seems stale).

---

### 3) Show Exactly What Resources Are OutOfSync

This prints every tracked resource and its per-resource sync/health:

```sh
kubectl get application -n argocd <app-name> -o jsonpath='{range.status.resources[*]}{.kind}{" "}{.namespace}{" "}{.name}{" sync="}{.status}{" health="}{.health.status}{"n"}{end}'
```

Why:

When an app is OutOfSync, this tells you which specific resources are causing it.

---

### 4) Show Application Conditions (why Sync Failed / degraded)

```sh
kubectl get application -n argocd ff-hie-test-34 -o jsonpath='{range.status.conditions[*]}{.type}{" "}{.reason}{" "}{.message}{"n"}{end}'
```

Why:

This is where you'll see messages like:

- SyncError Failed sync attempt …
- ComparisonError …
- admission webhook failures
- immutable field errors
- missing resources / RBAC issues

---

### 5) Show Last Operation State (most Useful for "Failed Sync attempt")

```sh
kubectl get application -n argocd <app-name> -o yaml | sed -n '/operationState:/,/^status:/p'
```

If you want only the message:

```sh
kubectl get application -n argocd <app-name> -o jsonpath='{.status.operationState.message}{"n"}'
```

Why:

operationState often includes the clearest "what failed to apply and why".

---

### 6) Quickly Identify "app-of-apps" (parent Apps Managing Child apps)

If the resources list contains many Application argocd \<child-app>, then it's a parent app.

List child apps tracked by a parent:

```sh
kubectl get application -n argocd <parent-app> -o jsonpath='{range.status.resources[?(@.kind=="Application")]}{.name}{" sync="}{.status}{" health="}{.health.status}{"n"}{end}'
```

Why:

Parent apps can be Degraded even when workloads run, because a _child app_ is OutOfSync or failed sync.

---

### 7) Refresh Everything in a "deployment bundle" (common workflow)

Example: if \<parent-app> is an app-of-apps:

```sh
# Refresh parent
kubectl annotate application -n argocd ff-hie-test-34 argocd.argoproj.io/refresh=hard --overwrite

# Refresh all child apps listed by the parent (manual loop)

kubectl get application -n argocd ff-hie-test-34 -o jsonpath='{range.status.resources[?(@.kind=="Application")]}{.name}{"n"}{end}'
```

Then refresh each child:

```sh
kubectl annotate application -n argocd <child-app> argocd.argoproj.io/refresh=hard --overwrite
```

Why:

Parent status may not clear until children re-compare cleanly.

---

### 8) Common "OutOfSync but Pods Are running" Causes + what to Check

#### A) Immutable ConfigMap/Secret Rotated / Replaced

Symptoms:

- old hashed ConfigMap shows OutOfSync
- new hashed ConfigMap shows Synced
- workload is healthy

Find what's OutOfSync (Section 3), then verify it's referenced:

```sh
kubectl get deploy -n <ns> <deploy> -o yaml | grep -n '<old-configmap-name>|configMap'
```

If not referenced, it's orphaned and safe to delete:

```sh
kubectl delete configmap -n <ns> <old-configmap-name>
kubectl annotate application -n argocd <app> argocd.argoproj.io/refresh=hard --overwrite
```

#### B) Operator-managed Resources Mutate Live State

Examples: cert-manager, external-secrets, vault-secrets-operator, etc.

Argo can show drift due to auto-added annotations/labels.

Check the exact drifted resource from Section 3 and decide:

- allow drift (ignoreDifferences), or
- make Git match operator behaviour, or
- accept Argo re-apply.

---

### 9) Quick "what's different?" Checks (live Resource introspection)

Once you know the drifting resource from Section 3:

```sh
kubectl get <kind> -n <ns> <name> -o yaml
```

Useful focused greps:

```sh
kubectl get <kind> -n <ns> <name> -o yaml | egrep -n 'annotations:|labels:|image:|env:|configMapRef:|secretRef:'
```

Why:

This helps identify whether drift is a real config change or just metadata noise.

---

### 10) Optional: Server-side "force re-evaluation" via Restart (workload-level)

This doesn't change Argo sync status, but can help when you fixed a secret/config and need pods to pick it up:

```sh
kubectl rollout restart deployment -n <ns> <deployment-name>
```

---

### 11) Copy/paste "Debug Bundle" Template

Replace \<app> and run:

```sh
# 1) Refresh app
kubectl annotate application -n argocd <app> argocd.argoproj.io/refresh=hard --overwrite

# 2) List resources and their sync/health

kubectl get application -n argocd <app> -o jsonpath='{range.status.resources[*]}{.kind}{" "}{.namespace}{" "}{.name}{" sync="}{.status}{" health="}{.health.status}{"n"}{end}'

# 3) Show conditions (why)

kubectl get application -n argocd <app> -o jsonpath='{range.status.conditions[*]}{.type}{" "}{.reason}{" "}{.message}{"n"}{end}'

# 4) Show last operation message (if sync attempts failed)

kubectl get application -n argocd <app> -o jsonpath='{.status.operationState.message}{"n"}'
```

---

### Notes / Guardrails

- A refresh does not "sync". It only re-checks desired vs live.
- If Argo says it retried sync 5 times and failed, there is usually an apply error (immutable field, webhook rejection, RBAC, missing CRD).
- For app-of-apps, always inspect child apps—the parent reflects their state.

---

Owner: Platform Engineering

Category: Operational Playbooks → GitOps / Argo CD

Keywords: argocd refresh, outofsync, degraded, syncerror, kubectl-only

This transformation decomposes your prose-heavy note into the "Control Plane" structure. We will create four Atomic Commands and one Master Playbook.

The primary shift here is moving the "Why" (Mental Model) into the Playbook, and the "How" (JSONPath magic) into reusable Atomic Blocks.

---

### Part 1: The Atomic Commands

_Save these as individual notes. They are the tools in your box._

#### 1. List Application Status

Filename:`cmd_kubectl_argocd_list_apps`

## 2. Verification

_Check for specific unhealthy states._

## 2. Show Sync Failure Conditions

_Reveal why the sync failed (e.g., Immutable Fields, Webhook Rejection)._

## 3. Show Last Operation Message

_View the error message from the last attempt._

### Variables

- `<APP_NAME>`: The name of the ArgoCD Application CR.

## 2. Verification

_Confirm the annotation was applied. The Argo controller will remove this annotation once the refresh is complete._

_If the output is empty after a few seconds, the controller has successfully processed the refresh._

---

## Phase 1: High-Level Diagnosis

_Assess the blast radius. Is it one app or the whole cluster?_

1. List All Applications![[cmd_kubectl_argocd_list_apps]]
2. Identify App-of-Apps (If applicable) _If the degraded app manages other apps, check the children first._![[cmd_kubectl_argocd_list_children]]

---

## Phase 2: Deep Dive Analysis

_Isolate the specific resource causing the drift._

> [!TIP] Common Drift Causes
>
> - Immutable Fields: Changing a field that K8s forbids (e.g., Service ClusterIP).
> - Operator Mutation: An external operator (e.g., External Secrets) changed the live state, causing drift from Git.

1. Inspect Failure Details _Run the "Debug Bundle" to see specific resource drift and error messages._![[cmd_kubectl_argocd_inspect_app]]

---

## Phase 3: Remediation

_Force the controller to recognize the state or retry._

1. Hard Refresh _Use this to clear "Stale" states or force a re-comparison._![[cmd_kubectl_argocd_refresh_hard]]
2. Workload Restart (Optional) _If the ConfigMap is synced but the App is behaving oddly, force a pod restart._![[cmd_kubectl_rollout_restart#1. The Command]]

---

## Phase 4: Verification

_Confirm stability._

1. Re-check App Status _Ensure Sync is "Synced" and Health is "Healthy"._
