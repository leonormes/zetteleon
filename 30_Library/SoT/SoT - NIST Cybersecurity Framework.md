---
aliases: [Cybersecurity Governance, NIST CSF, NIST Cybersecurity Framework 2.0]
created: 2026-04-02T11:00:00+00:00
modified: 2026-07-13T08:52:51+00:00
permalink: llmeon/30-library/so-t/so-t-nist-cybersecurity-framework
source_of_truth: true
tags: [compliance, cybersecurity, governance, nist, resilience]
title: SoT - NIST Cybersecurity Framework
---

## Minimum Viable Understanding (MVU)

The NIST Cybersecurity Framework (CSF) is a high-level, vendor-neutral roadmap for managing and reducing cybersecurity risk. It organizes security activities into six core functions—Govern, Identify, Protect, Detect, Respond, and Recover—to provide a common language and systematic approach for building a resilient digital environment.

---

## 1. The Core Functions (CSF 2.0)

The Framework is structured around six concurrent and continuous functions that provide a strategic view of the lifecycle of an organization's management of cybersecurity risk.

| Function | Objective | Key Activities |
|:--- |:--- |:--- |
| Govern | Establish and monitor the organization's cybersecurity risk management strategy, roles, and responsibilities. | Policy development, supply chain risk management, oversight. |
| Identify | Develop an organizational understanding to manage cybersecurity risk to systems, people, assets, data, and capabilities. | Asset management, risk assessment, visibility into identities. |
| Protect | Develop and implement appropriate safeguards to ensure delivery of critical services. | Identity management, access control (least privilege), data security. |
| Detect | Develop and implement appropriate activities to identify the occurrence of a cybersecurity event. | Continuous monitoring, anomaly detection, logging. |
| Respond | Develop and implement appropriate activities to take action regarding a detected cybersecurity incident. | Incident analysis, mitigation, containment (blast radius reduction). |
| Recover | Develop and implement appropriate activities to maintain plans for resilience and to restore any capabilities or services that were impaired due to a cybersecurity incident. | Recovery planning, improvements based on lessons learned. |

---

## 2. Philosophy: "Protect" as the Primary Pivot

While all functions are necessary, the Protect function is often considered the most critical for proactive security.

- The Heuristic: "If you think you know something but don't write it down, you only think you know it." Similarly, if you aren't protecting your network at the data layer, your detection and response are merely damage control.
- Core Strategy: Focus heavily on data and system protections (Least Privilege, MFA, Isolation) to minimize the probability of a breach ever succeeding.

---

## 3. Maturity Tiers (NIST CSF 2.0)

The framework defines four Tiers to describe the degree of maturity in an organization's cybersecurity risk management practices:

- Tier 1 (Partial): Risk management is ad-hoc; limited awareness of risk.
- Tier 2 (Risk Informed): Practices are approved but not organization-wide.
- Tier 3 (Repeatable): Formally approved and expressed as policy.
- Tier 4 (Adaptive): Practices are adapted based on lessons learned and predictive indicators (e.g., automated response, dynamic policy).

---

## 4. Implementation Strategies

The NIST CSF is designed to be mapped to specific technical controls. Modern approaches like Microsegmentation and Zero Trust are uniquely positioned to operationalize all six functions.

- See: [[Protocol - NIST CSF Implementation via Microsegmentation]]

---

## Related Knowledge

- Governance: [[SoT - GitOps for IAM and Permissions]]
- Infrastructure: [[Protocol - Azure Private AKS Deployment]]
- Networking: [[SoT - The Data-Centric Theory of Networking]]
- Architecture: [[MOC - Data-Centric Software Engineering]]
