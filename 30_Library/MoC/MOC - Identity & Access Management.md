---
aliases: ["IAM MOC", "Identity MOC"]
created: 2026-04-05T10:00:00Z
last_reviewed: 
modified: 2026-04-09T06:42:24+00:00
prodos: {kind: atomic, lifecycle: seedling, trust: working, id: "", review: {interval: "", last_reviewed: ""}, chronos: {last_synthesis: "", synthesis_count: 0}, atomic: {form: concept}, protocol: {applies_to: [], binary_checklist: true}, moc: {hub_for: [], entry_points: []}, ops: {tool: "", target_service: "", hop_level: "", requires_tunnel: false, prerequisites: []}, prompt: {description: "", inject_as: "", model_hints: ""}, project: {area: "", status: "", owner: ""}}
see_also: []
status: "Active"
superseded_by: ""
supersedes: ""
tags: ["iam", "infrastructure", "moc", "security"]
title: MOC - Identity & Access Management
type: "MOC"
---

## MOC - Identity & Access Management

### Overview

Identity and Access Management (IAM) is the framework of policies and technologies that ensures the right individuals have access to the right resources at the right times for the right reasons. In modern cloud-native environments, Identity is the new perimeter.

### 1. Core Concepts (The Fundamentals)

- [[SoT - Digital Identity]]: Attributes, Identifiers, and Credentials.
- [[SoT - Modern Authentication Standards]]: OAuth 2.0, OpenID Connect (OIDC), and SAML.
- [[SoT - Zero Trust Architecture]]: The strategic shift from perimeter security to identity-driven security.

### 2. Platform Implementations

- [[SoT - Microsoft Entra Identity]]: Azure's identity services (formerly Azure AD), including PIM, Conditional Access, and RBAC.
  - [[SoT - Microsoft Entra Application Model]]: App Registrations vs. Service Principals.
- [[SoT - AWS Identity & Access Management]]: AWS IAM, Resource-level permissions, and Cross-account access.
- [[SoT - FitFile Identity & Access Management (Auth0)]]: Application-level identity management.

### 3. Governance & Compliance

- [[SoT - NHS Identity Compliance]]: Specific controls required for handling sensitive NHS patient data (DSPT, UK GDPR).
- [[SoT - NIST Cybersecurity Framework]]: Alignment with global security standards.

### 4. Operational Protocols

- [[SoT - FitFile Secret Management Architecture]]: How identities consume secrets.
- [[SoT - GitOps for IAM and Permissions]]: Managing access via code.

---

### Related Maps

- [[MOC - Cloud-Native Authentication]]
- [[MOC - Cryptography]]
- [[MOC - FitFile Security & Secrets]]
- [[MOC - Networking]]
