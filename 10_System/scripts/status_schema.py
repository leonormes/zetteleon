"""Loads 10_System/schema/status.yaml, the single source of truth for `status` values."""
from pathlib import Path

import yaml

_PATH = Path(__file__).resolve().parents[1] / "schema" / "status.yaml"
_DATA = yaml.safe_load(_PATH.read_text(encoding="utf-8"))

VALUES = set(_DATA["values"])
TIER1 = set(_DATA["tier1"])
TYPE_EXTRAS = {k: set(v) for k, v in _DATA.get("type_extras", {}).items()}
RETIRED = set(_DATA.get("retired", []))
