---
aliases: ["Type-Safe IaC", "Type-Driven Infrastructure", "Terraform Type Safety", "Data-Centric IaC"]
confidence: "5/5"
created: 2025-12-29
epistemic: "architecture"
last_reviewed: "2025-12-29"
modified: 2025-12-29
purpose: "To define the architectural pattern of applying Type Theory and State Space reduction to Infrastructure as Code (Terraform), preventing 'Configuration Explosion'."
review_interval: "6 months"
see_also: ["[[SoT - Type-Driven Development (The Torvalds Loop)]]", "[[SoT - The Trinity of Isomorphism (Logic, Computation, Categories)]]", "[[SoT - Rust's Design Philosophy]]"]
source_of_truth: []
status: "stable"
tags: ["infrastructure", "terraform", "type_theory", "architecture", "security"]
title: SoT - Type-Driven Infrastructure as Code
type: "SoT"
uid: 
updated: 
---

## 1. The Core Problem: Configuration Explosion

Infrastructure as Code (IaC) tools like Terraform are often treated as "Scripts" rather than "Software," leading to the **Configuration Explosion** anti-pattern.

- **The Anti-Pattern (God Modules):** Creating generic modules that expose every underlying API parameter as a variable.
- **The Consequence:** The "State Space" (possible combinations) is effectively infinite. Users can create invalid or insecure configurations (e.g., public S3 buckets, GPU nodes on basic instances) because the code permits it.
- **The Diagnosis:** Terraform HCL is "Stringly Typed" (Structural/Dynamic). It lacks the Nominal Typing required to enforce business invariants at compile time.

---

## 2. The Solution: Type-Driven Constraints

We force the **Mental Model** of Type Theory onto Terraform by treating Modules as **Types** (Contracts) rather than scripts.

### Strategy A: Simulating Sum Types (Enums)

Since HCL lacks Enums, we simulate them using **Validation Logic** and **Lookup Maps**.

**The Pattern:**
1. **The Interface (Enum Tag):** Expose a single variable (e.g., `profile`) restricted to a specific set of strings (`generic`, `compute`, `gpu`).
2. **The Implementation (Variant Data):** Use a `local` map to hold the complex configuration for each variant.
3. **The Result:** The user cannot mix-and-match invalid settings. They must choose a pre-validated "Variant."

```hcl
variable "profile" {
  type = string
  validation {
    condition = contains(["generic", "compute"], var.profile)
    error_message = "Must be a valid profile variant."
  }
}
```

### Strategy B: The "Compiler" Pattern (TypeScript as Metalanguage)

For complex domains (like Security/IAM), HCL is insufficient. We use a **stronger language (TypeScript/Rust)** to define the model and "compile" it to JSON for Terraform to consume.

**The Workflow:**
1. **Define the Model:** Use TypeScript Discriminated Unions to define valid states (e.g., `DevCapability` vs. `AdminCapability`).
2. **Compile:** Run the TS code to generate a `terraform.tfvars.json`.
3. **Apply:** Terraform acts as the "Runtime," blindly actuating the JSON without complex logic.

---

## 3. Security Application: Capability-Based Access

We reject standard RBAC (Role-Based Access Control) strings in favor of **Capability Tokens**.

- **Identity:** Modeled as a Sum Type (`Human | Bot`).
- **Capability:** A verified token granting specific access (e.g., `DevCapability` cannot target `Prod`).
- **Lease:** Time-bound access enforced by the type system (e.g., Ephemeral leases must be < 1 hour).

**The Guarantee:**
If the TypeScript model compiles, the generated infrastructure is secure by definition. We shift validation from "Runtime Policy" (OPA Gatekeeper) to "Compile-Time Architecture."

---

## 4. Minimum Viable Understanding (MVU)

1. **Modules are Types:** Don't expose parameters; expose **Variants**.
2. **Reduce State Space:** Use validation to make invalid configurations (like public databases) unrepresentable.
3. **The Compiler Pattern:** When HCL isn't enough, generate the config using a real language.
