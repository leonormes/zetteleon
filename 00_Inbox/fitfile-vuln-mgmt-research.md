---
created: 2026-08-07T15:12:01+00:00
modified: 2026-08-08T08:48:28+00:00
permalink: llmeon/00-inbox/fitfile-vuln-mgmt-research
title: fitfile-vuln-mgmt-research
type: note
---

## Vulnerability Management for Containerized Node.js/Python Workloads on AKS

### Working Assumption on Scope

Namespace and component naming referencing OMOP/OHDSI and an NHS "mesh-mailbox" strongly suggests integration with NHS MESH (the NHS's secure messaging transport used across primary care, secondary care, and social care), and downstream analytics against the OMOP Common Data Model, an OHDSI standard widely used for observational health research on de-identified or pseudonymised patient-level data. This report treats NHS supplier-framework applicability (DSPT, DTAC, Cyber Essentials Plus, DCB0129/DCB0160) as an unconfirmed hypothesis and calls out, in a dedicated section, exactly where those frameworks would raise the bar versus general industry practice—this determination should be validated against FitFile's actual data processing agreements and NHS Digital Technology Assessment Criteria (DTAC) submission status, not inferred from infrastructure names alone.[^1][^2]

*

### A. Maturity Assessment of the Current Setup

FitFile's vulnerability management program sits at what is commonly described as "detect-only" maturity: a single, capable, in-cluster scanner with good visibility, but no gating, no remediation automation, and no supply-chain integrity controls. This is a coherent starting point but is behind where a health-data-adjacent platform team with production NHS-facing workloads should be in 2026.

| Dimension | Current state | Industry norm for this profile |
|---|---|---|
| Scanning stage | Post-deployment only, in-cluster (trivy-operator) | Layered: pre-commit/CI gate + registry/admission + runtime[^3][^4] |
| Remediation loop | Manual jq/Python cross-referencing SbomReport ↔ VulnerabilityReport | Automated: scanner findings drive dependency-bump PRs with SLA triage[^5][^6] |
| Policy enforcement | Gatekeeper installed, audit/dry-run only | Progressive dryrun → warn → deny per policy, per environment[^7][^8][^9] |
| Supply chain integrity | None (no image signing, no provenance, no SHA-pinned Actions) | Baseline expected in 2026: cosign signing + SBOM/provenance attestation, admission-verified[^10][^11] |
| SBOM handling | CycloneDX, retained only as in-cluster CRDs | Growing expectation of an external, retained, exportable SBOM store or attestation registry[^12][^13][^14] |
| Multi-environment consistency | Staging apparently best-instrumented; prod/testing parity unconfirmed | Identical scanning/policy config across environments via GitOps templating[^15] |
| IaC hygiene for the tooling itself | Recurring Helm-values drift, manual `helm upgrade`s bypassing Terraform | Declarative, drift-detected, single source of truth (Terraform/ArgoCD, no live edits)[^15] |

The single most urgent gap is not a missing tool—it's the complete absence of a shift-left gate. Every vulnerability trivy-operator finds today has already been running in production for some unknown period before anyone looks at a dashboard. That is a materially different risk posture than catching the same CVE in a PR.

A second urgent point, orthogonal to the maturity roadmap below: Trivy's supply chain was itself compromised in March 2026 (CVE-2026-33634), when threat actors force-pushed malicious commits into 76 of 77 `aquasecurity/trivy-action` tags and all `aquasecurity/setup-trivy` tags, and published a backdoored `trivy` binary (v0.69.4) and compromised Docker Hub images (v0.69.4–v0.69.6), designed to exfiltrate Kubernetes secrets, cloud credentials, and CI/CD tokens. This is directly relevant to FitFile because it just granted trivy-operator Workload Identity + AcrPull permissions—a credential now sitting inside the exact class of tool that was weaponized. Regardless of which scanner is chosen going forward, any CI-stage Trivy usage must pin to commit SHAs, not tags, and the currently-running trivy-operator Helm chart version and image digest should be audited against the safe-version table (trivy ≥v0.69.7 confirmed clean, or any pre-v0.69.4 release; `trivy-action` pinned to v0.35.0 or a SHA).[^16][^17][^18][^19][^20]

*

### B. Prioritized Recommendations

Ordered by impact-to-effort ratio, assuming a small platform team with no dedicated security engineer.

#### Tier 1—do in the next Sprint (Low eFfort, hIgh iMpact)

1. Audit and pin the existing Trivy supply chain. Confirm trivy-operator's chart/image version is not in the compromised window; if any CI workflows reference `trivy-action`/`setup-trivy` by tag, pin to SHA immediately. _Effort: hours. Impact: closes an active, disclosed credential-theft vector._[^17][^21]
2. Add a CI-stage SCA gate using the same Trivy binary you already operate, rather than introducing a second tool. Run `trivy fs`/`trivy image` in the CI pipeline for both Node.js and Python repos, gated on `--severity HIGH,CRITICAL --exit-code 1 --ignore-unfixed`. This is the cheapest way to close research question 2 (shift-left vs in-cluster) without a new tool to operate. _Effort: 1–2 days per repo template. Impact: high—moves detection from "already deployed" to "before merge."_[^22][^3][^4]
3. Wire Renovate's OSV-based vulnerability alerts (`osvVulnerabilityAlerts: true`) now, rather than leaving Renovate as a disconnected adjacent workstream. Renovate queries OSV.dev for npm and PyPI direct dependencies specifically (both of FitFile's stacks are covered datasources) and opens vulnerability-fix PRs automatically once a fix is available—this is the single fastest way to partially automate the "package needs updating" list FitFile currently builds by hand, though it only covers _direct_ dependencies, not everything Trivy's SBOM-based approach sees. _Effort: config change, half a day. Impact: high—directly targets the manual jq/Python process called out as the main operational pain point._[^5][^6]
4. Keep the manual Trivy-SBOM-cross-reference process running in parallel, but script it into a scheduled job that opens or updates a tracking issue/PR per fixable CVE, rather than a one-off jq exercise. This is a bridge until item 6 below is built out. _Effort: 1 day. Impact: medium—converts tribal process into a repeatable artifact._

#### Tier 2—next 1–2 Quarters (Moderate eFfort, hIgh sTrategic iMpact)

1. Progress Gatekeeper from audit-only to a phased enforcement path, following the standard dryrun → warn → deny progression rather than flipping to deny directly. Concretely: pick a small number of CVE-severity-based constraints (e.g., block CRITICAL images with a known fix available, using a custom Rego constraint that queries the `VulnerabilityReport` CRD or an OPA data source fed by Trivy's exported findings), leave them in `dryrun` for 1–2 weeks per cluster to establish a violation baseline, then `warn`, then `deny`—staging first, then testing, then production, with a defined grace period (e.g., 14 days from disclosure) before `deny` triggers, and an exception mechanism (time-boxed annotation-based waiver, audited). _Effort: 2–4 weeks incl. testing. Impact: high—this is the actual "admission-time" layer research question 4 asks about, and it is the natural next step given Gatekeeper is already installed._[^7][^8][^9][^23]
2. Build the automated remediation loop: a small scheduled job (CronJob or Argo Workflow) that reads `VulnerabilityReport`/`SbomReport` CRDs, filters to entries with non-empty `fixedVersion`, and either (a) opens a GitHub issue tagged by severity/SLA, or (b) triggers a targeted Renovate run scoped to just that package (Renovate supports on-demand/dependency-specific triggering). This directly answers research question 3: rather than running Renovate and Trivy as disconnected tools, Trivy's fixedVersion output becomes an input that prioritizes _which_ Renovate PRs matter most, while Renovate's OSV alerts independently catch anything Trivy's SBOM matching misses. _Effort: 1–2 weeks. Impact: high—this is the most named gap in the current-state section of the brief._
3. Add CI-stage image signing with cosign (keyless/Sigstore) and SBOM/provenance attestation, then verify signatures at admission via Gatekeeper (with the Ratify data-source add-on) or a lightweight complementary Kyverno/Sigstore policy-controller deployment scoped only to image-verification. Since FitFile already builds its own base images and controls its private ACR, this is a comparatively low-friction win: sign at push time, verify at pull time, deny unsigned images from anywhere but the internal registry. _Effort: 1–2 weeks. Impact: medium-high—closes the "who can push to our registry and have it run" gap, which matters more once a CI gate exists to sign against._[^10][^24][^11][^25]
4. Fix the metrics cardinality/cost trade-off deliberately rather than accepting the newly-enabled per-CVE-ID metric as-is. Keep `metricsVulnIdEnabled` on for a short, defined "deep dive" dashboard used during incident triage, but build a severity-tier recording rule (critical/high/medium/low counts per namespace/workload, dropping the CVE-ID label) as the primary always-on dashboard, following standard Prometheus recording-rule practice of aggregating away high-cardinality labels while preserving the dimensions actually queried. _Effort: 2–3 days. Impact: medium—prevents the cardinality cost from growing unbounded as more workloads and CVE-IDs accumulate._[^26][^27][^28][^29]
5. Standardize scanning/policy config across staging, testing, and production via a single GitOps template (ArgoCD ApplicationSet or Helm values inheritance) rather than per-cluster manual configuration, explicitly addressing research question 9. Use a base `values.yaml` plus per-environment overlay, with ArgoCD's diff/self-heal surfaced as an alert on drift. _Effort: 1 week. Impact: high—directly prevents the "staging is the only well-instrumented environment" failure mode._[^15]

#### Tier 3—ongoing Hygiene / Evaluate Opportunistically

1. Prevent the Helm-values-schema drift failure mode specifically for security tooling by treating the trivy-operator (and Gatekeeper) Helm releases exactly like any other Terraform-managed Helm release: pin exact chart version and values schema in a Terraform Cloud workspace, use `helm template` + `diff` in CI as a pre-merge check against the live chart schema, and hard-block manual `helm upgrade` via RBAC (remove interactive `helm upgrade` permission from human users on these namespaces, leaving only the CD service account write access). This is the concrete answer to research question 10: the drift problem is not really about Helm, it's about who has write access outside GitOps—restricting that is more durable than any values-file tooling fix.
2. Evaluate distroless/Chainguard-style minimal base images for the Node.js and Python services. Given FitFile already builds and controls all base images via a private registry, this is a low-friction, high-value move: fewer OS packages means fewer CVEs Trivy has to report in the first place, directly reducing the volume the manual/automated triage pipeline has to process. Treat as opportunistic per-service migration, not a big-bang project—pick the highest-CVE-count service first as a pilot.
3. Consider adding Grype as a second opinion on a subset of critical-path images, not as a wholesale replacement for trivy-operator. Independent 2026 benchmarks show Trivy and Grype agree on roughly 95% of findings, diverge mainly on database refresh lag (Trivy refreshes every ~6h vs Grype ~12h) and on backport-patch false positives (Trivy is more inclusive, generating ~18% more findings, of which ~60% turn out to be false positives from backport-patched packages without version bumps). Running both on a defined critical subset—rather than everywhere—captures the "multi-scanner strategies reduce false negatives 15–25%" benefit cited in recent comparative studies without doubling operational load across the whole fleet.[^30][^31][^32]

*

### C. Tool Comparison Tables

#### SCA/CVE Scanners for Node.js + Python Containers

| Tool | Maintainer | K8s-native scanning | IaC/misconfig | Secrets scanning | SBOM | Risk scoring (EPSS/KEV) | Cost | Fit for FitFile |
|---|---|---|---|---|---|---|---|---|
| Trivy / trivy-operator | Aqua Security | Yes—native CRDs (already deployed)[^22][^4] | Yes (Terraform, K8s, Dockerfile)[^33][^30] | Yes | Generates + consumes CycloneDX/SPDX[^30] | No (CVSS severity only)[^30] | Free (Apache 2.0) | Already invested; keep as primary; must be version-pinned post-CVE-2026-33634[^17] |
| Grype + Syft | Anchore | No native cluster scanning[^30][^34] | No | No | Syft-generated, reusable across pipeline[^30][^34] | Yes—composite CVSS+EPSS+KEV score[^30][^35] | Free (Apache 2.0) | Good complementary second-opinion tool for critical images; not a cluster-scanning replacement |
| Snyk | Snyk (commercial) | Limited | Separate product | No (via other Snyk products) | Yes | CVSS + reachability analysis[^35] | Free tier / paid | Best fix-suggestion UX; consider for curated remediation review layer, not primary gate |
| Docker Scout | Docker | No | No | No | Docker-native SBOM | CVSS only | Freemium | Marginal added value given ACR (not Docker Hub) is the registry of record |
| GitHub Advanced Security / Dependabot | GitHub | No | Code scanning (CodeQL) | Yes (secret scanning) | Via dependency graph | GitHub Security Advisories | Included with GHAS | Strong PR-native remediation UX if FitFile's repos are on GitHub; complements Renovate rather than replacing it |
| JFrog Xray | JFrog (commercial) | No | Yes | Limited | Yes | CVSS + custom policies | Paid | Only justified if FitFile adopts JFrog Artifactory; not indicated by current stack |
| Wiz | Wiz (commercial) | Yes (agentless, cloud-native) | Yes, broad CSPM | Yes | Yes | Yes, contextual/graph-based | Enterprise paid | Overkill relative to team size/budget; revisit only if NHS supplier audit requires a commercial CNAPP with formal SLAs |

Where teams commonly run more than one tool, and why: the recurring pattern in 2026 comparative benchmarks is _not_ "replace Trivy," it's layering by pipeline stage—a fast, broad tool (Trivy) in the tight CI feedback loop, a precision-oriented SBOM-first tool (Grype+Syft) at a compliance/release gate, and a commercial curated-remediation tool (Snyk) for developer-facing fix suggestions. Running two vulnerability databases in parallel also hedges against exactly the kind of single-vendor supply-chain compromise Trivy just experienced.[^32][^16]

#### Admission-time Policy Engines for Image Verification

| Controller | Policy language | Signature verification (cosign/notation) | Vuln/SBOM/attestation gating | Operational weight | Fit given existing Gatekeeper install |
|---|---|---|---|---|---|
| OPA Gatekeeper (+ Ratify) | Rego | Yes, via Ratify plugin | Via external data source | Medium (Rego learning curve) | Natural extension of current investment—no new component for basic policy |
| Kyverno | Declarative YAML | Native `verifyImages` | Native attestation checks | Low-medium | Simpler syntax; consider running alongside Gatekeeper scoped only to image verification if Rego proves painful[^11][^25] |
| Sigstore policy-controller | ClusterImagePolicy CRD | Native, keyless-first | Native (SBOM/provenance/vuln attestations) | Low, narrow scope | Good minimal add-on purely for signature/attestation enforcement[^11] |
| Native Kubernetes ValidatingAdmissionPolicy (CEL) | CEL | Basic, manual | Limited | Lowest (no extra component) | Worth using for simple rules to reduce Gatekeeper's Rego surface area |

#### SBOM Format Comparison

| Dimension | CycloneDX (current, via trivy-operator CRDs) | SPDX |
|---|---|---|
| Origin/standards body | OWASP; ECMA-424[^13] | Linux Foundation; ISO/IEC 5962:2021 (SPDX 2.2.1)[^13] |
| Strongest at | Vulnerability + VEX workflows[^12] | License compliance, broader legal/ISO recognition[^12][^13] |
| Native VEX support | Yes, since v1.4[^13] | Only via separate SPDX 3.0 spec work |
| Native document signature field | Yes (root JSF signature)[^14] | No normative in-document signature; needs external signing (e.g., cosign)[^14] |
| Recognized by | CISA SBOM minimum elements (2026), EU CRA, FDA cyber-device guidance—accepted equally alongside SPDX[^12][^13][^14] | Same frameworks, accepted equally |
| Verdict for FitFile | Keep CycloneDX (already produced by trivy-operator); it has the tighter fit for a vulnerability-first workflow and native VEX/signature support[^13][^14] | No compelling reason to add SPDX unless a specific customer/procurement contract requires it for license-compliance review |

*

### D. Does the Current CRD-based SBOM Approach Meet audit/evidence Requirements?

Storing SbomReport CRDs only inside the cluster is workable for internal engineering purposes but is not the same thing as an audit-ready evidence trail, for two structural reasons. First, CRDs are ephemeral relative to cluster lifecycle—a cluster rebuild, namespace deletion, or CRD garbage-collection event destroys historical evidence, whereas frameworks and 2026 CISA/CRA guidance expect SBOMs to be retained, versioned, and tied to a specific build/release, not just to a currently-running workload. Second, in-cluster CRDs are not independently signed or attested; they represent "what the operator observed," not a cryptographically verifiable claim about "what was built and by whom." Emerging practice—Sigstore/cosign attestations recorded to the public Rekor transparency log, or an in-toto provenance chain—exists precisely to close that gap, producing artifacts that survive cluster teardown and can be independently verified by a third party (auditor, customer, regulator) without needing cluster access. For FitFile, the pragmatic move is not to abandon the CRD approach (it's genuinely useful for live-cluster CVE triage) but to add a build-time step that also attaches the CycloneDX SBOM as a cosign attestation on the image in ACR, giving a durable, portable record independent of any given cluster's uptime.[^12][^14][^36][^37][^24][^10]

*

### E. NHS/UK Healthcare-specific Callouts (Contingent on sCope cOnfirmation)

These items apply only if FitFile is confirmed to be in scope for NHS supplier frameworks as an IT Supplier or "Other"-category organisation with access to NHS patient data—a status that should be confirmed against actual data-processing agreements rather than inferred from naming conventions.

- DSPT vulnerability management outcome (B4.d) requires a _documented_ process covering: receiving/tracking/analysing vulnerabilities across all software packages and systems supporting the essential function; risk-based prioritisation; mitigation of externally-exposed vulnerabilities within a defined timeframe; a documented policy on which severities may receive temporary mitigation and for how long before full remediation is mandatory; and defined-frequency scanning. FitFile's current manual jq/Python triage process would need to become a written, defined-SLA policy document, not just a technical pipeline—DSPT assessors look for documented process as much as tooling. General industry practice (severity-based CVSS triage with informal SLAs) is not sufficient on its own; DSPT explicitly requires the _time-limits-with-compensating-controls_ structure for exceptions.[^38][^2]
- DSPT 2025-26 (version 8), effective 30 June 2026, adds a formal independent audit requirement covering 11 mandatory assertions for organisations classified as "IT Suppliers" (50+ employees and >£10m turnover)—assertion 6.3 covers vulnerability management specifically (addressing NHS Digital advisories and learning from past incidents), 8.3 covers patch management, and 8.4 covers network defence. If FitFile meets the IT Supplier size threshold, the current ad hoc process will not pass an independent audit; if FitFile is below that threshold it falls under the lighter-touch "Other" category self-assessment.[^39]
- DTAC requires, for any internet-facing or service-accessible product, a summary report of an external penetration test covering the OWASP Top 10 within the previous 12 months, and that report must demonstrate no vulnerabilities scoring CVSS 7.0 or above. This is a materially stricter bar than "block on critical" admission policy alone—it implies periodic third-party penetration testing as a complementary control to in-cluster/CI scanning, since Trivy/Grype-style SCA tools do not substitute for an application-layer pen test.[^1]
- Cyber Essentials Plus, if held, can exempt some DSPT evidence items from separate audit, provided its certification scope explicitly covers the systems processing health/care data—worth confirming scope alignment rather than assuming blanket coverage.[^39]
- Where NHS frameworks would change the recommendation vs. general industry practice: general industry guidance (this report's Tier 1/2 recommendations) is necessary but not sufficient for DSPT/DTAC—those frameworks additionally require (a) a written, board-visible vulnerability management policy document with defined SLAs and exception approval workflow, not just automation; (b) periodic external penetration testing, which no scanner discussed here provides; and (c) from 2025-26 onward, potentially an independent third-party audit of the whole program if FitFile meets the IT Supplier threshold. DCB0129/DCB0160 clinical risk management standards are a separate, higher bar again—relevant only if FitFile's software function is classified as a medical device or directly influences clinical decision-making, which is not established by the OMOP/OHDSI naming alone and needs a formal clinical safety classification exercise.

*

### F. Where Guidance is Genuinely Contested or Still Evolving

- Trivy vs Grype false-positive/false-negative trade-offs are actively debated in 2026 benchmarks: Trivy's more inclusive database yields better raw recall but a materially higher false-positive rate on backport-patched packages (roughly 60% of its "extra" findings in one 500-image study), while Grype's EPSS/KEV-based prioritization is seen by some as more actionable but by others as adding a dependency on external, sometimes-delayed exploit-probability feeds. There's no consensus "winner"—the split is genuinely workflow-dependent.[^31][^30]
- CycloneDX vs SPDX remains a live debate rather than a settled standard: both formats now satisfy essentially every major regulatory framework examined (CISA 2026 minimum elements, EU CRA, FDA cyber-device guidance), and the emerging expert consensus is that the choice is a _workflow_ fit question, not a compliance one.[^13][^14][^12]
- SLSA Level ambition is still evolving in practice—most 2026 guidance recommends targeting Level 2–3 as the realistic bar for most organizations, with Level 4 (hermetic builds, two-person review) considered aspirational rather than baseline-expected even for security-conscious teams[c10].[^24]
- Whether admission-time signature verification meaningfully reduces risk for teams that already fully control their own registry and build pipeline (as FitFile does) is disputed among practitioners: some treat it as essential defence-in-depth against a compromised CI credential or registry breach; others argue that if kubelet-level ACR pull auth and network policy already restrict image sourcing tightly, signing adds attestation/audit value more than it adds a new attack-surface reduction. Given FitFile just experienced exactly the kind of credential-exposure event (Trivy's compromised workload identity risk) that signature verification is designed to catch downstream of, the balance of evidence favours implementing it, but reasonable teams disagree on urgency versus the other Tier 1/2 items above.

---

### References

1. [DTAC form is available to download and print](https://transform.england.nhs.uk/media/documents/DTAC_Form_2.0_February_2026.docx)
2. [Strengthening Assurance –](https://www.dsptoolkit.nhs.uk/Help/Attachment/860)
3. [How to Scan Kubernetes with Trivy](https://oneuptime.com/blog/post/2026-02-02-trivy-kubernetes-scanning/view) - A hands-on guide to scanning Kubernetes clusters with Trivy for vulnerabilities, misconfigurations, …
4. [How to Use Trivy for Kubernetes Security](https://oneuptime.com/blog/post/2026-01-27-trivy-kubernetes-security/view) - A comprehensive guide to using Trivy and the Trivy Operator for Kubernetes security, covering vulner…
5. [Configuration Options¶](https://docs.renovatebot.com/configuration-options/) - Configuration Options usable in renovate.json or package.json
6. [is "vulnerabilityAlerts" for supported self-hosted renovate ...](https://github.com/renovatebot/renovate/discussions/15561) - I'm trying to use self-hosted renovate(v32.39) that can run part of our gitlab(v14.7.7 enterprise) C…
7. [🛡️ OPA Gatekeeper — How I Secured Kubernetes Deployments with Policy Enforcement](https://medium.com/@yagnesh03122002/%EF%B8%8F-opa-gatekeeper-how-i-secured-kubernetes-deployments-with-policy-enforcement-ec0fa88e27d8) - A practical guide to implementing OPA Gatekeeper for image registry control, label enforcement, repl…
8. [OPA/Gatekeeper Track Part 3: Audit, Mutation & Testing](https://www.wasilzafar.com/pages/series/distributed-systems-k8s/opa-gatekeeper-part03-audit-mutation-testing.html) - Gatekeeper audit mode, mutation policies with Assign/AssignMetadata, conftest for CI pipeline policy…
9. [OPA and Gatekeeper - Policy Enforcement for Kubernetes](https://www.k8s.guide/ecosystem/opa-gatekeeper/) - A deep guide to OPA Gatekeeper covering ConstraintTemplates, Constraints, Rego policies, mutation, d…
10. [SLSA + Sigstore: Software Supply Chain Security Architecture ...](https://iotdigitaltwinplm.com/slsa-sigstore-software-supply-chain-security-architecture-2026/) - SLSA and Sigstore explained: build provenance, keyless signing with Fulcio and Rekor, in-toto attest…
11. [Best Kubernetes Admission Controllers for Supply Chain ...](https://safeguard.sh/resources/blog/best-kubernetes-admission-controllers-for-supply-chain-security) - Compare the best Kubernetes admission controllers for supply chain security: Kyverno, OPA Gatekeeper…
12. [SBOM for Medical Devices: The 2026 FDA Pillar Guide](https://bluegoatcyber.com/guides/sbom-for-medical-devices) - What an SBOM is, why the FDA requires one under Section 524B, SPDX vs CycloneDX, how to generate and…
13. [CycloneDX vs SPDX: Picking Your CRA-Compliant SBOM ...](https://craevidence.com/cra-compliance/sbom/cyclonedx-vs-spdx) - 2026 CycloneDX and SPDX are the two formats that satisfy the CRA's machine-readable SBOM requirement…
14. [Mapping CISA's 2026 SBOM Minimum Elements to ...](https://runsafesecurity.com/blog/sbom-minimum-elements-cyclonedx-spdx/) - A field-by-field guide mapping CISA's 2026 SBOM minimum elements to CycloneDX and SPDX, with exact p…
15. [How to Implement Consistent Configuration Across ...](https://oneuptime.com/blog/post/2026-02-26-how-to-implement-consistent-configuration-across-clusters-with-argocd/view) - Learn how to maintain consistent configuration across multiple Kubernetes clusters with ArgoCD using…
16. [Guidance for detecting, investigating, and defending against the Trivy supply chain compromise | Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/03/24/detecting-investigating-defending-against-trivy-supply-chain-compromise/) - Threat actors abused trusted Trivy distribution channels to inject credential‑stealing malware into …
17. [The Trivy Supply Chain Compromise: What Happened and ...](https://www.legitsecurity.com/blog/the-trivy-supply-chain-compromise-what-happened-and-playbooks-to-respond) - Aqua Security's Trivy vulnerability scanner was compromised, exposing sensitive data. Learn how to r…
18. [Trivy ecosystem supply chain temporarily compromised](https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23) - ## Summary On March 19, 2026, a threat actor used compromised credentials to publish a malicious Tri…
19. [Trivy Compromised by "TeamPCP" | Wiz Blog](https://www.wiz.io/blog/trivy-compromised-teampcp-supply-chain-attack) - Breaking down the March 2026 Trivy supply chain attack. TeamPCP compromised trivy + trivy-action & s…
20. [Trivy supply chain compromise: What Docker Hub users should ...](https://www.docker.com/blog/trivy-supply-chain-compromise-what-docker-hub-users-should-know/) - On March 19, 2026, threat actors compromised Aqua Security's CI/CD pipeline and used stolen credenti…
21. [Breakdown of the Trivy supply chain compromise - timeline, who's affected, and remediation steps](https://www.reddit.com/r/kubernetes/comments/1s3pxcu/breakdown_of_the_trivy_supply_chain_compromise/) - Breakdown of the Trivy supply chain compromise - timeline, who's affected, and remediation steps
22. [Trivy Tutorial: Scan Containers in 12 Steps [2026] - Tech Insider](https://tech-insider.org/trivy-tutorial-2026/) - Trivy tutorial: scan container images, code, IaC and Kubernetes for CVEs and secrets in 12 steps, th…
23. [OPA Gatekeeper](https://www.cncf.io/wp-content/uploads/2020/08/CNCF-Webinar-OPA-Gatekeeper-Presentation-SHARED-EXTERNALLY.pdf) - Common best practices are enforced. Dry Run ● Allows constraints to be tested in a running cluster w…
24. [Supply Chain Security in 2026: SLSA, Sigstore, and... - Luca Berton](https://lucaberton.com/blog/supply-chain-security-slsa-sigstore/) - Secure your software supply chain with SLSA levels, Sigstore signing, and SBOM generation. Practical…
25. [Layer 3: Slsa (provenance)](https://lucaberton.com/blog/supply-chain-security-sbom-sigstore-slsa/) - Software supply chain attacks are surging. Here's how to implement SBOMs, container signing with Sig…
26. [How to manage high cardinality metrics in Prometheus and ...](https://grafana.com/blog/how-to-manage-high-cardinality-metrics-in-prometheus-and-kubernetes/) - You can learn more about reducing Prometheus recording rules and relabel configuration in the follow…
27. [How to Manage Metric Cardinality in Prometheus](https://oneuptime.com/blog/post/2026-01-25-prometheus-metric-cardinality/view) - Cardinality refers to the number of unique time series in your Prometheus database. Use recording ru…
28. [How to Optimize Prometheus Recording Rules to Reduce Query ...](https://oneuptime.com/blog/post/2026-02-09-optimize-prometheus-recording-rules-latency/view) - Discover advanced techniques to optimize Prometheus recording rules and achieve up to 90 percent red…
29. [Recording rules](https://prometheus.io/docs/practices/rules/) - Prometheus project documentation for Recording rules
30. [Trivy vs Grype (2026): Container Security Compared](https://appsecsanta.com/sca-tools/trivy-vs-grype) - Trivy covers more ground—it scans for vulnerabilities, IaC misconfigurations, secrets, and license…
31. [Trivy vs Grype: A Buyer Comparison for 2026](https://safeguard.sh/resources/blog/trivy-vs-grype-buyer-comparison-2026) - Trivy produced about 18% more findings than Grype, and after triage, s driven by backport patches. T…
32. [Container Security Scanning in 2026](https://sesamedisk.com/container-security-scanning-2026/) - Discover how container security scanning evolved in 2026, emphasizing multi-scanner strategies, supp…
33. [Trivy vs Grype 2026: Container Security Scanners](https://lucaberton.com/blog/trivy-vs-grype-2026/) - Grype is consistently 30-40% faster for pure vulnerability scanning. Grype does one thing, while Tri…
34. [Trivy and Grype: Which Matured Better?](https://jacar.es/en/trivy-and-grype-a-year-later-which-matured-better/) - Trivy and Grype compared: two container scanners after a year of intensive CI use. Which matured bet…
35. [Beyond Trivy and tfsec - Comparing Alternative Security ...](https://codenote.net/en/posts/trivy-tfsec-alternatives-security-scanning-tools-comparison/) - With Trivy's supply chain compromise in March 2026 and tfsec's end-of-life, we evaluate alternatives…
36. [How to Sign Container Images with Cosign](https://oneuptime.com/blog/post/2026-01-25-cosign-container-image-signing/view) - Learn how to sign and verify container images with Cosign to establish trust in your software supply…
37. [How to Implement SLSA Level 3 Build Provenance for ...](https://oneuptime.com/blog/post/2026-02-09-slsa-level3-build-provenance/view) - Learn how to implement SLSA Level 3 build provenance for Kubernetes container images using Tekton Ch…
38. [Board and executive assurance: cyber security risk](https://www.england.nhs.uk/long-read/board-and-executive-assurance-cyber-security-risk/) - NHS England " Board and executive assurance: cyber security risk
39. [NHS DSPT 2025-26: Audit Requirements, Exemptions and 11 ...](https://www.periculo.co.uk/cyber-security-blog/nhs-dspt-2025-26-audit-requirements-exemptions-and-11-mandatory-controls) - Discover what's new in the NHS DSP Toolkit 2025-26, including the 11 mandatory audit areas and how h…
