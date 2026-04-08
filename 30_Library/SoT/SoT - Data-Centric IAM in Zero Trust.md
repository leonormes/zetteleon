---
aliases: ["Data-Centric Security", "PDP-PEP Architecture", "Zero Trust IAM"]
created: 2025-03-15T10:12:06Z
last_reviewed: "2025-12-29"
modified: 2026-04-08T18:01:07+00:00
status: "stable"
tags: ["data-centric", "IAM", "SoftwareEngineering/Architecture", "SoftwareEngineering/Security", "TheHuman/Identity", "zero-trust"]
title: SoT - Data-Centric IAM in Zero Trust
type: "SoT"
updated: 
---

## 1. Definitive Statement

In a Zero Trust architecture, Identity and Access Management (IAM) is a continuous, calculated state rather than a static gateway. It is a data-processing function where access is the output of an evaluation of three decoupled datasets: Identity assertions, Contextual signals, and Policy logic.

Conceptual Foundation: See [[SoT - Zero Trust Architecture]] for the high-level philosophy of identity-centric security.

## 2. The Core Data Model (Schema)

To architect a Zero Trust IAM system, we must define the structural entities involved. These are concrete data objects that the Policy Decision Point (PDP) must ingest.

### A. The Subject Entity (Identity)

The _Subject_ is the actor requesting access, defined by bound attributes (claims).

- Source: Identity Provider (IdP) / Directory Service.
- Key Attributes: `sub` (Subject ID), `groups` (Affiliation), `auth_time` (Freshness), `amr` (Auth Method Reference).

### B. The Context Entity (Environment)

The _Context_ is the ephemeral state surrounding the request (metadata wrapper).

- Source: EDR, Network telemetry, Threat Intel.
- Key Attributes: `device_id`, `trust_level` (Managed/Compliant), `network_location`, `risk_score` (0-100).

### C. The Resource Entity (Object)

The _Resource_ is the target asset, which must self-describe its security requirements.

- Source: Resource Server / CMDB.
- Key Attributes: `classification` (Confidential/PII), `sensitivity_label` (Required `auth_strength`).

---

## 3. The Logic Function & Topology

### The Equation of Trust

Access ($A$) is a boolean output derived from a function ($f$) of the aggregate dataset:

$$
A = f(Identity \cup Context \cup Resource, Policy)
$$

### Architectural Planes

1. Data Plane (The Muscle): Handles actual data transmission. Sits behind the PEP (Policy Enforcement Point).
2. Control Plane (The Brain): Computes trust scores and issues instructions. Contains the PDP (Policy Decision Point).

---

## 4. Technical Specification: Zero Trust Policy Object

This JSON schema formalizes the "equation" by defining how these attributes must be matched to grant access.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Zero Trust Policy Object",
  "type": "object",
  "properties": {
    "target_resource": {
      "type": "object",
      "properties": {
        "service_identifier": { "type": "string" },
        "classification_level": { "type": "string", "enum": ["public", "internal", "confidential", "restricted"] }
      }
    },
    "conditions": {
      "type": "object",
      "properties": {
        "identity_assertions": {
          "type": "object",
          "properties": {
            "required_claims": { "type": "array", "items": { "type": "object" } },
            "min_auth_strength": { "type": "integer", "description": "1=Pwd, 2=MFA, 3=PhishingResistant" }
          }
        },
        "contextual_signals": {
          "type": "object",
          "properties": {
            "device_compliance": { "type": "boolean" },
            "max_risk_score": { "type": "integer" }
          }
        }
      }
    },
    "actions": {
      "type": "object",
      "properties": {
        "access_decision": { "type": "string", "enum": ["allow", "deny", "step_up_auth"] }
      }
    }
  }
}
```

---

## Case Study: OIDC + Kubernetes RBAC

The relationship between an OIDC Token (Identity Data) and a Kubernetes RBAC Binding (Policy Data) is a perfect implementation of this model.

1. Identity (JWT): The IdP asserts `groups: ["9999-8888…"]`.
2. Policy (RoleBinding): Kubernetes defines a link between `subject.name: "9999-8888…"` and `role: view`.
3. Relational Mapping: The Group Object ID acts as a Foreign Key connecting the remote Identity database to the local Permission table.

---

## 5. Minimum Viable Understanding (MVU)

1. Schema over Strings: Identities are structured objects (claims sets), not just usernames.
2. Intersection Logic: Authorization is the calculated intersection of Identity Claims, Context Signals, and Resource Policies.
3. Segregation of Duties: The component that _moves_ the data (PEP) never decides _if_ it should move; it obeys the PDP.
