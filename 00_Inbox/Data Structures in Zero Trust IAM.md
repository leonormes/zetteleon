---
aliases: []
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
modified: 2025-12-29T09:48:14+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
title: Data Structures in Zero Trust IAM
source: "https://gemini.google.com/share/6c81a8532a1e"
author:
  - "[[Gemini]]"
published:
created: 2025-12-29T09:40:31+00:00
description: "Created with Gemini"
tags:
  - "clippings"
---

review this and output an updated version that discusses the data structures and their relationships in clear detail

Here is the updated Source of Truth (SoT). This version restructures the content to prioritise the underlying data schemas, their relational mapping, and the architectural logic, aligning with your request for structural clarity and concept density.

---

Markdown

```markdown
---
aliases: ["Zero Trust IAM", "Data-Centric Security"]
confidence: "5/5"
created: 2025-03-15T10:12:06Z
epistemic: "theory"
last_reviewed: "2025-12-26"
modified: 2025-12-26T18:35:00+00:00
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
    * \`sub\` (Subject ID): Immutable unique identifier.
    * \`groups\` (Affiliation): List of functional roles or security groups.
    * \`auth_time\` (Freshness): Timestamp of the last primary authentication.
    * \`amr\` (Auth Method Reference): Evidence of authentication strength (e.g., \`mfa\`, \`pwd\`).

### B. The Context Entity (Environment)
The *Context* is the ephemeral state surrounding the request. It acts as a metadata wrapper around the Subject.

* **Structure:** A dynamic JSON object aggregated at runtime.
* **Source:** Endpoint Detection & Response (EDR), Network telemetry, Threat Intelligence feeds.
* **Key Attributes:**
    * \`device_id\` & \`trust_level\`: e.g., "Managed", "Compliant", "Unknown".
    * \`network_location\`: IP geo-location, trusted network segment.
    * \`risk_score\`: Aggregated integer (0-100) representing anomaly probability.

### C. The Resource Entity (Object)
The *Resource* is the target asset. It must self-describe its security requirements.

* **Structure:** Tagged metadata on the asset.
* **Source:** Resource Server / CMDB.
* **Key Attributes:**
    * \`classification\`: e.g., "Confidential", "Public", "PII".
    * \`sensitivity_label\`: Determining the minimum required \`auth_strength\`.

---

## 3. Structural Relationships & Topology

The security of the system relies on the integrity of the relationships between these data structures.

### The Decoupling Principle
A critical architectural invariant is the **decoupling of Authentication (AuthN) and Authorization (AuthZ)**.

1.  **IdP (Identity Provider):** Owns the **Subject Data**. It asserts *who* the entity is and mints the Identity Token. It does not know about the Resource.
2.  **RP (Relying Party / Resource):** Owns the **Resource Data**. It does not know the user's password; it only trusts the IdP's signature.
3.  **PDP (Policy Decision Point):** The logic engine that acts as the intersection point.

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

\`\`\`json
{
  "aud": "k8s-cluster-api",
  "iss": "[https://sts.windows.net/tenant-id/](https://sts.windows.net/tenant-id/)",
  "oid": "1111-2222-3333-4444",   // The Immutable Subject Key
  "groups": [
    "9999-8888-7777-6666"          // The Foreign Key for permissions
  ]
}
```

### B. The Policy Structure (The RoleBinding)

Kubernetes defines a `RoleBinding` object. This is the **Link Table** connecting a remote Identity to a local Permission.

YAML

```markdown
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

## 5\. Minimum Viable Understanding (MVU)

1. **Schema over Strings:** Do not treat identities as strings (usernames); treat them as structured objects (claims sets).
2. **Intersection Logic:** Authorisation is the calculated intersection of Identity Claims and Resource Policies.
3. **Dynamic Binding:** Trust is established dynamically at the moment of request by binding a trusted Identity Token to a specific Context.

```markdown
***

### Next Step
Would you like me to generate a specific generic JSON schema for a "Zero Trust Policy Object" that could be used to standardise policy definitions across different enforcement points?
```

yes

Here is a JSON schema definition for a standardised "Zero Trust Policy Object." This schema abstracts the logic discussed in the Source of Truth into a portable data structure that could theoretically be consumed by any Policy Decision Point (PDP).

### Zero Trust Policy Object (JSON Schema)

This schema formalises the "equation" by defining how these attributes must be matched to grant access.

JSON

```markdown
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/schemas/zero-trust-policy.json",
  "title": "Zero Trust Policy Object",
  "description": "A structured definition of access requirements binding Identity, Context, and Resource attributes.",
  "type": "object",
  "properties": {
    "meta": {
      "type": "object",
      "properties": {
        "policy_id": { "type": "string", "format": "uuid" },
        "version": { "type": "string" },
        "author": { "type": "string" },
        "last_updated": { "type": "string", "format": "date-time" }
      },
      "required": ["policy_id", "version"]
    },
    "target_resource": {
      "description": "Defines the scope/asset this policy protects.",
      "type": "object",
      "properties": {
        "service_identifier": { "type": "string", "examples": ["k8s-cluster-prod", "aws-s3-finance"] },
        "classification_level": { "type": "string", "enum": ["public", "internal", "confidential", "restricted"] },
        "data_tags": {
          "type": "array",
          "items": { "type": "string" },
          "examples": ["PII", "PCI-DSS", "GDPR"]
        }
      },
      "required": ["service_identifier"]
    },
    "conditions": {
      "description": "The logic gate. All defined conditions must evaluate to TRUE for access to be granted (AND logic).",
      "type": "object",
      "properties": {
        "identity_assertions": {
          "description": "Requirements regarding the Subject (Who).",
          "type": "object",
          "properties": {
            "required_claims": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "claim_key": { "type": "string", "examples": ["groups", "department", "roles"] },
                  "operator": { "type": "string", "enum": ["equals", "contains", "starts_with"] },
                  "expected_value": { "type": "string" }
                }
              }
            },
            "min_auth_strength": {
              "description": "The minimum AMR level required.",
              "type": "integer",
              "minimum": 1,
              "maximum": 3,
              "description": "1=Pwd, 2=MFA, 3=PhishingResistant"
            }
          }
        },
        "contextual_signals": {
          "description": "Requirements regarding the Environment (Where/How).",
          "type": "object",
          "properties": {
            "device_compliance": { "type": "boolean", "default": true },
            "allowed_geo_regions": { "type": "array", "items": { "type": "string" } },
            "max_risk_score": { "type": "integer", "maximum": 100 },
            "time_of_day_restrictions": {
                "type": "object",
                "properties": {
                    "start": { "type": "string", "format": "time" },
                    "end": { "type": "string", "format": "time" },
                    "timezone": { "type": "string" }
                }
            }
          }
        }
      }
    },
    "actions": {
      "description": "The outcome if conditions are met.",
      "type": "object",
      "properties": {
        "access_decision": { "type": "string", "enum": ["allow", "deny", "step_up_auth"] },
        "granted_permissions": {
          "type": "array",
          "items": { "type": "string", "examples": ["read", "write", "execute", "admin"] }
        },
        "audit_level": { "type": "string", "enum": ["none", "metadata", "full_capture"] }
      }
    }
  },
  "required": ["target_resource", "conditions", "actions"]
}
```

### Next Step

Would you like me to create a mock "Policy Evaluation" simulation, where we take a sample **Identity Token (JWT)** and a sample **Context JSON**, and run them against this schema to demonstrate a Pass/Fail decision?

yes

Here is a simulation of the Policy Decision Point (PDP) execution logic. This demonstrates the **deterministic evaluation** of the inputs (Identity + Context) against the rules (Policy) to produce a boolean output.

### 1\. The Input Datasets

These are the runtime variables injected into the evaluation function.

#### Input A: The Identity Token (Decoded JWT)

*Represents the "Who" (Subject).*

JSON

```markdown
{
  "sub": "alice.smith@corp.io",
  "iat": 1710500000,
  "claims": {
    "oid": "a1b2-c3d4-e5f6",
    "groups": ["sysadmin-tier-1", "devops-lead"],
    "amr": ["pwd", "mfa"]  // Authentication Method Reference
  }
}
```

#### Input B: The Context Object

*Represents the "Where" and "How" (Environment).*

JSON

```markdown
{
  "request_id": "req-889900",
  "timestamp": "2025-12-26T20:15:00Z",
  "environment": {
    "device_id": "laptop-mac-04",
    "is_managed": true,
    "risk_score_aggregated": 15, // Low risk (0-100 scale)
    "network_segment": "vpn-internal-secure"
  }
}
```

---

### 2\. The Policy Instance (The Constants)

This is the instantiated schema defining the requirements for the target resource.

JSON

```markdown
{
  "policy_id": "pol-prod-db-write",
  "target_resource": {
    "service_identifier": "postgres-prod-01",
    "classification_level": "confidential"
  },
  "conditions": {
    "identity_assertions": {
      "required_claims": [
        { "claim_key": "claims.groups", "operator": "contains", "expected_value": "sysadmin-tier-1" }
      ],
      "min_auth_strength": 2 // Requires at least MFA
    },
    "contextual_signals": {
      "device_compliance": true,
      "max_risk_score": 25
    }
  },
  "actions": {
    "access_decision": "allow",
    "granted_permissions": ["db:read", "db:write"]
  }
}
```

---

### 3\. The Execution Logic (Trace)

The PDP engine runs a linear validation sequence. All gates must return `TRUE`.

#### Step 1: Identity Evaluation (The "Who")

1. **Claim Check:** Does `Input A.claims.groups` contain `"sysadmin-tier-1"`?
	- *Input:*`["sysadmin-tier-1", "devops-lead"]`
	- *Requirement:*`contains "sysadmin-tier-1"`
	- *Result:***PASS**
2. **Strength Check:** Map `amr` to integer. `["pwd", "mfa"]` = Level 2.
	- *Input:* Level 2
	- *Requirement:*`>=` Level 2
	- *Result:***PASS**

#### Step 2: Context Evaluation (The "How")

1. **Device Check:** Is the device managed?
	- *Input:*`Input B.environment.is_managed` = `true`
	- *Requirement:*`true`
	- *Result:***PASS**
2. **Risk Check:** Is the risk score acceptable?
	- *Input:*`15`
	- *Requirement:*`<= 25`
	- *Result:***PASS**

---

### 4\. The Output

Since `(Identity == True) AND (Context == True)`:

- **Decision:**`ALLOW`
- **Enforcement:** The Policy Enforcement Point (PEP) issues a short-lived access token with scopes `["db:read", "db:write"]`.
- **Audit Log:** "Access granted to Alice Smith for postgres-prod-01 via Policy pol-prod-db-write."

### Alternate Fail Scenario

If `Input B` had a `risk_score_aggregated` of **45** (e.g., due to an impossible travel alert):

- Logic: `45 <= 25` is `FALSE`.
- **Decision:**`DENY` or `STEP_UP`.
- **Action:** The user is blocked, or redirected to re-authenticate (Step-Up) to lower the risk score or satisfy a higher policy requirement.

---

### Next Step

Would you like me to diagram the full "Zero Trust Architecture" stack, showing exactly where the PDP (Decision) and PEP (Enforcement) sit relative to the User, the App, and the Data?

yes

Here is the architectural topology of the Zero Trust stack. This model separates the system into two distinct planes: the **Data Plane** (where packets flow) and the **Control Plane** (where decisions are made).

### 1\. The Logical Planes

The architecture functions by removing the decision-making logic from the direct path of access, creating a check-and-balance system.

#### A. The Data Plane (The "Muscle")

- **Function:** Handles the actual transmission of application data between the Subject and the Resource.
- **State:** Default Deny. No traffic flows here until explicitly unlocked by the Control Plane.
- **Key Component:****PEP (Policy Enforcement Point)**.

#### B. The Control Plane (The "Brain")

- **Function:** Computes the trust score and issues instructions to the Data Plane. It is "out-of-band" (invisible to the user).
- **State:** Continuous Evaluation. It constantly re-calculates trust based on live signals.
- **Key Component:****PDP (Policy Decision Point)**.

---

### 2\. Component Definitions

#### The PEP (Policy Enforcement Point)

- **Role:** The Guard / Gateway.
- **Location:** Sits immediately in front of the Resource (e.g., an Ingress Controller, API Gateway, or Sidecar Proxy).
- **Logic:****None.** The PEP is "dumb." It strictly executes the binary command (`Allow` / `Block`) received from the PDP.
- **Action:** It intercepts the request, pauses the traffic, and asks the PDP for a decision.

#### The PDP (Policy Decision Point)

- **Role:** The Judge.
- **Location:** Centralised SaaS or Identity Control Plane (e.g., Entra ID, Okta, OPA).
- **Logic:****Complex.** It runs the evaluation algorithm we defined previously:.
- **Sub-components:**
	- **Policy Engine:** The calculator that runs the algorithm.
	- **Policy Administrator:** The signal emitter that tells the PEP to open/close the connection.

---

### 3\. The Interaction Flow (The "Switchboard" Model)

1. **Interception (Data Plane):**The User (Subject) sends a request to the App (Resource). The **PEP** intercepts this traffic. The packet is effectively "frozen."
2. **Evaluation (Control Plane):**The PEP sends a metadata snapshot (Token + Context) to the **PDP**.
	- *The PDP queries the Trust Stores (IdP, Threat Intel).*
	- *The PDP runs the "Policy Object" simulation.*
3. **Instruction (Control Loop):**The PDP returns a verdict to the PEP:
	- *Allow:* The PEP unfreezes the packet and forwards it to the Resource.
	- *Deny:* The PEP drops the packet and returns a 403 Forbidden.
4. **Continuous Re-Evaluation:**If the context changes mid-session (e.g., Risk Score spikes), the PDP sends a **Revocation Signal** to the PEP, which immediately cuts the connection.

---

### 4\. Minimum Viable Understanding (MVU)

1. **Segregation of Duties:** The component that *moves* the data (PEP) never decides *if* it should move.
2. **Centralised Logic, Distributed Enforcement:** You have one brain (PDP) but many muscles (PEPs) scattered across your infrastructure (Cloud, On-prem, K8s).
3. **Ephemeral Access:** The "gate" is not left open. It opens for a specific request and closes immediately after, or upon a change in risk state.

---

### Next Step

Would you like me to draft a high-level **"Zero Trust Strategy Document"** (an executive summary) that synthesises the Data Model, Policy Logic, and Architecture into a single page for stakeholder alignment?

Google Account

Leon Ormes

leonormes@gmail.com
