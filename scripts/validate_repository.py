#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ROOT / "README.md",
    ROOT / "SPECIFICATION.md",
    ROOT / "schema" / "harness.schema.json",
    ROOT / "examples" / "minimal" / "AGENTS.md",
    ROOT / "examples" / "minimal" / ".harness" / "harness.yaml",
]


def main() -> int:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        print("Missing required files:")
        for path in missing:
            print(f"- {path}")
        return 1

    schema_path = ROOT / "schema" / "harness.schema.json"
    try:
        json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Invalid JSON Schema: {exc}")
        return 1

    print("Repository structure and JSON Schema are valid.")
    print("YAML schema validation will be added when the draft format stabilizes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
