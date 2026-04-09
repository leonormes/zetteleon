---
created: 2026-04-08T17:48:04+00:00
modified: 2026-04-09T08:10:59+00:00
title: README
---

## ProdOS frontmatter—CUE Schema

### Why CUE?

[CUE](https://cuelang.org/) is useful here because it:

- Expresses sum types cleanly (`atomic` must have `atomic.form`; `protocol` must have `protocol`), which are awkward in JSON Schema `if`/`then`.
- Serves as a readable specification next to the human SoT ([SoT - ProdOS Note Metadata (Frontmatter)](../../30_Library/SoT/SoT%20-%20ProdOS%20Note%20Metadata%20(Frontmatter).md)).
- Validates JSON extracted from Markdown YAML with a single CLI command.

The JSON Schema in `../schemas/prodos-note-frontmatter.schema.json` remains useful for tools that only speak JSON Schema; keep both aligned when the spec changes.

### Validate One Extracted Frontmatter JSON File

From the repo root (or this folder):

```bash
cue vet -d '#Frontmatter' path/to/frontmatter.json prodos_frontmatter.cue
```

Silent on success; errors on stderr on failure.

### Scan the Vault (recommended)

Use the Python helper (install [PyYAML](https://pypi.org/project/PyYAML/)):

```bash
pip install -r ../scripts/requirements-validate.txt
python3 ../scripts/validate_note_frontmatter.py
```

Options:

- `--enforce-prodos`—exit with non-zero if a file under the library roots has no `prodos` key (for CI once migration is far enough along).
- `--_roots`—override default scan roots (defaults include `30_Library`, `10_System/prompts`, `20_Thinking/21_Workbench` relative to vault root).

The script expects the `cue` binary on `PATH` for `prodos`-bearing notes. If `cue` is missing, it falls back to reporting YAML parse errors and missing-`prodos` status only (unless `--require-cue` is passed, which exits with an error).
