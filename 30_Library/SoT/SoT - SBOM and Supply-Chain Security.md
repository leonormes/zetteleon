---
aliases: [Drift Detection, SBOM Analysis, Software Bill of Materials, Supply-Chain Security]
created: 2026-03-28T17:20:00+00:00
modified: 2026-07-13T08:52:53+00:00
permalink: llmeon/30-library/so-t/so-t-sbom-and-supply-chain-security
tags: [compliance, devops, sbom, security, supply-chain]
title: SoT - SBOM and Supply-Chain Security
type: sot
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## Minimum Viable Understanding (MVU)

A Software Bill of Materials (SBOM) is a formal, machine-readable record containing the details and supply chain relationships of various components used in building software. Supply-chain security focuses on detecting Drift (version, integrity, or metadata changes) and identifying risks introduced through Deep Transitive Dependencies (Depth 3+).

---

## Working Knowledge

### 1. Drift Detection Categories

| Drift Type | Indicator | Description | Risk Level |
|:---|:---:|:---|:---|
| Version Drift | 📦 | A component version number has changed. | Normal (Audit for CVEs) |
| Integrity Drift | ⚠️ | A hash changed without a version change. | High (Tampering signal) |
| Metadata Drift | 📝 | Only non-functional data (e.g., license field) changed. | Low (Audit for legal) |

### 2. The Transitive Risk Profile

Dependencies introduced deep in the graph are often pulled in without explicit review.

- Depth 1: Direct dependencies (Explicit choice).
- Depth 2: Dependencies of dependencies.
- Depth 3+: Deep transitive dependencies (High Risk). Often vectors for supply chain attacks (e.g., _event-stream_ incident).

### 3. Identity Matching Precedence

To reliably compare SBOMs across versions or formats, components should be matched using a strict hierarchy:

1. PURL (Package URL) - e.g., `pkg:npm/lodash`.
2. CPE (Common Platform Enumeration).
3. BOM-ref / SPDXID.
4. Namespace + Name.

---

## Current Understanding

### Key Metrics for Audit

- PURL/CPE Coverage: Percentage of components with valid identifiers (enables CVE scanning).
- License Risk Profile: Breakdown of Permissive vs. Copyleft (GPL) licenses.
- Attack Surface Delta: The net increase/decrease in package and file counts between releases.

### Tooling Patterns (Sbomlyze)

- CI Enforcement: Use policy files to fail builds if `deny_integrity_drift: true` or `max_depth: 3` is violated.
- Interactive Exploration: TUI/Web tools for deep-diving into dependency trees and raw JSON metadata.

## Related Documentation

- [[SoT - Container Security & Hardening]]
- [[SoT - SOT - CI-CD Pipelines]]
- [[GitHub - rezmosssbomlyze SBOM diff & analysis tool for software supply-chain security, integrity drift detection, and CICD enforcement]]


## Related

- [[SoT - Container Security & Hardening]]
- [[Integrate Security into the Workflow (Shift Left)]]
- [[Protocol - NIST CSF Implementation via Microsegmentation]]

