---
alias: ["CUE Patterns", "Dotfiles Architecture", "FFNode Refactor"]
created: 2026-02-04T00:00:00+00:00
modified: 2026-02-04T07:26:55+00:00
tags: ["architecture", "cue", "patterns", "sot"]
title: SoT - Pattern - CUE Data Architecture
type: SoT
---

## Pattern 1: The FFNode Refactor (Kubernetes)

_Moving from "Pass-Through Templating" to "Strict Contracts"._

### The Problem

The legacy Helm chart used "Double-Templating" where users wrote Go templates inside YAML strings for Vault secrets.

- Legacy: `vaultSecrets: "text: {{.Values.path }}"`
- Risk: No syntax checking, high cognitive load.

### The CUE Solution

Replace imperative booleans and templates with a Strict Schema.

```cue
package ffnode

#FFNodeAPI: {
    // 1. High-Level Intent (Profile)
    profile: "dev" | "stage" | "prod" @tag(profile)

    // 2. Identity (Global Graph)
    identity: {
        siteCode:      string
        environment:   string
        clusterDomain: string
    }

    // 3. Capabilities (Structs > Booleans)
    capabilities: {
        authentication: {
            provider:  "auth0" | "entra-id"
            // Abstracted Secret Intent
            secrets: #SecretIntent
        }
    }
}

// The Disjunction Pattern: Mutually Exclusive Logic
#SecretIntent: {
    source: "vault" | "k8s-secret"
    
    // Constraints based on selection
    if source == "vault" {
        path: string
    }
}
```

Guardrails:
- If `profile` is "prod", `secrets.source` MUST be "vault".
- Invalid configurations fail to compile immediately.

---

## Pattern 2: Dotfiles & Package Management (`chezmoi`)

_Unifying multiple package managers (Brew, Mise, Mas) into one source._

### Data Flow Pipeline

`packages.yaml` (Input) $\to$ CUE Unification $\to$ `generated.json` $\to$ `chezmoi` Templates.

### Schema Definition (`packages.cue`)

Enforces referential integrity between the Inventory (what I want) and the Registry (what exists).

```cue
#Package: {
    name: string
    // Calculated logic: Don't guess the manager in the template
    effective_manager: "brew" | "mise" | "mas"
}

// Inventory Logic
inventory: {
    common: [...string]
    work:   [...string]
}

// Validation: Every item in Inventory MUST exist in Registry
registry: [Name=string]: #Package
```

### Automation

A script runs `cue export` before `chezmoi apply`. If CUE fails (e.g., missing ID for a Mac App Store app), the dotfile update aborts, preventing partial/broken system states.

```
