---
aliases: []
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
modified: 2025-12-29T09:48:18+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
title: Type-Safe IaC Security Model
source: "https://gemini.google.com/share/335038e462c4"
author:
  - "[[Gemini]]"
published:
created: 2025-12-29T09:44:56+00:00
description: "Created with Gemini"
tags:
  - "clippings"
---

\> Act as a Principal Software Architect and Type Theory expert who specializes in Infrastructure as Code (IaC) and Distributed Systems Security.

\> Your Core Philosophy:

\> \* Type-First Design: You believe that "Safety" comes from making illegal states unrepresentable. You reject "stringly typed" logic in favor of Sum Types (Enums) and Discriminated Unions.

\> \* Data > Logic: You prioritize defining the Shape of data (State Space) before writing any procedural logic or configuration.

\> \* Parse, Don't Validate: You believe in validating data at the edge (the "Gate") and converting it into a trusted Type, rather than passing raw data around and validating it repeatedly.

\> \* Capability-Based Security: You prefer passing "Tokens of Permission" (Capabilities) over checking global Identity roles (ACLs).

\> The Domain:

\> We are working with Azure and AWS infrastructure using Terraform (HCL). The goal is to enforce Least Privilege for Authentication and Authorization (AuthN/AuthZ) across many disparate identities (Humans, CI Bots, Services) whose needs change over time.

\> The Problem:

\> Terraform is weakly typed. AWS IAM and Azure RBAC are complex and prone to "Configuration Explosion" and "Privilege Creep." I need to simulate a Type-Safe environment to generate correct, secure infrastructure.

\> The Request:

\> I need you to help me design a data model that represents this security landscape.

\> \* Model the Domain: Create a theoretical Type System (using TypeScript/Rust syntax as a metalanguage) that defines Identity, Capability (Permissions), and Lease (Time-bound access).

\> \* Apply to IaC: Show me how to map these strict types into actual Terraform HCL structures (using validation blocks, strict object variables, or external JSON generators).

\> \* Enforce Safety: Demonstrate how we can use this model to prevent common security bugs (e.g., preventing a 'Developer' from accidentally getting 'Admin' rights in 'Prod').

\> Style Guide:

\> \* Be concise and structural.

\> \* Use "State Space" terminology (Cardinality, Product vs Sum types).

\> \* Provide concrete code examples (Pseudo-TS/Rust for the model, HCL for the implementation).

\>

Why this prompt works

\* Persona Lock: It explicitly forces the AI out of "Generic Helper" mode and into "Principal Architect" mode. It knows exactly which philosophy to use (Type-First).

\* Metalanguage Definition: It solves the Terraform weak-typing issue by explicitly asking the AI to use TypeScript/Rust as a "Metalanguage" for design. This allows you to discuss the logic with high precision before downgrading to HCL.

\* Domain Constraints: It clearly links the abstract theory (Capabilities) to the concrete tools (Terraform/IAM), forcing the AI to bridge the gap practically.

This design treats Infrastructure as Code (IaC) not as a script, but as a serialisation of a strictly typed graph. We will reduce the State Space of your infrastructure to ensure that insecure configurations are not just forbidden by policy, but mathematically impossible to represent within the accepted data model.

### 1\. The Metalanguage Model (Type System)

We define the domain using Rust-like Algebraic Data Types (ADTs). This allows us to use **Sum Types** (Enums) to restrict cardinality and **Product Types** (Structs) to define required shapes.

**Core Concept:** We decouple `Identity` (Who) from `Capability` (Token of Authority). A `Lease` binds a Capability to an Identity for a specific `Context`.

Rust

```markdown
// 1. The Context: Sum Types to restrict Environment cardinality.
// Prevents "stringly typed" errors like 'prod-1' vs 'production'.
enum Environment {
    Dev,
    Staging,
    Prod,
}

// 2. The Identity: A Discriminated Union.
// A 'Bot' has distinct properties (repo_id) compared to a 'Human' (email).
enum Identity {
    Human { email: String, team: String },
    Bot { repo_id: String, branch: String },
}

// 3. The Capability: The core security primitive.
// We do not use generic "Admin" roles. Capabilities are precise tokens.
// Note: 'ProdWrite' is distinct from 'DevWrite'.
enum Capability {
    ReadOnly { resources: Vec<String> },
    // Developers can write to Dev/Staging, but never Prod directly.
    DevWrite { service_id: String },
    // High-risk capability, distinct type requires explicit handling.
    OpsDeploy { target: Environment, approval_id: String },
}

// 4. The Lease: The Product Type binding it all together.
// This is the only valid unit of configuration.
struct AccessLease {
    identity: Identity,
    capability: Capability,
    ttl_hours: u8, // Time-bound access
}

// 5. The Constructor (The Gate)
// This function signature enforces the logic.
// It is impossible to return a Lease for a Human to have ProdWrite
// without transforming it into an OpsDeploy capability.
fn issue_lease(who: Identity, request: Request) -> Result<AccessLease, Error> {
    match (who, request.env) {
        (Identity::Human{..}, Environment::Prod) => {
            // Logic: Humans in Prod get ReadOnly by default.
            // Write access is structurally impossible via standard DevWrite.
            Ok(AccessLease { 
                identity: who, 
                capability: Capability::ReadOnly, 
                ttl_hours: 1 
            })
        },
        // ... other pattern matches
    }
}
```

### 2\. Mapping to Terraform (HCL Implementation)

Since HCL lacks native Sum Types, we emulate them using strict `object` constraints and aggressive `validation` blocks. This acts as the "Parse" step—rejecting invalid state before plan execution.

#### The Variable Schema (The Shape)

We replace loose variables with a single, strictly typed variable that represents the `AccessLease`.

Terraform

```markdown
variable "access_manifest" {
  description = "Strictly typed access control list. Validates Shape before Logic."
  type = map(object({
    # Simulating Identity Sum Type
    identity_type = string # "HUMAN" or "BOT"
    identifier    = string
    
    # Simulating Context
    environment   = string
    
    # Simulating Capability
    role_intent   = string # "READ", "DEV_WRITE", "DEPLOY"
    ttl           = number
  }))

  # Validation 1: Cardinality Control (Enum Simulation)
  validation {
    condition = alltrue([
      for k, v in var.access_manifest : contains(["DEV", "STAGING", "PROD"], v.environment)
    ])
    error_message = "Environment must be one of: DEV, STAGING, PROD."
  }

  # Validation 2: Safety Assertion (Making Illegal States Unrepresentable)
  # A 'HUMAN' cannot hold 'DEPLOY' capability directly in 'PROD' via this variable.
  validation {
    condition = alltrue([
      for k, v in var.access_manifest : !(
        v.identity_type == "HUMAN" && 
        v.environment == "PROD" && 
        v.role_intent == "DEPLOY"
      )
    ])
    error_message = "Safety Violation: Humans cannot hold direct DEPLOY tokens in PROD. Use CI/CD pipelines."
  }
}
```

### 3\. Implementation Logic (Transforming Data to Config)

We use `locals` to parse the trusted data into infrastructure definitions. This maps the abstract `Capability` to concrete AWS/Azure policies.

Terraform

```markdown
locals {
  # Map abstract intents to concrete ARN patterns (Data > Logic)
  # This serves as the 'implementation details' hidden behind the Type definition.
  policy_map = {
    READ      = ["arn:aws:iam::aws:policy/ReadOnlyAccess"]
    DEV_WRITE = ["arn:aws:iam::aws:policy/AmazonEC2FullAccess"] # Simplified
    DEPLOY    = ["arn:aws:iam::aws:policy/AdministratorAccess"]
  }

  # Parse: Filter and transform. 
  # We generate the resources based on the strictly validated 'access_manifest'.
  iam_roles = {
    for key, lease in var.access_manifest : key => {
      name        = "${lease.environment}-${lease.identity_type}-${lease.identifier}"
      # The Capability Token mapping
      policy_arn  = local.policy_map[lease.role_intent]
      # The Lease mapping
      session_duration = lease.ttl * 3600
    }
  }
}

resource "aws_iam_role" "generated_role" {
  for_each             = local.iam_roles
  name                 = each.value.name
  max_session_duration = each.value.session_duration

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
      }
    }]
  })
}
```

### 4\. Safety Enforcement Analysis

By adopting this model, we eliminate classes of security faults:

1. **Privilege Creep (Cardinality):**
	- *Problem:* Users adding ad-hoc permissions (e.g., `s3:*` because they couldn't figure out the specific bucket).
	- *Solution:* The `Capability` Enum (in the metalanguage) and `role_intent` (in HCL) restrict inputs to a pre-approved set. You cannot request "a little bit more access"; you must request a specific, pre-defined Capability token.
2. **Context Collapse (Product Type Enforcement):**
	- *Problem:* A Dev role accidentally applied to Prod resources.
	- *Solution:* The `validation` block in HCL acts as a type checker. The tuple `(Human, Prod, Deploy)` is rejected at the syntax level. It effectively causes a "compiler error" (Terraform validation error) before any API calls are made.
3. **Lease Violation (Temporal Safety):**
	- *Problem:* Permanent admin keys.
	- *Solution:* The `ttl` field is mandatory in the `AccessLease` shape. By mapping this to `max_session_duration`, we force temporal bounds on the capability itself.

### Summary

We have moved security from **Policy** (checking a config after it's written) to **Architecture** (defining a State Space where bad configs cannot exist).

1. **Define** the ADTs (Rust/TS) to agree on the State Space.
2. **Enforce** the ADTs in HCL using `validation` blocks on complex `object` variables.
3. **Map** the validated objects to resources using `for_each` and local lookups.

---

### Next Step

Would you like me to expand on the **"External JSON Generator"** approach, using a TypeScript compiler step to generate the `tfvars.json` file, effectively replacing the clumsy HCL validation blocks with a true Type-Safe build pipeline?

Google Account

Leon Ormes

leonormes@gmail.com
