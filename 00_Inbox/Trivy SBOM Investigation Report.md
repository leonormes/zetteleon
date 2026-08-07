---
created: 2026-08-06T15:25:36+01:00
modified: 2026-08-06T14:27:42+00:00
permalink: llmeon/00-inbox/trivy-sbom-investigation-report-august-6-2026
title: Trivy SBOM Investigation Report
type: note
---

## Trivy / SBOM investigation—report

Generated: Thu Aug 6 2026, 15:25 BST—Claude Code session in the `deployment` repo (`/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/deployment`).

Context: Robin needs SBOMs (npm + Python packages) for frontend/fitconnect/ffcloud, but trivy-operator wasn't producing them. Investigated live via `kubectl`/`helm` against the actual clusters, then traced the root cause into IaC and fixed it.

---

### How Trivy Actually Works

Trivy is a static, offline filesystem scanner—it never executes the container. `trivy-operator` runs it as a Kubernetes Job per workload that pulls the image and inspects the merged filesystem across all layers.

- OS packages: reads the distro package DB (dpkg/rpm/apk).
- Node.js packages: parses `package-lock.json` (or `yarn.lock`/`pnpm-lock.yaml`) when present in the final image layer. This file records the _fully resolved_ dependency tree—not just top-level `package.json`—so a vulnerable package pulled in only as a transitive dependency (e.g. `ip@2.0.0` required by some other library, not by the app directly) is still caught, at its exact resolved version and exact `node_modules` path.
- No lockfile in the final image (common with slim/distroless multi-stage builds)? Falls back to reading each installed package's own `node_modules/<pkg>/package.json` `"version"` field off disk—still works, slightly less provenance.
- Every discovered package+version is matched against Trivy's offline vulnerability DB (GHSA/NVD/OSV/npm advisories), pulled periodically as an OCI artifact.
- Matches land as a `VulnerabilityReport` CR (one per container per workload): `resource` (package name), `installedVersion`, `fixedVersion`, `vulnerabilityID`, `severity`, `target`/pkgPath. Real example pulled live from staging (`argocd` namespace):

  ```json
  {
    "resource": "libcurl3t64-gnutls",
    "installedVersion": "8.14.1-2ubuntu1.3",
    "fixedVersion": "8.14.1-2ubuntu1.4",
    "vulnerabilityID": "CVE-2026-8925",
    "severity": "MEDIUM"
  }
  ```

- SBOM is a separate `SbomReport` CR per container—full CycloneDX/SPDX document listing every component (name, version, PURL, license), vulnerable or not. `ip@2.0.0` → `pkg:npm/ip@2.0.0`. Enabled uniformly across all ecosystems by one Helm value, `trivy.sbom.enabled: true`—no separate npm vs Python toggle.

### What Was Actually Found on the Clusters

- Not managed via the `deployment` GitLab repo or ArgoCD on either cluster—confirmed by repo-wide grep and `kubectl get applications -n argocd | grep trivy` (empty both places).
- `fitfile-cloud-testing-aks-cluster` ("sandbox-testing"—frontend/fitconnect/ffcloud all run here, in one shared namespace called `testing`, not separate per-app namespaces as first assumed): `trivy-system` was completely empty—no Deployment, no Helm release. CRDs existed (installed 2024-10-29) with stale reports frozen at 614–646 days old—the operator scanned nothing since and was later removed, with no trace in any IaC repo.
- `fitfile-cloud-staging-aks-cluster`: trivy-operator was actively running (Helm release, chart `trivy-operator-0.30.0`, revision 17, last upgraded 2025-09-03), watching all namespaces, SBOM generation on. But this cluster's own `testing` namespace has zero pods—the app workloads don't run here.
- Root cause: the working operator and the target workloads were on two different clusters—not a namespace-exclusion config bug.
- Leon's decision: trivy is staging-only; the testing-cluster gap is intentionally not being fixed.

### IaC Root Cause + Fix

Found in the separate Terraform repo `fitfile-non-production-infrastructure` (`Clusters/FITFILE/Non-Production/`):

- `staging-cluster-2/main.tf` declares trivy-operator as a real `helm_release` Terraform resource (namespace, chart, ClusterRoleBinding).
- `testing-cluster/main.tf` has no such block at all—confirms trivy was never codified for that cluster.
- Drift found: the live Helm release (revision 17) had `trivy.sbom.enabled`, `trivy.timeout`, `operator.scannerReportTTL`, `operator.vulnerabilityScannerScanOnlyCurrentRevisions`, and `serviceMonitor.enabled` set—none of which existed in `staging-cluster-2/main.tf`'s values block. Someone had run a manual `helm upgrade` directly against the cluster, bypassing Terraform. A future `terraform apply` would have silently reset SBOM generation to disabled.
- Fix applied this session: edited `staging-cluster-2/main.tf` to add the missing values so Terraform now matches what's live. Change is local-only, uncommitted, in that repo as of end of session—not yet decided whether to commit/open an MR.

### Open Items

- Whether/when the staging Terraform fix gets committed and merged.
- Whether the old testing-cluster install (removed ~600+ days ago) was ever intentional, or quietly broke unnoticed—no record exists in any IaC repo to check.

Related: fuller version with citations written to the Hermes vault: `wiki/reference/Trivy & SBOM Scanning.md` (source: `raw/2026-08-06-trivy-sbom-investigation.md`).
