---
aliases: ["Primitive Obsession", "String Blindness", "Stringly Typed"]
confidence: "High"
created: 2026-01-06T18:58:05+00:00
epistemic: "Pattern"
last_reviewed: 
modified: 2026-01-23T18:09:17+00:00
purpose: "To define the architectural anti-pattern of using strings to model complex data, and to contrast it with strongly typed structural modeling."
review_interval: "1 year"
see_also: ["[[SoT - Data-Centric Software Engineering]]", "[[SoT - Parse, Don't Validate]]", "[[SoT - Type-Driven Development (The Torvalds Loop)]]"]
source_of_truth: []
status: "Active"
tags: ["anti-pattern", "devops", "SoftwareEngineering/Architecture", "types"]
title: SoT - Stringly Typed vs Strongly Typed
type: "SoT"
uid: 
updated: 
---

## SoT - Stringly Typed Vs Strongly Typed

> **The Core Tension:** "Strings represent high-entropy, unstructured state. Relying on them for internal logic bypasses the type safety and structural guarantees required for robust architecture."

### 1. The Anti-Pattern: Stringly Typed

"Stringly Typed" code uses string primitives to represent domain concepts. It is a form of **Primitive Obsession** where the developer relies on implicit knowledge rather than explicit contracts.

- **The Container:** A string is just a generic array of bytes.
- **The Contract:** Hidden. `var config = "…"` could be JSON, a file path, or a haiku. The compiler cannot help you.
- **The Parsing Cliff:** To use the data, you must constantly **parse** it (split, regex, cast). Every usage is a potential runtime failure.
- **Opaque State:** You cannot introspect the properties. It is a black box.

#### The DevOps Manifestation (Templates)

In Infrastructure as Code (Helm, Terraform HCL), this manifests as **Templating**:

- _Mechanism:_ String interpolation `"${var.region}-${var.env}"`.
- _Fragility:_ You are programming in macros. A whitespace error in the generated YAML string crashes the deployment, even if the logic was "correct."

### 2. The Solution: Strongly Typed (Structural Modeling)

Strongly typed code uses specific **Types** (Classes, Structs, Enums) to enforce the domain model at compile time.

- **The Container:** A defined Schema (`struct Config`).
- **The Contract:** Explicit. `var config: Config`. The compiler enforces that required fields exist.
- **Zero Parsing:** The data is already in its final, usable form.
- **Transparent State:** IDEs provide autocomplete; dependencies are visible in the graph.

#### The DevOps Solution (Synthesis)

Modern IaC tools (CDK, Pulumi) move from **Templating** to **Modeling**:

- _Mechanism:_ `new Vpc(scope, "MyVPC", { cidr: "10.0.0.0/16" })`.
- _Safety:_ If you miss a required property, the code does not compile. You are building an Object Graph, not a text file.

### 3. Implementation Paradigms for IaC

| Paradigm | Mental Model | Best For | Languages |
|:--- |:--- |:--- |:--- |
| **Templating** | "Inject logic into text." | Simple, static configs. | Helm, HCL (Terraform) |
| **SDK / GPL** | "Imperative: Execute loops to build a graph." | Complex logic, dynamic environments. | **CDK**, Pulumi (TypeScript, Go) |
| **Cloud-Oriented** | "Unified: Infra and Code are one." | Serverless, reducing "glue" code. | Winglang |
| **Programmable Config** | "Declarative: Unify data with constraints." | Strict policy/schema validation. | CUE, Pkl, Nickel |

### 4. Minimum Viable Understanding (MVU)

1. **Strings are for Transmission, not Modeling.** Use them only at the I/O boundary (serialization).
2. **Internal State must be Typed.** Once data enters your system, parse it into a struct immediately.
3. **Templates are Fragile.** Any system that relies on text manipulation for logic (Helm) is inherently prone to "Whitespace Bugs" and "Silent Failures."
