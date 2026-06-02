---
title: NGINX Ingress Admission Webhook Fix
wiki_type: dossier
entity_kind: project
created: 2026-06-01T17:58:23+00:00
modified: 2026-06-02T06:44:05+00:00
tags: [wiki, dossier]
sources: [raw/2026-06-01-pieces-nginx-ingress-webhook-fix, raw/2026-06-01-pieces-argocd-ingress-investigation, raw/2026-06-01-pieces-argocd-nginx-a, raw/2026-06-01-pieces-argocd-nginx-b]
---


## Summary

Investigation and fix for a failing ArgoCD sync caused by an NGINX Ingress admission webhook rejection. The cluster's NGINX Ingress Controller has snippet annotations disabled (`allowSnippetAnnotation: false`), causing Ingress manifests with `server-snippet` annotations to be rejected. The investigation spanned FTFL-512 (nginx server_tokens information disclosure), multiple ArgoCD force-sync attempts, and Helm template edits. Work is scoped to IaC-only changes (Helm charts, Kustomize overlays, or raw YAML in Git), since the target cluster is on a private network with no direct `kubectl` access.


## Key Facts

> "Good constraint to lock in. The prompt needs to drop all `kubectl` live-cluster operations and pivot entirely to **IaC-only changes** — find the files in the repo, rewrite them, and let ArgoCD's own sync verify the fix.  ---  ## Revised Hermes Prompt…" — [[raw/2026-06-01-pieces-nginx-ingress-webhook-fix]] (Pieces: 24a8b712-f922-40e9-a6b6-06e57e2445ee)
> "The user is clarifying that Hermes (the LLM agent) cannot directly interact with the cluster (since it's on a private network), so it can only modify the Infrastructure as Code (IaC) — likely Helm charts, Kustomize overlays, or raw YAML manifests in…" — [[raw/2026-06-01-pieces-nginx-ingress-webhook-fix]] (Pieces: 212a7336-2663-4126-bf24-4d95d7bd9a0e)
> "the cluster is on a private network so hermes can only update the IaC rather than directly the cluster.…" — [[raw/2026-06-01-pieces-nginx-ingress-webhook-fix]] (Pieces: 1c378604-c5d5-4d62-92b3-1fb8df02a019)
> "## Hermes Prompt — NGINX Ingress Snippet Webhook Fix  Copy-paste ready. Works with Nous-Hermes 2, OpenHermes, or any ChatML-compatible model (Cursor, LM Studio, Ollama, etc.).  ---  ````text <|im_start|>system You are an expert Kubernetes and NGINX I…" — [[raw/2026-06-01-pieces-nginx-ingress-webhook-fix]] (Pieces: d01de85a-1e3f-4049-9b89-7db7ae06f70d)
> "The user wants me to create a "Hermes prompt" to investigate and fix the NGINX Ingress admission webhook issue described. A "Hermes prompt" typically refers to a prompt formatted for use with the Hermes/Nous-Hermes model family, or more generally, a…" — [[raw/2026-06-01-pieces-nginx-ingress-webhook-fix]] (Pieces: e5500e50-e1fb-47e8-b6b2-9a37ce280806)
> "give me a hermes prompt to investigate and fix this This is coming from the **NGINX Ingress admission webhook**, not ArgoCD itself. Argo is just surfacing the failure during the sync.  ### What the error means  ``` admission webhook "validate.nginx.i…" — [[raw/2026-06-01-pieces-nginx-ingress-webhook-fix]] (Pieces: 43a78b56-55a4-4e96-a5f6-b615de3f741f)

- **2026-06-01T11:23** — > "User asked for jumpbox commands to validate and fix FTFL-512 — basic curl to https://sandbox-testing-1.fitfile.net still returns a 302 page exposing nginx in the HTML body." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: dbf29a64-38dd-46fb-b92a-ac7c3af5625a)

- **2026-06-01T11:36** — > "Validation commands run on jumpbox: `curl -s sandbox-testing-1.fitfile.net | grep -i nginx` still returns `<hr><center>nginx</center>`. The `app-root` annotation IS present on the ingress but `server-..." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: 11e0242f-0166-4198-8486-38f23c4f7e76)

- **2026-06-01T11:38** — > "Status: partially fixed, one step remaining. The `app-root` annotation is present but `server-tokens` in the configmap is not yet set. The `<center>nginx</center>` body disclosure persists in 302 resp..." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: 94fe262d-a644-4cad-ba5b-4664c635be2f)

- **2026-06-01T11:39** — > "User asked what `server-tokens` means and whether it can safely be disabled. Answer: `server_tokens` controls whether nginx includes its identifier in response headers and HTML error/redirect bodies. ..." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: 37e4252f-1b8e-45e5-a1e3-1908d114b3fd)

- **2026-06-01T11:43** — > "Full explanation of server-tokens: when enabled, nginx sends `Server: nginx/<version>` in headers and includes `<center>nginx</center>` in default error/redirect HTML bodies. Purely informational for ..." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: b7816631-94ba-435b-af95-1f5886a61ef8)

- **2026-06-01T11:46** — > "User shared the Helm ingress template config and asked where to add the `server-snippet` annotation with `server_tokens off`. The template has three Ingress resources: the main ingress, the range-loop..." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: ff90d29d-0696-4efa-a944-6f8dc178b886)

- **2026-06-01T11:47** — > "Fix location identified: the `nginx` body disclosure comes from the **default ingresses** (those with `app-root: /fitfile`). `server-snippet` must be added to BOTH the main ingress and the `range .Val..." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: e99767e1-9ec2-4b14-aecf-ae77bbd5d128)

- **2026-06-01T11:47** — > "Specific YAML fix: add `nginx.ingress.kubernetes.io/server-snippet: |\n    server_tokens off;` to the annotations block of both the main Ingress and the range-loop default Ingress resources." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: 2c6b661d-0d98-4f6c-95b9-e3594046a56e)

- **2026-06-01T12:13** — > "User pushed changes and moved the `sandbox-testing-1-latest-release` tag. The curl test still shows nginx in the response. Investigation ongoing to determine if it is an ArgoCD sync issue, ingress rel..." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: 06b78766-90fd-4f6b-b3f5-e23d13acf69b)

- **2026-06-01T12:14** — > "User ran validation steps on jumpbox. ArgoCD sync status needs checking: commands provided to verify if the new tag was picked up, and if server-snippet annotations are on the live ingress object." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: 60badcff-4999-4358-8c53-7f023c94ad89)

- **2026-06-01T12:17** — > "Critical finding: ArgoCD synced to commit `151c64128c6eebe28fe13815cca4da7e541bd37d`. BUT the live ingress object `sandbox-testing-1-frontend-frontend-c3d91-default-ingress` shows `kubectl.kubernetes...." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: bab966f6-3980-4567-abcf-d58cd217c102)

- **2026-06-01T12:20** — > "Diagnostic commands provided: check ArgoCD app sync status, describe the live ingress for server-snippet, check controller configmap for server-tokens setting, verify controller has reloaded nginx con..." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: ffc75310-6d32-4b29-9649-13e2746265e9)

- **2026-06-01T12:48** — > "User asked for the kubectl command to force-sync ArgoCD (no argocd CLI available). ArgoCD app `sandbox-testing-1-frontend` is `OutOfSync Healthy`." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: 39e1c8d2-a946-4dd8-94a3-06f8b88e96db)

- **2026-06-01T12:49** — > "kubectl force-sync command: `kubectl patch application sandbox-testing-1-frontend -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"kubectl"},"sync":{"syncStrategy":{"force":{}},"rev..." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: 1560b425-47d6-4bc6-a3ba-7ed113b695be)

- **2026-06-01T12:51** — > "Jumpbox kubectl exec into ingress-nginx controller confirms `server_tokens off;` is set in `/etc/nginx/nginx.conf` at the controller level. But the `<center>nginx</center>` body still appears in curl ..." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: 6cf288db-865a-4fb9-bb4a-75c87ebdee17)

- **2026-06-01T12:51** — > "Patch command returned a warning (unknown field `operation.sync.syncStrategy.force`) but may have partially worked. The `server-snippet` annotation is not appearing on the live ingress object after sy..." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: fcd6c4c2-f39a-4b92-8075-0c49230645e2)

- **2026-06-01T12:54** — > "Critical GitLab finding: MR !784 "FTFL-512 Disables NGINX server tokens" was merged into master (https://gitlab.com/fitfile/deployment/-/merge_requests/784). A second open MR !785 also exists." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: 2c92d73e-edb4-4e3f-b92c-229c5c677980)

- **2026-06-01T12:59** — > "User pasted ArgoCD app output: `sandbox-testing-1-frontend OutOfSync Healthy`. After kubectl patch force-sync, the app is still OutOfSync and `server-snippet` annotation is not on the live ingress (gr..." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: 0b62d657-a52e-4bc5-8360-fb111fa1c82a)

- **2026-06-01T13:07** — > "Commit `a8405351` contains the change replacing `server_tokens off` with `server_tokens ""` in the server-snippet annotation. User asked: why is ArgoCD OutOfSync and what can be done?" — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: d54b2256-513f-465b-ba50-1cde141c238a)

- **2026-06-01T13:07** — > "Diagnostic commands provided: check ArgoCD sync revision vs tag, diff live vs desired state, force self-heal, check operation state." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: 4380cec7-cf76-4be2-93e1-18c9780f4b1a)

- **2026-06-01T13:11** — > "Jumpbox session (captured 14:02 BST) shows the full sequence of kubectl commands run, including annotation and patch attempts, all still leaving the app OutOfSync. Root issue: the server-snippet annot..." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: 248a4007-b72a-4cdd-bd99-b932818133d1)

- **2026-06-01T13:29** — > "Current ArgoCD sync revision: `a8405351e4b8c0da55c2aff9b03913840e4dcf0d`. The app is syncing to the commit with the server_tokens change but the webhook rejects the server-snippet annotation, keeping ..." — [[raw/2026-06-01-pieces-argocd-ingress-investigation]] (Pieces: ecb0cc97-2811-41ff-a6c4-5af9f739a9de)





## Timeline

- **2026-06-01T08:38** — ingress-nginx helm chart version 4.14.1 / app 1.14.1 confirmed on cluster
- **2026-06-01T08:53** — DNS-only propagation confirmed; `dig sandbox-testing-1.fitfile.net` returns `20.117.146.221` (Azure LB, no Cloudflare); FTFL-511 TLS remediation confirmed ✅
- **2026-06-01T11:23** — User requested jumpbox commands to validate FTFL-512 fix; curl still showing nginx body disclosure
- **2026-06-01T11:36** — Validation confirmed: `app-root` annotation present but `server-snippets` not on live ingress, `server-tokens` not in controller configmap
- **2026-06-01T11:46** — User identified Helm template location; fix identified: add `server-snippet` to both main and default ingress blocks
- **2026-06-01T12:13** — User pushed changes and moved `sandbox-testing-1-latest-release` tag; curl still shows nginx disclosure
- **2026-06-01T12:17** — Critical finding: ArgoCD synced to commit `151c6412` but `server-snippet` annotation NOT on live ingress object despite being in Git
- **2026-06-01T12:48** — User requested kubectl force-sync command (no argocd CLI available); app is `OutOfSync Healthy`
- **2026-06-01T12:51** — kubectl exec into controller confirms `server_tokens off` in nginx.conf at controller level, but body disclosure persists in ingress redirect responses
- **2026-06-01T12:54** — MR !784 "FTFL-512 Disables NGINX server tokens" confirmed merged; MR !785 also open
- **2026-06-01T12:59** — After force-sync patch, app still OutOfSync; `server-snippet` annotation not appearing on live ingress
- **2026-06-01T13:07** — Commit `a8405351` contains `server_tokens ""` change (modified from `server_tokens off`); user asked why ArgoCD still OutOfSync
- **2026-06-01T13:11** — Jumpbox session reviewed: full sequence of kubectl commands all left app OutOfSync; webhook blocking server-snippet confirmed as root cause
- **2026-06-01T13:29** — ArgoCD sync revision is `a8405351e4b8c0da55c2aff9b03913840e4dcf0d`; webhook rejection keeping app in permanent OutOfSync state
- **2026-06-01T13:31** — **Root cause confirmed**: admission webhook explicitly blocking `server-snippet` annotations cluster-wide; `allow-snippet-annotations` is `false`
- **2026-06-01T14:45** — User requested Hermes prompt to investigate and fix the webhook issue; prompt created with IaC-only constraint
- **2026-06-01T14:48** — IaC-only constraint locked: Hermes cannot directly interact with cluster (private network); must modify Helm charts/Kustomize/YAML in Git and let ArgoCD sync

## Connections

- [[FTFL-511 Nginx HTTPS Hardening]] — related NGINX Ingress hardening workstream
- [[FTFL-512 Nginx Security]] — companion ticket for nginx server_tokens information disclosure (same ingress)
- [[Azure AKS Backup — FTFL]] — same FTFL project family, ArgoCD-based deployment
- [[FITFILE Testing Infrastructure]] — sandbox-testing-1 environment
- [[ArgoCD]] — deployment tool surfacing the webhook rejection


## Contradictions

None identified.


## Open Questions

- Which Ingress manifests need the `server-snippet` annotation? (Answer: both the main ingress and the `range .Values.ingress.hosts` default ingress blocks in the frontend Helm chart)
- Is the fix to remove snippet annotations, replace them with whitelist-safe alternatives, or reconfigure the Ingress Controller to allow snippets? (Answer: MR !784 already merged with `server_tokens ""` approach; still blocked by webhook)
- What is the exact FTFL ticket reference? (FTFL-512 — Nginx Security — server tokens information disclosure)
- Why does ArgoCD remain OutOfSync after force-sync patch? (The webhook rejects the server-snippet; ArgoCD keeps trying to apply the rejected manifest)
- Should the controller-level `allow-snippet-annotations` be reconfigured to `true` as a cluster-wide setting, or should the IaC be rewritten to avoid snippet annotations entirely?
