---
aliases: ["Zero Trust IAM", "Data-Centric Security"]
confidence: "5/5"
created: 2025-03-15T10:12:06Z
epistemic: "theory"
last_reviewed: "2025-12-26"
modified: 2025-12-26T19:02:10+00:00
purpose: "To define IAM within a Zero Trust framework as a function of data relationships, specifying the schemas and logic required for trust establishment."
review_interval: "6 months"
see_also: ["[[SoT - Digital Identity]]", "[[SoT - Modern Authentication Standards]]"]
source_of_truth: []
status: "stable"
tags: ["data-centric", "IAM", "security", "zero-trust", "identity", "architecture"]
title: SoT - Data-Centric IAM in Zero Trust
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

In a Zero Trust architecture, **Identity and Access Management (IAM)** is a continuous, calculated state rather than a static gateway. It is a data-processing function where access is the output of an evaluation of three decoupled datasets: **Identity assertions**, **Contextual signals**, and **Policy logic**.

## 2. The Core Data Model (Schema)

To architect a Zero Trust IAM system, we must define the structural entities involved. These are not abstract concepts but concrete data objects that the Policy Decision Point (PDP) must ingest.

### A. The Subject Entity (Identity)

The *Subject* is the actor requesting access. In a data-centric model, the Subject is defined by a set of bound attributes (claims).

* **Structure:** A collection of Key-Value pairs (Claims).
* **Source:** Identity Provider (IdP) / Directory Service.
* **Key Attributes:**
    * `sub` (Subject ID): Immutable unique identifier.
    * `groups` (Affiliation): List of functional roles or security groups.
    * `auth_time` (Freshness): Timestamp of the last primary authentication.
    * `amr` (Auth Method Reference): Evidence of authentication strength (e.g., `mfa`, `pwd`).

### B. The Context Entity (Environment)

The *Context* is the ephemeral state surrounding the request. It acts as a metadata wrapper around the Subject.

* **Structure:** A dynamic JSON object aggregated at runtime.
* **Source:** Endpoint Detection & Response (EDR), Network telemetry, Threat Intelligence feeds.
* **Key Attributes:**
    * `device_id` & `trust_level`: e.g., "Managed", "Compliant", "Unknown".
    * `network_location`: IP geo-location, trusted network segment.
    * `risk_score`: Aggregated integer (0-100) representing anomaly probability.

### C. The Resource Entity (Object)

The *Resource* is the target asset. It must self-describe its security requirements.

* **Structure:** Tagged metadata on the asset.
* **Source:** Resource Server / CMDB.
* **Key Attributes:**
    * `classification`: e.g., "Confidential", "Public", "PII".
    * `sensitivity_label`: Determining the minimum required `auth_strength`.

---

## 3. Structural Relationships & Topology

The security of the system relies on the integrity of the relationships between these data structures.

### The Decoupling Principle

A critical architectural invariant is the **decoupling of Authentication (AuthN) and Authorization (AuthZ)**.

1. **IdP (Identity Provider):** Owns the **Subject Data**. It asserts *who* the entity is and mints the Identity Token. It does not know about the Resource.
2. **RP (Relying Party / Resource):** Owns the **Resource Data**. It does not know the user's password; it only trusts the IdP's signature.
3. **PDP (Policy Decision Point):** The logic engine that acts as the intersection point.

### The Logic Function

Access ($A$) is a boolean output derived from a function ($f$) of the aggregate dataset:

$$A = f(Identity \cup Context \cup Resource, Policy)$$

Where:

* $Identity$ provides the claims (Subject).
* $Context$ provides the constraints (Environment).
* $Resource$ provides the classification (Target).
* $Policy$ provides the evaluation logic.

---

## 4. Case Study: Data Structures in Kubernetes & Entra ID

This integration demonstrates the data-centric model via the relationship between an **OIDC Token** (Identity Data) and a **Kubernetes RBAC Binding** (Policy Data).

### A. The Identity Structure (The JWT)

The IdP (Entra ID) emits a JSON Web Token. This is a portable database of the Subject.

```json
{
  "aud": "k8s-cluster-api",
  "iss": "https://sts.windows.net/tenant-id/",
  "oid": "1111-2222-3333-4444",   // The Immutable Subject Key
  "groups": [
    "9999-8888-7777-6666"          // The Foreign Key for permissions
  ]
}
```

### B. The Policy Structure (The RoleBinding)

Kubernetes defines a `RoleBinding` object. This is the **Link Table** connecting a remote Identity to a local Permission.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developers-read-access
subjects:
- kind: Group
  name: "9999-8888-7777-6666"      # Matches 'groups' claim in JWT
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: view                       # The actual permissions (read-only)
  apiGroup: rbac.authorization.k8s.io
```

### C. The Relational Mapping

The architectural elegance lies in the **Foreign Key relationship**:

1. **The Join Key:** The Group Object ID (`9999-8888...`) exists in both the Entra ID database (as a Group) and the Kubernetes Cluster (as a `subject.name`).
2. **Runtime Evaluation:**
    - Kubernetes validates the JWT signature (Trust).
    - Kubernetes extracts the `groups` list.
    - Kubernetes queries its internal `RoleBinding` table: `SELECT Role FROM RoleBindings WHERE Subject IN Token.groups`.

### D. Architectural Implications

- **Statelessness:** The API server requires no connection to the IdP to validate the request, provided the token key is cached.
- **Separation of Concerns:** The Identity Team manages group membership in Entra ID. The Platform Team manages permissions in Kubernetes. Neither team blocks the other.

---

## 5. Minimum Viable Understanding (MVU)

1. **Schema over Strings:** Do not treat identities as strings (usernames); treat them as structured objects (claims sets).
2. **Intersection Logic:** Authorisation is the calculated intersection of Identity Claims and Resource Policies.
3. **Dynamic Binding:** Trust is established dynamically at the moment of request by binding a trusted Identity Token to a specific Context.
