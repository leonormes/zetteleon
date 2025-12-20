---
aliases: []
confidence:
created: 2025-11-06T11:51:53Z
epistemic:
last_reviewed:
modified: 2025-11-06T11:52:17Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: []
title: App of Apps Prompt
type: prompt
uid:
updated:
---

**LLM PROMPT: ArgoCD App of Apps – Render and Policy Scan Kubernetes Manifests**

***

**Context**:
You are a DevOps engineer working with ArgoCD in App of Apps pattern. In this pattern, there is a parent ArgoCD Application (“root”) that manages multiple child ArgoCD Applications, each of which may deploy multiple Kubernetes manifests (YAML files) to clusters.

- All application definitions and manifests are stored in local directories (or Git).
- Each Application defines `spec.source.path` (for kustomize/helm/plain).
- The rendering process must account for ArgoCD’s mechanism: it traverses App of Apps, renders each child application according to its declared source type (Helm, Kustomize, directory of YAMLs, etc.), merges values/overlays, and creates the full set of manifests that would actually be applied to the Kubernetes cluster.

**Task:**
Given:

- The **root “App of Apps” manifest**
- All referenced sub-application manifests and their referenced Kustomize bases, Helm values, or raw YAMLs, in local directories

**You must:**

1. Traverse the full application tree starting from the App of Apps manifest.
2. For each child (and grandchild, recursively):
    - Detect the source type (Helm, Kustomize, YAML directory).
    - Render the manifests as ArgoCD would (Helm template, Kustomize build, or direct YAML expansion).
    - Respect overlays and values files per ArgoCD conventions.
3. Collect all final manifests that would be applied to the cluster in their rendered YAML form.

**Extra Instructions:**

- Output the combined YAML set: one YAML document per manifest, separated by `---`.
- Skip ArgoCD Application CRs themselves in the output.
- Do **not** apply or connect to a live cluster – render only.
- Then run a policy scan (using best-practice policy rules, e.g., Kubernetes security, vulnerability, and compliance checks) on the rendered manifests.
- Report any violations in a concise list after the manifests.

**Input Example:**

```sh
.
├── root-app.yaml         # App of Apps manifest
├── child1/
│   ├── app.yaml          # Child app manifest (kustomize)
│   └── kustomization.yaml
│   └── base/
│       └── deployment.yaml
├── child2/
│   ├── app.yaml          # Child app manifest (Helm)
│   └── chart/...
└── child3/
    ├── app.yaml          # Child app manifest (raw YAMLs)
    └── manifest.yaml
```

**Prompt:**
**Render** the manifests described above as ArgoCD would (resolving App of Apps hierarchy and overlays/templating). **Output:**

- The fully rendered Kubernetes manifests (`---` separated).
- A summary table of **any policy violations** detected (policy name, affected resource, summary).

**Assume**:

- All files are present locally and readable.
- ArgoCD v2.x conventions.
- Use standard policy checks (PodSecurity, default-deny, resource limits, etc.).

***
