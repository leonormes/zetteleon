---
aliases: []
confidence: 
created: 2025-10-31T09:04:03Z
epistemic: 
last_reviewed: 
modified: 2025-10-31T09:16:08Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: GitKraft
type: 
uid: 
updated: 
---

## <https://youtube.com/watch?v=G8VT_YaDY5U>\&si=eDwLtckrDMaRb07x

The video you provided details how GitKraft enables teams to privately fork and customize open-source Helm charts—solving major pain points in Kubernetes chart patch management and DevOps workflows[^1_1].

### Core Concepts from the Video

- **Problem Solver:** Many organizations need to maintain their own patches to upstream Helm charts, but struggle to keep these patches when the original chart updates. Existing tools like Github’s public forks or patch files are either insecure or inadequate for secrecy and update management[^1_1].
- **GitKraft’s Solution:**
    - Adds a “private fork” feature to GitHub for Helm charts—including private forks of public repos, which Github doesn’t normally support[^1_1].
    - Uses a template repo and bootstrap workflow to create private repositories for your team, populated with the target chart’s full history.
    - Enables teams to apply custom patches directly in git, and seamlessly sync (or “weld merge”) those customizations with new upstream releases, maintaining a readable, auditable history without history loss or breakage[^1_1].
    - Special “welding merge” combines the safety of rebasing with Git compatibility for multi-user collaboration, preventing the git history disconnects often seen with straight rebases[^1_1].

### Practical Workflow Outline

- Fork a chart from the GitKraft catalog into your org, privately.
- Apply your custom changes as commits—directly in source, not rendered manifests[^1_1].
- When upstream releases a new chart version, click “update”—your patches are reapplied on top, with automatic conflict resolution support if needed, and you can resolve merge conflicts in a standard PR UI[^1_1].
- Parent/child history is kept cleanly visible, with patches always explicit on top of a clearly versioned base[^1_1].
- OCI, Helm repo, or tarball distribution aren’t needed—Git is the source of truth for both code and change history[^1_1].

### DevOps/Platform Engineer Integration

- Integrates directly with ArgoCD, Codefresh, and similar GitOps CI/CD platforms—just point to your organization’s forked repo. No custom tooling required for deployment pipelines[^1_1].
- All dependencies (including nested Helm chart dependencies) are kept as code, auditable and versioned[^1_1].

### Unique Security and Audit Features

- Workarounds Github’s limitations and the Truffle Security flaw (public forks can leak deleted/private repo content) by enabling private forks and containing all code in your organization’s security perimeter[^1_1].
- Full change auditability—every patch, update, or conflict resolution is a git commit in your history, attributed to the actual engineer making the change, not hidden in patch blobs[^1_1].

***

**Summary Table:**

| Feature | GitKraft (vs. Others) | Benefit |
| :-- | :-- | :-- |
| Private Forks of Public Repos | Yes (using template + workflow) | Secret, secure, auditable customization |
| Maintain Patches Over Updates | Yes (auto-merge \& conflict support) | No lost fixes, rapid security upgrades |
| Clean Git History | Yes (“welding merge” strategy) | Always see base \& customizations |
| Helm Dependency Management | Source as code, not blobs | Full diff visibility, better audits |
| GitOps Deploy Integration | Direct with ArgoCD, Codefresh, etc. | No new toolchain needed |

***

**Concrete Example:**
Patch a Helm chart line in your private fork, track it as a commit. When upstream updates, update your fork with a click; resolve conflicts in a PR if needed. Deploy as normal via ArgoCD using your fork as the source[^1_1].

If you need practical command examples, best-practices for workflow integration, or further detail on the custom merge strategy, just specify your use-case.

<div align="center">⁂</div>

[^1_1]: <https://www.youtube.com/watch?v=G8VT_YaDY5U>\&si=eDwLtckrDMaRb07x
