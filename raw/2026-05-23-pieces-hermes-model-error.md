---
created: 2026-05-23T19:15:00+00:00
modified: 2026-07-20T16:33:05+00:00
permalink: llmeon/raw/2026-05-23-pieces-hermes-model-error
pieces_ids: [6b51a1a5-8b0d-4486-882c-357389e69e2a, 731b9ccf-4135-4c1f-8bd1-92ea4b77ca6e, 978debe8-6314-45e4-bded-677ffc55ad6c, e0116cd3-e5c8-4d67-9f36-2f0becd652e0, eca53792-f633-4ed1-a886-d0a9cca0a8b2]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-05-23-pieces-hermes-model-error
---

## Hermes qwen/qwen3.5:cloud Model ID Error Diagnosis

### Asset 1 (Pieces: eca53792-f633-4ed1-a886-d0a9cca0a8b2)

### Diagnosis complete—here's the Full Picture

#### Root Cause Confirmed

The error `qwen/qwen3.5:cloud is not a valid model ID` is not coming from your main config. The filesystem grep proves it:

- `~/.hermes/config.yaml` (live) → `default: qwen/qwen3.5-plus-20260420` ✅ valid
- `~/.local/share/chezmoi/private_dot_hermes/private_config.yaml` (chezmoi source) → `default: qwen/qwen3.5-plus-20260420` ✅ valid

The stale `qwen3.5:cloud` string lives in your profile YAML files, not your main config.

### Asset 2 (Pieces: e0116cd3-e5c8-4d67-9f36-2f0becd652e0)

Everything needed is now on the table. Here is the complete, grounded diagnosis and fix.

---

### Diagnosis: the `qwen/qwen3.5:cloud` Error

#### Root Cause Confirmed from Filesystem

Both the live config (`/Users/leon.ormes/.hermes/config.yaml`) and the chezmoi source (`/Users/leon.ormes/.local/share/chezmoi/private_dot_hermes/private_config.yaml`) show the exact same value on disk:

```yaml
model:
  default: qwen/qwen3.5-plus-20260420
```

That is the correct OpenRouter model ID. The error comes from a stale profile YAML file still referencing `qwen/qwen3.5:cloud`.

### Asset 3 (Pieces: 978debe8-6314-45e4-bded-677ffc55ad6c)

The `config.yaml` read returned the critical piece of information. I can now see exactly what's happening. Here's the diagnosis and fix:

---

### Root Cause Identified

The live `~/.hermes/config.yaml` file clearly shows:

```yaml
model:
  default: qwen/qwen3.5-plus-20260420
```

But the error you're hitting is:

```
'qwen/qwen3.5:cloud is not a valid model ID'
```

These are two different things. Your `config.yaml` on disk already has the correct ID `qwen/qwen3.5-plus-20260420`—which is a valid OpenRouter model. The stale reference is in a profile YAML file.

### Asset 4 (Pieces: 6b51a1a5-8b0d-4486-882c-357389e69e2a)

The user is getting an error when trying to run the `/goal` prompt in Hermes. The error is:

```
Error: Error code: 400 - {'error': {'message': 'qwen/qwen3.5:cloud is not a valid model ID', 'code': 400}, 'user_id': 'user_2mtquAqy8vut24biZwv73iWzILo'}
```

This is an OpenRouter API error—`qwen/qwen3.5:cloud` is not a valid model ID on OpenRouter.

### Asset 5 (Pieces: 731b9ccf-4135-4c1f-8bd1-92ea4b77ca6e)

I am getting [[/goal Diagnose a.. [96 lines].. e SOUL.md §1.5 or §1.6 rules]]

Error: Error code: 400 - {'error': {'message': 'qwen/qwen3.5:cloud is not a valid model ID', 'code': 400}, 'user_id': 'user_2mtquAqy8vut24biZwv73iWzILo'}
