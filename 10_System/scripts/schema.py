"""Loads the vault's closed vocabularies: 10_System/schema/status.yaml and enums.yaml.

The single source of truth for `status`, `type`, `epistemic_status` and the typed-edge
vocabulary. Importing scripts must have PyYAML (run with `uv run --with pyyaml`).
"""
from pathlib import Path

import yaml

_DIR = Path(__file__).resolve().parents[1] / "schema"
_STATUS = yaml.safe_load((_DIR / "status.yaml").read_text(encoding="utf-8"))
_ENUMS = yaml.safe_load((_DIR / "enums.yaml").read_text(encoding="utf-8"))

# status.yaml
VALUES = set(_STATUS["values"])
TIER1 = set(_STATUS["tier1"])
TYPE_EXTRAS = {k: set(v) for k, v in _STATUS.get("type_extras", {}).items()}
RETIRED = set(_STATUS.get("retired", []))

# enums.yaml
TYPE = set(_ENUMS["type"])
EPISTEMIC_STATUS = set(_ENUMS["epistemic_status"])
EDGE_RELATIONS = set(_ENUMS["edge_relations"])
EDGE_CONFIDENCE = set(_ENUMS["edge_confidence"])
EDGE_STRENGTH_MIN = int(_ENUMS["edge_strength"]["min"])
EDGE_STRENGTH_MAX = int(_ENUMS["edge_strength"]["max"])
