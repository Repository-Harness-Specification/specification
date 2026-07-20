\
#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import json
from pathlib import Path, PurePosixPath
import shlex
import sys
from typing import Any, Iterable

try:
    import yaml
except ImportError:
    print(
        "Missing dependency: PyYAML. Create a virtual environment and run: "
        ".venv/bin/python -m pip install -r requirements-dev.txt"
    )
    raise SystemExit(2)

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print(
        "Missing dependency: jsonschema. Create a virtual environment and run: "
        ".venv/bin/python -m pip install -r requirements-dev.txt"
    )
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
RECOMMENDED_LINES = 200
HARD_LINES = 250
RECOMMENDED_BYTES = 12 * 1024
HARD_BYTES = 16 * 1024


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
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest root must be an object")
    return value


def format_schema_path(parts: Iterable[Any]) -> str:
    rendered = "$"
    for part in parts:
        rendered += f"[{part}]" if isinstance(part, int) else f".{part}"
    return rendered


def validate_schema(
    instance: dict[str, Any],
    schema: dict[str, Any],
    label: str,
    result: Result,
) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: [str(part) for part in error.absolute_path],
    )
    for error in errors:
        result.error(
            f"{label}: {format_schema_path(error.absolute_path)}: {error.message}"
        )


def is_valid_repository_path(value: str) -> bool:
    if not value or "\\" in value or value.startswith("/"):
        return False
    if len(value) >= 2 and value[0].isalpha() and value[1] == ":":
        return False
    return ".." not in PurePosixPath(value).parts


def ensure_unique(
    items: list[dict[str, Any]],
    collection: str,
    result: Result,
) -> set[str]:
    seen: set[str] = set()
    for item in items:
        identifier = item.get("id")
        if not isinstance(identifier, str):
            continue
        if identifier in seen:
            result.error(f"{collection}: duplicate id '{identifier}'")
        seen.add(identifier)
    return seen


def selector_values(selector: dict[str, Any], kind: str) -> set[str]:
    values: set[str] = set()
    group = selector.get(kind, {})
    for operator in ("any", "all"):
        values.update(group.get(operator, []))
    return values


def selectors_in_manifest(manifest: dict[str, Any]) -> Iterable[tuple[str, dict[str, Any]]]:
    for index, route in enumerate(manifest.get("routes", [])):
        route_id = route.get("id", f"index-{index}")
        yield f"route '{route_id}' match", route.get("match", {})

        for item in route.get("context", {}).get("conditional", []):
            yield (
                f"route '{route_id}' conditional document '{item.get('document')}'",
                item.get("when", {}),
            )

        for item in route.get("validation", {}).get("conditional", []):
            yield (
                f"route '{route_id}' conditional command '{item.get('command')}'",
                item.get("when", {}),
            )

    for index, rule in enumerate(manifest.get("validation_rules", [])):
        yield f"validation rule {index}", rule.get("match", {})


def validate_manifest_budget(
    manifest_path: Path,
    result: Result,
) -> None:
    text = manifest_path.read_text(encoding="utf-8")
    logical_lines = [
        line
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    line_count = len(logical_lines)
    byte_count = len(text.encode("utf-8"))
    label = str(manifest_path.relative_to(ROOT))

    if line_count >= HARD_LINES:
        result.error(
            f"{label}: manifest has {line_count} non-blank, non-comment lines; "
            f"hard limit is below {HARD_LINES}"
        )
    elif line_count > RECOMMENDED_LINES:
        result.warn(
            f"{label}: manifest has {line_count} non-blank, non-comment lines; "
            f"recommended maximum is {RECOMMENDED_LINES}"
        )

    if byte_count >= HARD_BYTES:
        result.error(
            f"{label}: manifest is {byte_count} UTF-8 bytes; "
            f"hard limit is below {HARD_BYTES}"
        )
    elif byte_count > RECOMMENDED_BYTES:
        result.warn(
            f"{label}: manifest is {byte_count} UTF-8 bytes; "
            f"recommended maximum is {RECOMMENDED_BYTES}"
        )


def validate_no_empty_values(
    value: Any,
    label: str,
    result: Result,
    path: str = "$",
) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if child == {} or child == []:
                result.error(f"{label}: empty collection at {child_path}")
            validate_no_empty_values(child, label, result, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            validate_no_empty_values(child, label, result, f"{path}[{index}]")


def validate_command_path(
    command: dict[str, Any],
    label: str,
    example_root: Path,
    result: Result,
) -> None:
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
            result.error(
                f"{label}: invalid repository-relative executable path '{first}'"
            )
            return
        if not (example_root / normalized).exists():
            result.error(f"{label}: executable path does not exist: {normalized}")


def validate_selector_references(
    selector: dict[str, Any],
    label: str,
    concern_ids: set[str],
    scope_ids: set[str],
    result: Result,
) -> None:
    unknown_concerns = selector_values(selector, "concerns") - concern_ids
    if unknown_concerns:
        result.error(
            f"{label}: unknown concern ids: {sorted(unknown_concerns)}"
        )

    unknown_scopes = selector_values(selector, "scopes") - scope_ids
    if unknown_scopes:
        result.error(
            f"{label}: unknown scope ids: {sorted(unknown_scopes)}"
        )


def validate_manifest_cross_references(
    manifest: dict[str, Any],
    manifest_path: Path,
    result: Result,
) -> None:
    label = str(manifest_path.relative_to(ROOT))
    example_root = manifest_path.parents[1]

    documents = manifest.get("documents", [])
    scopes = manifest.get("scopes", [])
    concerns = manifest.get("concerns", [])
    commands = manifest.get("commands", [])
    routes = manifest.get("routes", [])
    validation_rules = manifest.get("validation_rules", [])

    document_ids = ensure_unique(documents, f"{label} documents", result)
    scope_ids = ensure_unique(scopes, f"{label} scopes", result)
    concern_ids = ensure_unique(concerns, f"{label} concerns", result)
    command_ids = ensure_unique(commands, f"{label} commands", result)
    ensure_unique(routes, f"{label} routes", result)

    if len(routes) > 6:
        result.warn(f"{label}: {len(routes)} routes; recommended starting maximum is 6")
    if len(concerns) > 8:
        result.warn(
            f"{label}: {len(concerns)} concerns; recommended starting maximum is 8"
        )

    entrypoint = manifest.get("entrypoint")
    if isinstance(entrypoint, str):
        if not is_valid_repository_path(entrypoint):
            result.error(f"{label}: invalid entrypoint path '{entrypoint}'")
        elif not (example_root / entrypoint).exists():
            result.error(f"{label}: entrypoint does not exist: {entrypoint}")

    for document in documents:
        path_value = document.get("path")
        if not isinstance(path_value, str):
            continue
        if not is_valid_repository_path(path_value):
            result.error(f"{label}: invalid document path '{path_value}'")
        elif not (example_root / path_value).exists():
            result.error(f"{label}: registered document does not exist: {path_value}")

    scope_signatures: dict[tuple[str, ...], str] = {}
    for scope in scopes:
        scope_id = scope.get("id", "<unknown>")
        paths = tuple(sorted(scope.get("paths", [])))
        previous = scope_signatures.get(paths)
        if previous:
            result.warn(
                f"{label}: scopes '{previous}' and '{scope_id}' have identical paths"
            )
        else:
            scope_signatures[paths] = str(scope_id)

    for command in commands:
        command_id = command.get("id")
        working_directory = command.get("working_directory")
        if isinstance(working_directory, str):
            if not is_valid_repository_path(working_directory):
                result.error(
                    f"{label}: invalid working_directory '{working_directory}'"
                )
            elif not (example_root / working_directory).exists():
                result.error(
                    f"{label}: working_directory does not exist: {working_directory}"
                )

        if command.get("mutates") is False:
            result.warn(
                f"{label} command '{command_id}': omit default 'mutates: false'"
            )
        if command.get("requires_approval") is False:
            result.warn(
                f"{label} command '{command_id}': "
                "omit default 'requires_approval: false'"
            )

        validate_command_path(
            command,
            f"{label} command '{command_id}'",
            example_root,
            result,
        )

    for selector_label, selector in selectors_in_manifest(manifest):
        validate_selector_references(
            selector,
            f"{label} {selector_label}",
            concern_ids,
            scope_ids,
            result,
        )

    broad_concerns = {
        "feature",
        "bugfix",
        "implementation",
        "change",
        "task",
        "refactoring",
        "validation",
        "completion",
    }
    route_signatures: dict[tuple[Any, ...], str] = {}
    document_route_count: Counter[str] = Counter()
    used_commands: set[str] = set()
    direct_path_groups: defaultdict[tuple[str, ...], list[str]] = defaultdict(list)

    for index, route in enumerate(routes):
        route_id = str(route.get("id", f"index-{index}"))
        match = route.get("match", {})
        route_concerns = selector_values(match, "concerns")

        if (
            route_concerns
            and not match.get("paths")
            and not match.get("scopes")
            and route_concerns <= broad_concerns
        ):
            result.warn(
                f"{label} route '{route_id}' relies only on broad concerns: "
                f"{sorted(route_concerns)}"
            )

        context = route.get("context", {})
        required_docs = context.get("required", [])
        conditional_docs = context.get("conditional", [])

        if len(required_docs) > 2:
            result.warn(
                f"{label} route '{route_id}' requires {len(required_docs)} documents"
            )

        conditional_doc_ids: list[str] = []
        for document_id in required_docs:
            document_route_count[document_id] += 1
            if document_id not in document_ids:
                result.error(
                    f"{label} route '{route_id}': "
                    f"unknown required document '{document_id}'"
                )

        for item in conditional_docs:
            document_id = item.get("document")
            conditional_doc_ids.append(document_id)
            document_route_count[document_id] += 1
            if document_id not in document_ids:
                result.error(
                    f"{label} route '{route_id}': "
                    f"unknown conditional document '{document_id}'"
                )

        overlap_docs = set(required_docs) & set(conditional_doc_ids)
        if overlap_docs:
            result.error(
                f"{label} route '{route_id}': documents cannot be required and "
                f"conditional: {sorted(overlap_docs)}"
            )

        validation = route.get("validation", {})
        required_commands = validation.get("required", [])
        conditional_commands = validation.get("conditional", [])
        conditional_command_ids: list[str] = []

        for command_id in required_commands:
            used_commands.add(command_id)
            if command_id not in command_ids:
                result.error(
                    f"{label} route '{route_id}': "
                    f"unknown required command '{command_id}'"
                )

        for item in conditional_commands:
            command_id = item.get("command")
            conditional_command_ids.append(command_id)
            used_commands.add(command_id)
            if command_id not in command_ids:
                result.error(
                    f"{label} route '{route_id}': "
                    f"unknown conditional command '{command_id}'"
                )

        overlap_commands = set(required_commands) & set(conditional_command_ids)
        if overlap_commands:
            result.error(
                f"{label} route '{route_id}': commands cannot be required and "
                f"conditional: {sorted(overlap_commands)}"
            )

        signature = (
            tuple(required_docs),
            tuple(
                (
                    item.get("document"),
                    json.dumps(item.get("when", {}), sort_keys=True),
                )
                for item in conditional_docs
            ),
            tuple(required_commands),
            tuple(
                (
                    item.get("command"),
                    json.dumps(item.get("when", {}), sort_keys=True),
                )
                for item in conditional_commands
            ),
        )
        previous = route_signatures.get(signature)
        if previous:
            result.warn(
                f"{label}: routes '{previous}' and '{route_id}' have identical "
                "context and validation"
            )
        else:
            route_signatures[signature] = route_id

    for index, rule in enumerate(validation_rules):
        for command_id in rule.get("commands", []):
            used_commands.add(command_id)
            if command_id not in command_ids:
                result.error(
                    f"{label} validation rule {index}: "
                    f"unknown command '{command_id}'"
                )

    route_count = len(routes)
    if route_count:
        for document_id, count in document_route_count.items():
            if count / route_count > 0.60:
                result.warn(
                    f"{label}: document '{document_id}' is referenced by "
                    f"{count}/{route_count} routes"
                )

    for selector_label, selector in selectors_in_manifest(manifest):
        paths = selector_values(selector, "paths")
        if len(paths) > 1:
            direct_path_groups[tuple(sorted(paths))].append(selector_label)

    for paths, locations in direct_path_groups.items():
        if len(locations) > 1:
            result.warn(
                f"{label}: repeated direct path group {list(paths)} in "
                f"{locations}; define a reusable scope"
            )

    unused_documents = document_ids - set(document_route_count)
    if unused_documents:
        result.warn(
            f"{label}: documents not referenced by routes: "
            f"{sorted(unused_documents)}"
        )

    used_scopes: set[str] = set()
    used_concerns: set[str] = set()
    for _, selector in selectors_in_manifest(manifest):
        used_scopes.update(selector_values(selector, "scopes"))
        used_concerns.update(selector_values(selector, "concerns"))

    unused_scopes = scope_ids - used_scopes
    if unused_scopes:
        result.warn(f"{label}: unused scopes: {sorted(unused_scopes)}")

    unused_concerns = concern_ids - used_concerns
    if unused_concerns:
        result.warn(f"{label}: unused concerns: {sorted(unused_concerns)}")

    unused_commands = command_ids - used_commands
    if unused_commands:
        result.warn(f"{label}: unused commands: {sorted(unused_commands)}")


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
        result.error(
            "schema/harness.schema.json must be identical to "
            "schema/0.2/harness.schema.json"
        )

    current_spec = (ROOT / "SPECIFICATION.md").read_text(encoding="utf-8")
    versioned_spec = (
        ROOT / "versions" / "0.2" / "SPECIFICATION.md"
    ).read_text(encoding="utf-8")
    if current_spec != versioned_spec:
        result.error(
            "SPECIFICATION.md must be identical to versions/0.2/SPECIFICATION.md"
        )

    examples = [
        (
            ROOT / "examples" / "minimal" / ".harness" / "harness.yaml",
            schema_02,
        ),
        (
            ROOT / "examples" / "0.1" / "minimal" / ".harness" / "harness.yaml",
            schema_01,
        ),
        (
            ROOT / "examples" / "0.2" / "minimal" / ".harness" / "harness.yaml",
            schema_02,
        ),
    ]

    for manifest_path, manifest_schema in examples:
        try:
            manifest = load_yaml(manifest_path)
        except Exception as exc:
            result.error(
                f"{manifest_path.relative_to(ROOT)}: invalid YAML: {exc}"
            )
            continue

        validate_schema(
            manifest,
            manifest_schema,
            str(manifest_path.relative_to(ROOT)),
            result,
        )

        if manifest.get("spec") == "repository-harness/0.2":
            validate_manifest_budget(manifest_path, result)
            validate_no_empty_values(
                manifest,
                str(manifest_path.relative_to(ROOT)),
                result,
            )
            validate_manifest_cross_references(
                manifest,
                manifest_path,
                result,
            )

    current_root = ROOT / "examples" / "minimal"
    versioned_root = ROOT / "examples" / "0.2" / "minimal"

    current_files = {
        path.relative_to(current_root)
        for path in current_root.rglob("*")
        if path.is_file()
    }
    versioned_files = {
        path.relative_to(versioned_root)
        for path in versioned_root.rglob("*")
        if path.is_file()
    }

    if current_files != versioned_files:
        result.error(
            "examples/minimal and examples/0.2/minimal contain different file sets"
        )
    else:
        for relative in sorted(current_files):
            if (
                current_root / relative
            ).read_bytes() != (
                versioned_root / relative
            ).read_bytes():
                result.error(
                    f"examples/minimal differs from examples/0.2/minimal "
                    f"at {relative}"
                )

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
