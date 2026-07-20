#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path, PurePosixPath
import shlex
import sys
from typing import Any, Iterable

try:
    import yaml
except ImportError:
    print("Missing dependency: PyYAML. Run: python3 -m pip install -r requirements-dev.txt")
    raise SystemExit(2)

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("Missing dependency: jsonschema. Run: python3 -m pip install -r requirements-dev.txt")
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Result:
    errors: list[str]
    warnings: list[str]

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("manifest root must be an object")
    return data


def format_jsonschema_path(parts: Iterable[Any]) -> str:
    rendered = "$"
    for part in parts:
        if isinstance(part, int):
            rendered += f"[{part}]"
        else:
            rendered += f".{part}"
    return rendered


def validate_schema_instance(instance: dict[str, Any], schema: dict[str, Any], label: str, result: Result) -> None:
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path)):
        result.error(f"{label}: {format_jsonschema_path(error.absolute_path)}: {error.message}")


def is_valid_repository_path(value: str) -> bool:
    if not value or "\\" in value or value.startswith("/"):
        return False
    if len(value) >= 2 and value[0].isalpha() and value[1] == ":":
        return False
    return ".." not in PurePosixPath(value).parts


def ensure_unique(items: list[dict[str, Any]], collection: str, result: Result) -> set[str]:
    seen: set[str] = set()
    for item in items:
        identifier = item.get("id")
        if identifier in seen:
            result.error(f"{collection}: duplicate id '{identifier}'")
        elif isinstance(identifier, str):
            seen.add(identifier)
    return seen


def referenced_selector_concerns(selector: dict[str, Any]) -> set[str]:
    concerns: set[str] = set()
    group = selector.get("concerns", {})
    for key in ("any", "all"):
        concerns.update(group.get(key, []))
    return concerns


def validate_command_path(command: dict[str, Any], label: str, example_root: Path, result: Result) -> None:
    run = command.get("run", "")
    try:
        tokens = shlex.split(run)
    except ValueError as exc:
        result.error(f"{label}: invalid command quoting: {exc}")
        return
    if not tokens:
        return
    first = tokens[0]
    if first.startswith("./") or first.startswith(".\\"):
        normalized = first.replace("\\", "/")
        if not is_valid_repository_path(normalized):
            result.error(f"{label}: invalid repository-relative executable path '{first}'")
            return
        target = example_root / normalized
        if not target.exists():
            result.error(f"{label}: executable path does not exist: {normalized}")


def validate_manifest_cross_references(manifest: dict[str, Any], manifest_path: Path, result: Result) -> None:
    label = str(manifest_path.relative_to(ROOT))
    documents = manifest.get("documents", [])
    concerns = manifest.get("concerns", [])
    commands = manifest.get("commands", [])
    routes = manifest.get("routes", [])

    document_ids = ensure_unique(documents, f"{label} documents", result)
    concern_ids = ensure_unique(concerns, f"{label} concerns", result)
    command_ids = ensure_unique(commands, f"{label} commands", result)
    ensure_unique(routes, f"{label} routes", result)

    entrypoint = manifest.get("entrypoint")
    if isinstance(entrypoint, str):
        if not is_valid_repository_path(entrypoint):
            result.error(f"{label}: invalid entrypoint path '{entrypoint}'")
        elif not (manifest_path.parents[1] / entrypoint).exists():
            result.error(f"{label}: entrypoint does not exist relative to example root: {entrypoint}")

    example_root = manifest_path.parents[1]

    for document in documents:
        path_value = document.get("path")
        if not isinstance(path_value, str):
            continue
        if not is_valid_repository_path(path_value):
            result.error(f"{label}: invalid document path '{path_value}'")
            continue
        if not (example_root / path_value).exists():
            result.error(f"{label}: registered document does not exist: {path_value}")

    for command in commands:
        working_directory = command.get("working_directory")
        if isinstance(working_directory, str):
            if not is_valid_repository_path(working_directory):
                result.error(f"{label}: invalid working_directory '{working_directory}'")
            elif not (example_root / working_directory).exists():
                result.error(f"{label}: working_directory does not exist: {working_directory}")
        validate_command_path(command, f"{label} command '{command.get('id')}'", example_root, result)

    broad_concerns = {"feature", "bugfix", "implementation", "change", "task", "refactoring", "validation", "completion"}
    signatures: dict[tuple[Any, ...], str] = {}

    for index, route in enumerate(routes):
        route_id = route.get("id", f"index-{index}")
        match = route.get("match", {})
        referenced = referenced_selector_concerns(match)
        unknown = referenced - concern_ids
        if unknown:
            result.error(f"{label} route '{route_id}': unknown concern ids in match: {sorted(unknown)}")

        context = route.get("context", {})
        required_docs = context.get("required", [])
        conditional_docs = context.get("conditional", [])

        for document_id in required_docs:
            if document_id not in document_ids:
                result.error(f"{label} route '{route_id}': unknown required document '{document_id}'")

        conditional_doc_ids: list[str] = []
        for item in conditional_docs:
            document_id = item.get("document")
            conditional_doc_ids.append(document_id)
            if document_id not in document_ids:
                result.error(f"{label} route '{route_id}': unknown conditional document '{document_id}'")
            trigger_unknown = referenced_selector_concerns(item.get("when", {})) - concern_ids
            if trigger_unknown:
                result.error(f"{label} route '{route_id}': unknown concern ids in document trigger: {sorted(trigger_unknown)}")

        overlap_docs = set(required_docs) & set(conditional_doc_ids)
        if overlap_docs:
            result.error(f"{label} route '{route_id}': documents cannot be both required and conditional: {sorted(overlap_docs)}")

        validation = route.get("validation", {})
        required_commands = validation.get("required", [])
        conditional_commands = validation.get("conditional", [])

        for command_id in required_commands:
            if command_id not in command_ids:
                result.error(f"{label} route '{route_id}': unknown required command '{command_id}'")

        conditional_command_ids: list[str] = []
        for item in conditional_commands:
            command_id = item.get("command")
            conditional_command_ids.append(command_id)
            if command_id not in command_ids:
                result.error(f"{label} route '{route_id}': unknown conditional command '{command_id}'")
            trigger_unknown = referenced_selector_concerns(item.get("when", {})) - concern_ids
            if trigger_unknown:
                result.error(f"{label} route '{route_id}': unknown concern ids in command trigger: {sorted(trigger_unknown)}")

        overlap_commands = set(required_commands) & set(conditional_command_ids)
        if overlap_commands:
            result.error(f"{label} route '{route_id}': commands cannot be both required and conditional: {sorted(overlap_commands)}")

        if document_ids and len(set(required_docs)) == len(document_ids):
            result.warn(f"{label} route '{route_id}' requires every registered document")
        elif document_ids and len(set(required_docs)) / len(document_ids) >= 0.75:
            result.warn(f"{label} route '{route_id}' requires at least 75% of registered documents")

        paths_present = bool(match.get("paths"))
        if referenced and not paths_present and referenced <= broad_concerns:
            result.warn(f"{label} route '{route_id}' relies only on broad concern labels: {sorted(referenced)}")

        signature = (
            tuple(required_docs),
            tuple((item.get("document"), json.dumps(item.get("when", {}), sort_keys=True)) for item in conditional_docs),
            tuple(required_commands),
            tuple((item.get("command"), json.dumps(item.get("when", {}), sort_keys=True)) for item in conditional_commands),
        )
        previous = signatures.get(signature)
        if previous:
            result.warn(f"{label} routes '{previous}' and '{route_id}' have identical context and validation")
        else:
            signatures[signature] = str(route_id)

    used_commands = {
        command_id
        for route in routes
        for command_id in route.get("validation", {}).get("required", [])
    }
    used_commands.update(
        item.get("command")
        for route in routes
        for item in route.get("validation", {}).get("conditional", [])
    )
    unused = command_ids - used_commands
    if unused:
        result.warn(f"{label}: commands not used by any route validation: {sorted(unused)}")


def main() -> int:
    result = Result(errors=[], warnings=[])

    required_files = [
        ROOT / "README.md",
        ROOT / "SPECIFICATION.md",
        ROOT / "versions" / "0.1" / "SPECIFICATION.md",
        ROOT / "versions" / "0.2" / "SPECIFICATION.md",
        ROOT / "schema" / "harness.schema.json",
        ROOT / "schema" / "0.1" / "harness.schema.json",
        ROOT / "schema" / "0.2" / "harness.schema.json",
        ROOT / "examples" / "minimal" / "AGENTS.md",
        ROOT / "examples" / "minimal" / ".harness" / "harness.yaml",
        ROOT / "examples" / "0.1" / "minimal" / ".harness" / "harness.yaml",
        ROOT / "examples" / "0.2" / "minimal" / ".harness" / "harness.yaml",
        ROOT / "rfcs" / "0001-context-routing-v0.2.md",
    ]

    for path in required_files:
        if not path.exists():
            result.error(f"missing required file: {path.relative_to(ROOT)}")

    if result.errors:
        for error in result.errors:
            print(f"ERROR: {error}")
        return 1

    schema_alias = load_json(ROOT / "schema" / "harness.schema.json")
    schema_01 = load_json(ROOT / "schema" / "0.1" / "harness.schema.json")
    schema_02 = load_json(ROOT / "schema" / "0.2" / "harness.schema.json")

    if schema_alias != schema_02:
        result.error("schema/harness.schema.json must be identical to schema/0.2/harness.schema.json")

    if (ROOT / "SPECIFICATION.md").read_text(encoding="utf-8") != (ROOT / "versions" / "0.2" / "SPECIFICATION.md").read_text(encoding="utf-8"):
        result.error("SPECIFICATION.md must be identical to versions/0.2/SPECIFICATION.md")

    examples = [
        (ROOT / "examples" / "minimal" / ".harness" / "harness.yaml", schema_02),
        (ROOT / "examples" / "0.1" / "minimal" / ".harness" / "harness.yaml", schema_01),
        (ROOT / "examples" / "0.2" / "minimal" / ".harness" / "harness.yaml", schema_02),
    ]

    for manifest_path, schema in examples:
        try:
            manifest = load_yaml(manifest_path)
        except Exception as exc:
            result.error(f"{manifest_path.relative_to(ROOT)}: invalid YAML: {exc}")
            continue
        validate_schema_instance(manifest, schema, str(manifest_path.relative_to(ROOT)), result)
        if manifest.get("spec") == "repository-harness/0.2":
            validate_manifest_cross_references(manifest, manifest_path, result)

    current_root = ROOT / "examples" / "minimal"
    versioned_root = ROOT / "examples" / "0.2" / "minimal"
    current_files = {path.relative_to(current_root) for path in current_root.rglob("*") if path.is_file()}
    versioned_files = {path.relative_to(versioned_root) for path in versioned_root.rglob("*") if path.is_file()}
    if current_files != versioned_files:
        result.error("examples/minimal and examples/0.2/minimal contain different file sets")
    else:
        for relative in sorted(current_files):
            if (current_root / relative).read_bytes() != (versioned_root / relative).read_bytes():
                result.error(f"examples/minimal differs from examples/0.2/minimal at {relative}")

    for warning in result.warnings:
        print(f"WARNING: {warning}")

    if result.errors:
        for error in result.errors:
            print(f"ERROR: {error}")
        return 1

    print("Repository Harness Specification files are valid.")
    print(f"Warnings: {len(result.warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
