---
source: hermes (deepseek-v4-flash)
tags:
- hermes
- solution
- topgrade
- pipx
permalink: llmeon/wiki/2026-09-08-fix-topgrade-pipx-python
---

# Topgrade Pipx Fix: PIPX_DEFAULT_PYTHON

## Problem

`pipx` step in `topgrade` failed with:

```
Python 3.10 or later is required.
```

## Root Cause

pipx is installed via `mise` (manager: pipx, no pipx: prefix). The pipx binary is a compiled Mach-O binary that resolves Python via PATH. Under topgrade's non-interactive shell, `python3` resolves to `/usr/bin/python3` (macOS system Python 3.9.6), which is too old.

The mise shim (`~/.local/share/mise/shims/pipx`) is also a compiled binary that links to the mise-installed pipx. But when pipx runs its subprocesses, it needs a Python 3.10+ interpreter.

## Fix

Set `PIPX_DEFAULT_PYTHON` environment variable in mise config to point to the mise-managed Python:

```toml
[env]
PIPX_DEFAULT_PYTHON = "{{ .chezmoi.homeDir }}/.local/share/mise/installs/python/latest/bin/python"
```

Deployed via chezmoi template at `dot_config/mise/config.toml.tmpl`.

## Verification

```bash
pipx list          # works
pipx upgrade-all   # works (no packages to upgrade)
```

## Related Failures in Same Topgrade Run

| Step | Failure | Fix |
|------|---------|-----|
| pipx | Python 3.10+ required | PIPX_DEFAULT_PYTHON in mise env |
| chezmoi | git HTTPS auth failed | Already had gh auth setup-git — works with proper env |
| Containers | ACR auth required | `az acr login --name fitfileregistry` |