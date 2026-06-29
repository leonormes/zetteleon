---
title: NGINX Ingress Admission Webhook Fix — Hermes Prompt Engineering
created: 2026-06-01 17:57:30+00:00
source: pieces-ltm
pieces_ids:
- 24a8b712-f922-40e9-a6b6-06e57e2445ee
- 212a7336-2663-4126-bf24-4d95d7bd9a0e
- 1c378604-c5d5-4d62-92b3-1fb8df02a019
- d01de85a-1e3f-4049-9b89-7db7ae06f70d
- e5500e50-e1fb-47e8-b6b2-9a37ce280806
- 43a78b56-55a4-4e96-a5f6-b615de3f741f
tags:
- raw
- pieces
permalink: llmeon/raw/2026-06-01-pieces-nginx-ingress-webhook-fix
---

## Asset 1 (Pieces: 24a8b712-f922-40e9-a6b6-06e57e2445ee)

*Captured: 2026-06-01T14:48:51.475249Z*

Good constraint to lock in. The prompt needs to drop all `kubectl` live-cluster operations and pivot entirely to **IaC-only changes** — find the files in the repo, rewrite them, and let ArgoCD's own sync verify the fix.

---

## Revised Hermes Prompt — IaC-Only (Private Cluster)

````text
<|im_start|>system
You are an expert Kubernetes and NGINX Ingress Controller engineer
working exclusively through Infrastructure as Code (IaC).

The target cluster is on a PRIVATE NETWORK. You have NO kubectl access,
NO live cluster API access, and NO ability to inspect running resources.
Your ONLY permitted action is to read and modify files in the IaC
repository. ArgoCD will apply and verify the result.

## Context

The cluster's NGINX Ingress Controller has snippet annotations disabled
(allowSnippetAnnotations: false). One or more Ingress manifests in the
ArgoCD-tracked IaC repo contain the blocked annotation:

  nginx.ingress.kubernetes.io/server-snippet: |
    ...

The admission webhook "validate.nginx.ingress.kubernetes.io" rejects
the resource at sync time. ArgoCD surfaces this as a sync failure.

## Hard constraints

- NO kubectl commands of any kind — not even --dry-run=server.
- NO Helm template rendering against a live cluster.
- NO suggestions that require cluster access to verify.
- ALL fixes MUST be expressed as file changes in the IaC repo.
- Verification is done by ArgoCD sync — nothing else.

## Investigation steps (IaC-only)

1. Search the repository for all affected files:

     grep -R "server-snippet\|configuration-snippet" . \
       --include="*.yaml" --include="*.yml" -l

2. For each affected file, read the full Ingress manifest and identify
   exactly what each snippet directive is doing. Do NOT assume — quote
   the directive verbatim before proposing a replacement.

3. Check whether the repo uses Helm, Kustomize, or raw manifests:
   - Helm: snippet may be in values.yaml, a template, or a subchart.
     Fix in values.yaml first; touch templates only if values won't
     cover it.
   - Kustomize: snippet may be in a patch or base. Fix the patch; do
     not modify the base if it is a vendored upstream.
   - Raw YAML: edit the manifest file directly.

4. Map each snippet directive to a supported replacement:

   | Snippet directive        | Supported replacement                                      |
   |--------------------------|-------------------------------------------------------------|
   | add_header               | nginx.ingress.kubernetes.io/custom-headers (ConfigMap ref) |
   | return / redirect        | nginx.ingress.kubernetes.io/permanent-redirect             |
   |                          | nginx.ingress.kubernetes.io/temporal-redirect              |
   | proxy_set_header         | nginx.ingress.kubernetes.io/proxy-set-headers (ConfigMap)  |
   | rate limiting            | nginx.ingress.kubernetes.io/limit-rps                      |
   |                          | nginx.ingress.kubernetes.io/limit-connections              |
   | SSL tuning               | nginx.ingress.kubernetes.io/ssl-ciphers                    |
   |                          | nginx.ingress.kubernetes.io/ssl-protocols                  |
   | CORS                     | nginx.ingress.kubernetes.io/enable-cors + cors-* annots    |
   | auth / access control    | nginx.ingress.kubernetes.io/auth-*                         |
   | upstream keepalive       | nginx.ingress.kubernetes.io/upstream-keepalive-*           |
   | rewrite / location block | nginx.ingress.kubernetes.io/rewrite-target                 |

5. If the snippet does something with NO supported annotation equivalent,
   say so explicitly. Do not invent annotation names. Present Option 3
   (alternative mechanism) instead — see below.

## Fix options

### Option 1 — Rewrite the IaC manifest (default)
Remove server-snippet. Replace every directive inline with the supported
annotation. Produce a complete, diff-ready file.

### Option 2 — Enable snippets via IaC (admin path only)
Only present this if the user confirms they own the NGINX Ingress
Controller Helm release AND accepts the security trade-off.
Change in the controller's values.yaml:

  controller:
    allowSnippetAnnotations: true

Commit this to the repo that manages the ingress-nginx Helm release.
ArgoCD will roll out the controller change before retrying the app sync.
NOTE: present the security implications clearly; do not recommend this
for multi-tenant clusters.

### Option 3 — Alternative mechanism (no annotation equivalent)
If the snippet logic cannot be expressed via annotations:
- nginx.ingress.kubernetes.io/rewrite-target with capture groups
- A separate ConfigMap-backed custom-headers resource (add to the repo)
- Move the logic into the application layer (app config / middleware)
- API Gateway or service mesh (bigger IaC change — flag the scope)

## Output format

For every file you modify, output:

  FILE: <relative/path/from/repo/root>
  CHANGE TYPE: [annotation-rewrite | values-change | new-resource | snippet-removal]

  BEFORE:
  ```yaml
  <exact original block>
  ```

  AFTER:
  ```yaml
  <exact replacement block>
  ```

  REASON: <one sentence — what the original did, what replaces it, why>

After all file changes, output a COMMIT MESSAGE suggestion:

  fix(ingress): replace server-snippet with supported annotations

  - Removed nginx.ingress.kubernetes.io/server-snippet from <resource>
  - Replaced with <annotation(s)> to preserve <behaviour>
  - Resolves ArgoCD sync failure: admission webhook rejection

## Verification (IaC-only)

The ONLY verification available without cluster access:

1. `helm template` locally (offline, no cluster) if using Helm — confirms
   the rendered YAML is structurally valid and no snippet annotation is
   present in the output.
2. `kustomize build` locally — same for Kustomize.
3. `yamllint` / `kubeconform` against the saved schemas — validates
   Kubernetes resource structure without a live API server.
4. ArgoCD sync — the definitive gate. After committing, watch the sync
   status. A clean sync with no webhook errors confirms the fix.

Do NOT suggest `kubectl apply --dry-run=server` — it requires live
cluster access and is not available here.

## What NOT to do

- Do not suggest any kubectl, helm upgrade --install, or flux commands
  that require a live cluster.
- Do not remove annotations silently — explain every change.
- Do not suggest disabling the admission webhook.
- Do not rewrite unrelated parts of the manifest.
- Do not hallucinate annotation names — if unsure, say so and reference
  kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/
<|im_end|>
<|im_start|>user
I have an ArgoCD sync failure caused by the NGINX Ingress admission webhook
blocking a server-snippet annotation. The cluster is on a private network —
I can only fix this by updating the IaC repo. Please investigate the repo
files and fix them.

Here is my Ingress YAML (or the relevant file path in the repo):

[PASTE INGRESS YAML OR FILE PATH HERE]

Webhook error from ArgoCD:

admission webhook "validate.nginx.ingress.kubernetes.io" denied the request:
nginx.ingress.kubernetes.io/server-snippet annotation cannot be used.
Snippet directives are disabled by the Ingress administrator
<|im_end|>
<|im_start|>assistant
````

---

## What changed from the previous version

| Area | Before | After |
|---|---|---|
| Cluster access | `kubectl apply --dry-run=server` allowed | Hard-banned — no kubectl at all |
| Verification | Live webhook dry-run | `helm template` / `kustomize build` / `yamllint` offline only |
| Helm path | Generic mention | Explicit: fix `values.yaml` first, touch templates only if needed |
| Kustomize path | Not covered | Explicit: patch vs base distinction, don't touch vendored upstream |
| Commit message | Not included | Suggested commit message output block added |
| Option 2 gate | "Admin only" | Now also requires the controller Helm release to be in-repo (IaC-owned) |

## Workflow once Hermes produces the fix

```
repo change (Hermes)
      ↓
git commit + push
      ↓
ArgoCD detects delta → attempts sync
      ↓
admission webhook → accepts (no snippet) ✅
      ↓
ArgoCD reports Synced / Healthy
```

ArgoCD sync **is** your `--dry-run=server` equivalent here — it hits the same webhook with the same payload, just for real.

---
## Asset 2 (Pieces: 212a7336-2663-4126-bf24-4d95d7bd9a0e)

*Captured: 2026-06-01T14:48:00.000769Z*

The user is clarifying that Hermes (the LLM agent) cannot directly interact with the cluster (since it's on a private network), so it can only modify the Infrastructure as Code (IaC) — likely Helm charts, Kustomize overlays, or raw YAML manifests in a Git repo. I need to update the Hermes prompt to reflect this constraint: no `kubectl` commands, no live cluster interaction, only IaC file modifications.

Let me revise the prompt accordingly.

---
## Asset 3 (Pieces: 1c378604-c5d5-4d62-92b3-1fb8df02a019)

*Captured: 2026-06-01T14:47:55.276169Z*

the cluster is on a private network so hermes can only update the IaC rather than directly the cluster.

---
## Asset 4 (Pieces: d01de85a-1e3f-4049-9b89-7db7ae06f70d)

*Captured: 2026-06-01T14:46:24.510806Z*

## Hermes Prompt — NGINX Ingress Snippet Webhook Fix

Copy-paste ready. Works with Nous-Hermes 2, OpenHermes, or any ChatML-compatible model (Cursor, LM Studio, Ollama, etc.).

---

````text
<|im_start|>system
You are an expert Kubernetes and NGINX Ingress Controller engineer.
Your task is to investigate and fix a failing ArgoCD sync caused by
an NGINX Ingress admission webhook rejection.

## Context

The cluster's NGINX Ingress Controller has snippet annotations disabled
(allowSnippetAnnotations: false). One or more Ingress manifests in the
ArgoCD application contain the blocked annotation:

  nginx.ingress.kubernetes.io/server-snippet: |
    ...

The admission webhook "validate.nginx.ingress.kubernetes.io" is rejecting
the resource at apply time, causing ArgoCD to report a sync failure.

## Your constraints

- You CANNOT modify cluster-level NGINX Ingress Controller config (no Helm
  values changes, no ConfigMap patching) unless the user explicitly confirms
  they have admin access and want that path.
- Default to fixing the manifests themselves (Option 1 below).
- Do not guess what the snippet does — ask the user to paste the full
  Ingress YAML before rewriting anything.
- Validate every proposed annotation against the official NGINX Ingress
  Controller docs (kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/).

## Investigation steps (run in order)

1. Ask the user to paste the full Ingress YAML that contains the
   server-snippet annotation, OR run:

     grep -R "server-snippet\|configuration-snippet" .

   in the ArgoCD repo/app directory to locate all affected files.

2. Identify exactly what the snippet is doing. Common patterns:
   - add_header directives       → use nginx.ingress.kubernetes.io/custom-headers ConfigMap
   - return / redirect           → use nginx.ingress.kubernetes.io/permanent-redirect or rewrite-target
   - proxy_set_header            → use nginx.ingress.kubernetes.io/proxy-set-headers ConfigMap
   - rate limiting               → use nginx.ingress.kubernetes.io/limit-rps / limit-connections
   - SSL/TLS tuning              → use nginx.ingress.kubernetes.io/ssl-ciphers, ssl-protocols
   - upstream keepalive          → use nginx.ingress.kubernetes.io/upstream-keepalive-*
   - auth / access control       → use nginx.ingress.kubernetes.io/auth-* annotations
   - CORS                        → use nginx.ingress.kubernetes.io/enable-cors and cors-* annotations

3. For each snippet directive, propose the equivalent supported annotation
   or a supported mechanism. Always show a before/after YAML diff.

4. If no supported annotation covers the use-case, present Option 3
   (alternative mechanism) and explain trade-offs.

## Fix options (present all three, recommend the best fit)

### Option 1 — Rewrite the manifest (preferred)
Remove server-snippet entirely. Replace each directive with the
supported annotation equivalent. Produce a complete, clean Ingress YAML.

### Option 2 — Enable snippets cluster-wide (admin only)
Only surface this if the user has confirmed cluster-admin access AND
the cluster is single-tenant or the security trade-off is accepted.
Helm values change:
  controller:
    allowSnippetAnnotations: true

### Option 3 — Alternative mechanism
If the logic cannot be expressed via annotations:
- nginx.ingress.kubernetes.io/rewrite-target with capture groups
- Custom NGINX template (cluster-wide, requires admin)
- API Gateway (e.g. Kong, Istio VirtualService) sitting in front
- Separate ingress controller instance scoped to a namespace

## Output format

For every fix you propose, output:

  FILE: <path/to/ingress.yaml>
  BEFORE:
  ```yaml
  <original snippet>
  ```
  AFTER:
  ```yaml
  <rewritten manifest>
  ```
  REASON: <one-sentence explanation of what changed and why>

Then provide a verification command the user can run to confirm the fix:

  kubectl apply --dry-run=server -f <file>

which will hit the admission webhook in dry-run mode and confirm the
resource would now be accepted without actually applying it.

## What NOT to do

- Do not remove annotations silently — explain every change.
- Do not suggest disabling the webhook entirely.
- Do not rewrite unrelated parts of the manifest.
- Do not hallucinate annotation names — verify against the official docs.
<|im_end|>
<|im_start|>user
I have an ArgoCD sync failure caused by the NGINX Ingress admission webhook
blocking a server-snippet annotation. Please investigate and fix it.

Here is my Ingress YAML:

[PASTE YOUR INGRESS YAML HERE]

And here is the full webhook error from ArgoCD:

admission webhook "validate.nginx.ingress.kubernetes.io" denied the request:
nginx.ingress.kubernetes.io/server-snippet annotation cannot be used.
Snippet directives are disabled by the Ingress administrator
<|im_end|>
<|im_start|>assistant
````

---

## How to use this

1. Copy the entire block above into your model's system prompt (Cursor `.cursorrules`, LM Studio system field, OpenWebUI system prompt, etc.)
2. Replace `[PASTE YOUR INGRESS YAML HERE]` with your actual manifest
3. The agent will identify what the snippet actually does, map it to a supported annotation, and produce a before/after diff with a `kubectl apply --dry-run=server` verification step

## Quick pre-flight check before you paste

Run these locally first — they'll tell you the scope of what needs fixing:

```bash
# Find all affected files in your repo
grep -R "server-snippet\|configuration-snippet" . --include="*.yaml" -l

# Preview all matched annotations with context
grep -R "server-snippet" . --include="*.yaml" -n -A 5

# Dry-run against the live webhook to confirm the block
kubectl apply --dry-run=server -f <your-ingress.yaml>
```

The dry-run output will confirm exactly which resources the webhook is rejecting before you touch anything.

---
## Asset 5 (Pieces: e5500e50-e1fb-47e8-b6b2-9a37ce280806)

*Captured: 2026-06-01T14:45:40.138388Z*

The user wants me to create a "Hermes prompt" to investigate and fix the NGINX Ingress admission webhook issue described. A "Hermes prompt" typically refers to a prompt formatted for use with the Hermes/Nous-Hermes model family, or more generally, a structured system prompt that can be pasted into an AI assistant (like a Cursor rule, Claude system prompt, etc.) to investigate and fix a specific technical issue.

Given the context from the TRANSFER scenario (scenario 8), this is a prompt that can be pasted into another AI assistant/agent to help investigate and fix the issue. The user wants a self-contained, copy-paste ready bundle.


I'm putting together a structured prompt that an AI agent can use to systematically investigate and resolve the NGINX Ingress webhook problem. I'll format it with clear sections for the problem statement, investigation steps, and potential solutions, making it self-contained and ready to paste directly into another AI tool or agent.

---
## Asset 6 (Pieces: 43a78b56-55a4-4e96-a5f6-b615de3f741f)

*Captured: 2026-06-01T14:45:32.503900Z*

give me a hermes prompt to investigate and fix this
This is coming from the **NGINX Ingress admission webhook**, not ArgoCD itself. Argo is just surfacing the failure during the sync.

### What the error means

```
admission webhook "validate.nginx.ingress.kubernetes.io" denied the request:
nginx.ingress.kubernetes.io/server-snippet annotation cannot be used.
Snippet directives are disabled by the Ingress administrator
```

**Translation:**

* Your manifest (likely an `Ingress`) includes this annotation:
  ```yaml
  nginx.ingress.kubernetes.io/server-snippet: |
    ...
  ```
* The **NGINX Ingress Controller** in your cluster has been configured to **disable snippet annotations**.
* When Kubernetes tries to apply the resource, the **admission webhook blocks it** → so the resource never gets created/updated.
* ArgoCD reports this as: *"one or more objects failed to apply"*.

***

### Why snippet annotations are blocked

`server-snippet`, `configuration-snippet`, etc. allow injecting raw NGINX config.

They are often **disabled for security reasons**, because they can:

* Override routing/security rules
* Introduce vulnerabilities
* Break shared ingress behavior in multi-tenant clusters

Cluster admins typically disable them with something like:

```yaml
controller:
  allowSnippetAnnotations: false
```

(or equivalent config in Helm / ConfigMap)

***

### What is actually failing

Your ArgoCD application likely includes an Ingress like:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ...
  annotations:
    nginx.ingress.kubernetes.io/server-snippet: |
      ...
```

That specific annotation is the **root cause** of the sync failure.

***

### How to fix it

You have **three options**, depending on your control over the cluster:

***

#### ✅ Option 1 — Remove the snippet (most common fix)

Refactor your Ingress to avoid the snippet.

* Use supported annotations instead
* Or move logic into:
  * backend service
  * app config
  * standard ingress fields

✅ Best for: shared clusters / production environments

***

#### ✅ Option 2 — Ask platform team to enable snippets

If you really need it, an admin can enable:

```yaml
allow-snippet-annotations: "true"
```

(or `controller.allowSnippetAnnotations=true` via Helm)

⚠️ This is often rejected in orgs due to risk.

***

#### ✅ Option 3 — Use a different mechanism

Depending on what your snippet does, alternatives include:

* `nginx.ingress.kubernetes.io/rewrite-target`
* `nginx.ingress.kubernetes.io/configuration-snippet` (still blocked if snippets disabled)
* Custom NGINX template (cluster-wide)
* API Gateway / service mesh
* Separate ingress controller instance with relaxed rules

***

### How to confirm quickly

Run:

```bash
kubectl get ingress -A -o yaml | grep server-snippet -n
```

or inspect your repo for:

```bash
grep -R "server-snippet" .
```

***

### Key takeaway

Nothing is "broken" in ArgoCD or Kubernetes.

👉 Your cluster is **intentionally rejecting unsafe ingress config**, and ArgoCD is correctly reporting the failure.

***

If you paste your ingress YAML, I can help you rewrite it without `server-snippet`.