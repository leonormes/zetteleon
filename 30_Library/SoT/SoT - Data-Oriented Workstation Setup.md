---
created: 2026-02-11 16:00:00+00:00
modified: 2026-07-04 10:51:01+00:00
permalink: llmeon/30-library/so-t/so-t-data-oriented-workstation-setup
source_of_truth: true
tags:
- architecture
- bootstrap
- chezmoi
- cue
- mise
- sot
- workstation
title: SoT - Data-Oriented Workstation Setup
prodos:
  kind: sot
  lifecycle: evergreen
  trust: stable
  chronos:
    last_synthesis: 2026-02-11
    synthesis_count: 1
---


## Minimum Viable Understanding (MVU)

The Data-Oriented Workstation Setup is a "Clean Slate" architecture for managing developer environments. It replaces imperative, platform-specific scripts with a declarative model driven by CUE, Chezmoi, and Mise. The system prioritises type safety, zero redundancy (common vs. OS targets), and a "Mise-first" strategy for runtime parity.

---

## 1. Core Principles

- Type Safety Over String Matching: Strict `#OS` definitions (`"darwin" | "linux"`) prevent logic errors across platforms.
- Mise-First Strategy: Use `mise` for all tool runtimes and CLI versions. OS package managers (Brew/Apt) are reserved for system-level GUI apps and core dependencies (e.g., 1Password).
- Zero Redundancy: Identical tools are defined in a `common` target; OS-specific overrides are applied only where strictly necessary.
- Root of Trust: The bootstrap sequence begins with 1Password CLI + Git via SSH to establish identity before any configuration is applied.

---

## 2. The Bootstrap Pipeline (Phase 0)

The setup follows a strict dependency chain to reach a functional state.

### 2.1 Dependency Chain

1. OS Package Manager: (Xcode CLI / Apt) to get `git` and `curl`.
2. Homebrew: (macOS only) to install core binaries.
3. 1Password CLI: To authenticate and unlock SSH keys.
4. Chezmoi: To manage the dotfiles repository.
5. CUE: To compile the data-driven configuration.
6. Mise: To manage all development runtimes (Node, Python, Go, etc.).

### 2.2 Primal Tools Schema (CUE)

Defined in `cue/bootstrap.cue`:

```cue
package bootstrap

#PrimalTool: {
    name:    string
    binary:  string
    install: {
        darwin: string
        linux:  string
    }
}

primal_tools: [
    {
        name:   "Homebrew (macOS) / Basic Tools (Linux)"
        binary: "brew"
        install: {
            darwin: #"/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && eval "$(/opt/homebrew/bin/brew shellenv)""#
            linux:  "sudo apt-get update && sudo apt-get install -y git curl unzip build-essential"
        }
    },
    // ... Additional tools: Mise, 1Password, Chezmoi, CUE
]
```

---

## 3. Discovery & Identity

A discovery script (`discover.sh`) acts as the system "sensor," gathering environment facts into `discovery.json` which is then ingested by CUE.

### 3.1 Identity Mapping

Identity is tied to the Profile, driven by the `is_work` tag and `hostname`.

```cue
#Identity: {
    username: string
    email:    string
    full_name: string
}

identities: {
    personal: #Identity & {
        username: "leonormes"
        email:    "leonormes@gmail.com"
        full_name: "Leon Ormes"
    }
    work: #Identity & {
        username: "leon.ormes"
        email:    "leon.ormes@fitfile.com"
        full_name: "Leon Ormes"
    }
}
```

---

## 4. Operational Protocols

### 4.1 Generating the Install Script

```bash
cue export cue/bootstrap.cue cue/gen_install.cue --out text -e output > install.sh
chmod +x install.sh
```

### 4.2 Handling Inventory Conflicts

Use a Set-based approach (struct mapping) in CUE to handle tool deduplication when merging `common`, `personal`, and `work` inventories.

```cue
_inventory_set: {
    for item in packages.inventory.common { (item): item }
    if is_work {
        for item in packages.inventory.work { (item): item }
    }
}
_all_inventory: [for _, item in _inventory_set { item }]
```

---

## 5. Related Knowledge

- Config: [[SoT - CUE Configuration]]
- Patterns: [[SoT - Pattern - CUE Data Architecture]]
