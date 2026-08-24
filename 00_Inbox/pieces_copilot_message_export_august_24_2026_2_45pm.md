---
title: pieces_copilot_message_export_august_24_2026_2_45pm
type: note
permalink: llmeon/00-inbox/pieces-copilot-message-export-august-24-2026-2-45pm
---

*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Monday Aug 24, 2026 - 2:45 PM*
---
## What Kubescape does

**Kubescape** is an open-source Kubernetes security platform (CNCF, maintained by ARMO) that scans clusters, manifests, Helm charts, code repos, and container images to catch three categories of risk:

- **Configuration scanning** — Kubernetes manifests, YAML, and Helm charts for insecure settings and policy violations.
- **Vulnerability scanning** — known CVEs in container/workload images.
- **Compliance and risk posture** — mapped against frameworks like NSA-CISA, MITRE ATT&CK, and CIS Benchmarks, plus continuous cluster posture management and (in newer versions) runtime threat detection.
- **CI/CD integration** — so checks run pre-deployment, not just in the live cluster.

In short, it answers two questions: "Is my Kubernetes setup misconfigured?" and "Do the containers I'm deploying carry known CVEs?"

## How it maps onto your current CVE work

Your CVE/vulnerability-management work right now centers on the `FTFL-865` epic ([Vulnerability Management - Jira](https://fitfile.atlassian.net/browse/FTFL-865)), which tracks the remediation roadmap from the "Vulnerability Management for Containerized Node.js/Python Workloads on AKS" report, and a large volume of day-to-day CVE patch MRs (`black` → `v26` for `CVE-2026-31900`/`CVE-2026-32274`, `cryptography` → `v50`, `pyarrow` → `23.0.1` for `CVE-2026-25087`, etc.).

The stack you're currently running, per that epic and the surrounding events:

- **Trivy Operator** — image + workload CVE scanning, feeding the [Trivy Vulnerabilities dashboard](https://fitfiletest.grafana.net/d/security_trivy_operator/trivy-operator-vulnerabilities) in Grafana.
- **Renovate** — dependency-bump automation opening the SECURITY-tagged MRs.
- **VEX repository** — a private [`vex-repository`](https://gitlab.com/fitfile/vex-repository) conforming to `aquasecurity/vex-repo-spec`, used to suppress false positives on packages you've assessed as not-affected.
- **Gatekeeper** — currently audit-only, with `FTFL-859` tracking a move to phased enforcement.

Notably, the `FTFL-865` epic's corrected notes explicitly flag a gap: *"Cosign. There is no scanner in any pipeline anywhere in the estate"* — i.e., no image-signing/provenance check, and the epic's related tickets (`FTFL-861`: CI-stage image signing + SBOM/provenance attestation; `FTFL-858`: standardize scanning/policy config via GitOps) point at exactly the kind of IaC/manifest/compliance coverage Kubescape provides. That's also reflected in the scanner comparison table you built in `fitfile-vuln-mgmt-research`, which lays out SCA/CVE scanners against columns for "K8s-native scanning," "IaC/misconfig," "Secrets scanning," and "SBOM" — Trivy covers most of those, but Kubescape's specific strength is the **NSA-CISA/MITRE/CIS compliance posture layer** and **Helm/manifest misconfig scanning**, which isn't something Trivy is primarily built for.

**Would it complement the current work?** Yes, in a specific way rather than as a Trivy replacement:

- **Trivy** stays your CVE/image-vulnerability engine (that's its strength and it's already deeply wired into your Grafana dashboards, VEX repo, and CI).
- **Kubescape** would fill the adjacent gap your own epic already identified — Kubernetes manifest/Helm misconfiguration scanning and compliance-framework mapping (CIS/NSA-CISA/MITRE ATT&CK) — which is currently unaddressed ("no scanner in any pipeline anywhere in the estate" for that category).
- Running both is a fairly standard "SCA/image scanner + K8s posture scanner" pairing, and would directly support the phased-enforcement direction you're already headed with Gatekeeper.

One caveat: I didn't find any memory event where Kubescape was evaluated head-to-head against your existing tools (e.g., in the scanner-comparison note) or where a decision was made about adopting it — the hints matched tickets in the `FTFL-865` epic thematically, but I don't have direct evidence you've already scoped Kubescape specifically. If you want, I can pull the full `fitfile-vuln-mgmt-research` comparison table content to check whether Kubescape is already on that shortlist.