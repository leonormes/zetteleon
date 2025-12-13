---
aliases: []
confidence: 
created: 2025-02-07T12:57:53Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:42Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Rust nightly on the laptop
type:
uid: 
updated: 
version:
---

Here's a comprehensive debug wiki page documenting the issues and solutions we encountered:

---

## Rust/Cargo Toolchain Debug Guide

### Problem Overview

Scenario: Compilation failures when using `#![feature(test)]` due to toolchain conflicts and corrupted installations.

#### Key Symptoms
1. `error[E0554]: #![feature] may not be used on the stable release channel`
2. Corrupted nightly toolchain showing impossible dates (2025)
3. `curl` installation failures returning HTML instead of installer script
4. Toolchain override not taking effect

---

### Debugging Timeline

#### 1. Initial Channel Conflict

Error:

```rust
error[E0554]: `#![feature]` may not be used on the stable release channel
```

Solution:

```bash
rustup install nightly
rustup override set nightly
cargo clean && cargo test
```

Verification:

```bash
rustc --version | grep nightly
```

#### 2. Corrupted Toolchain

Symptom:

```bash
rustc 1.86.0-nightly (ed43cbcb8 2025-01-21) # Impossible date
```

Resolution:

```bash
# Force reinstall nightly
rustup toolchain uninstall nightly
rustup install nightly --force

# Verify
rustc --version # Should show current date
```

#### 3. Installation Conflicts

Issue: Homebrew-installed Rust conflicting with rustup

Clean Installation:

```bash
# Remove all Rust installations
brew uninstall rust
rustup self uninstall
rm -rf ~/.rustup ~/.cargo

# Fresh install via rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

#### 4. Network Issues

Error:

```bash
sh: line 1: syntax error near unexpected token `newline'
<!DOCTYPE html>...
```

Workarounds:

```bash
# Manual download
curl -L -o rustup-init https://sh.rustup.rs
sh rustup-init

# Alternative mirrors
curl https://static.rust-lang.org/rustup/dist/x86_64-apple-darwin/rustup-init -o rustup-init
```

---

### Prevention Best Practices

#### Toolchain Management

```bash
# Recommended setup
rustup default nightly
rustup component add rust-src rust-docs

# Project-specific override
rustup override set nightly
```

#### Environment Configuration

~/.zshrc:

```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

#### Verification Checklist
1. Single Rust installation (`which rustc` should show ~/.cargo/bin)
2. Valid toolchain dates (`rustc --version`)
3. No `rust-toolchain` file conflicts
4. Correct PATH order (`echo $PATH | grep .cargo/bin`)

---

### Common Pitfalls

#### ❌ Mixed Installations

Don't: Use Homebrew Rust with rustup

Do: Use rustup exclusively

#### ❌ Outdated Components

```bash
# Update regularly
rustup update
cargo install-update -a
```

#### ❌ Network Restrictions

For corporate environments:

```bash
export https_proxy="http://corp-proxy:3128"
rustup toolchain install nightly --proxy
```

---

### Troubleshooting Matrix

| Symptom | First Check | Solution |
|---------|-------------|----------|
| Feature gate errors | `rustc --version` | Switch to nightly |
| Compiler date mismatch | `rustup show` | Reinstall toolchain |
| Installation failures | `curl -v https://sh.rustup.rs` | Manual download |
| PATH conflicts | `which cargo` | Adjust shell config |

---

### Key Takeaways

1. Always use rustup - Avoid system package managers for Rust
2. Verify toolchain dates - Corrupted installs show future dates
3. Isolate environments - Use per-project `rustup override`
4. Clean builds - `cargo clean` when switching toolchains

Final Test Command:

```bash
rustup run nightly cargo test --verbose
```

---

This document serves as a reference for resolving toolchain conflicts, installation issues, and feature gate errors in Rust projects. Update timestamps and version numbers as new Rust releases occur.
