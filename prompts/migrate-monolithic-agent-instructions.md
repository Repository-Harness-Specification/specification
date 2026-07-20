# Migrate monolithic agent instructions to Repository Harness draft 0.2

Migrate the target repository's existing agent instructions into a Repository Harness conforming to draft `0.2`.

You are operating inside the target repository.

## Authoritative references

Before modifying the repository, read these pinned draft `0.2` references:

- Specification:
  https://raw.githubusercontent.com/Repository-Harness-Specification/specification/main/versions/0.2/SPECIFICATION.md

- Manifest schema:
  https://raw.githubusercontent.com/Repository-Harness-Specification/specification/main/schema/0.2/harness.schema.json

- Minimal example:
  https://raw.githubusercontent.com/Repository-Harness-Specification/specification/main/examples/0.2/minimal/.harness/harness.yaml

These resources are the source of truth for this migration.

The JSON Schema is authoritative for manifest structure. The specification is authoritative for behavior and conformance. The minimal example is illustrative.

Do not copy the specification, schema, or reference example into the target repository.

Do not reproduce or extend the manifest format based only on this prompt.

If any authoritative reference cannot be accessed, stop and report that the migration cannot be verified.

## Inspect the target repository

Inspect relevant sources before creating files, including:

- existing `AGENTS.md`, `CLAUDE.md`, Copilot, Cursor, or other agent instructions;
- repository directory and module boundaries;
- architecture and design documentation;
- testing and validation documentation;
- contributor and bootstrap documentation;
- build, test, lint, and validation scripts;
- project or dependency manifests;
- CI workflows;
- roadmap and product constraints.

Inspect enough repository structure to derive repository-specific concerns and path scopes. Do not load or duplicate unrelated documentation merely to create a large harness.

Do not infer that an example, planned feature, or aspirational design already exists in the implementation.

## Objectives

1. Preserve meaningful rules and their original authority.
2. Replace the monolithic instruction file with a small supported entry point.
3. Move detailed repository knowledge into repository-appropriate files under `.harness/` or register existing authoritative repository documents.
4. Create `.harness/harness.yaml` according to draft `0.2`.
5. Derive concerns, paths, documents, commands, and routes from the target repository.
6. Select a small required context set for each route.
7. Make additional context conditional on concrete concern or path evidence.
8. Register reproducible commands and checkable availability requirements when justified.
9. Avoid inventing commands, paths, tools, architecture rules, concerns, or project requirements.
10. Identify contradictory, obsolete, duplicated, or unverifiable instructions.
11. Simulate representative tasks and revise broad or duplicate routes.
12. Produce a concise migration and routing audit report for human review.

## Target output

Create only the artifacts required by the target repository:

```text
AGENTS.md or another supported entry point

.harness/
├── harness.yaml
├── repository-specific knowledge documents
└── scripts when justified
```

Do not create empty documents.

Do not create every document, concern, route, or command shown by the minimal example.

Create:

```text
REPOSITORY_HARNESS_MIGRATION_REPORT.md
```

The report is a temporary human-review artifact and must not be registered in `harness.yaml`.

## Routing requirements

The routing vocabulary belongs to the target repository.

Do not create universal `feature`, `bugfix`, `implementation`, `refactoring`, or `validation` routes unless each route selects meaningfully different context or validation based on repository evidence.

Use repository-defined concerns and repository-relative path scopes.

Order routes from narrowest to broadest because draft `0.2` uses first-match semantics.

Each route must define:

- how it matches concerns, paths, or both;
- a minimal `context.required` set;
- conditional documents with concrete triggers and reasons;
- required and conditional validation commands.

Do not make a document globally required merely because it may sometimes be useful.

Do not place architecture, workflow, bootstrap, testing, and validation documents into every route by default.

Do not create two routes with the same effective context and validation unless their selection behavior is meaningfully different and documented.

When no route can be derived safely, prefer `routing.on_no_match: report` and record the missing decision instead of creating a catch-all route that loads all documents.

## Path requirements

All manifest paths are relative to the repository root.

Use `/` separators. Do not use absolute paths, Windows drive prefixes, backslashes, or `..` traversal.

Reference only paths that exist, except route glob patterns that intentionally describe candidate files.

## Command requirements

Prefer existing project commands over unnecessary wrappers.

Create scripts only when they improve reproducibility, failure propagation, portability, or CI verification.

Commands must propagate non-zero exit status.

Declare checkable availability requirements when missing executables, platform restrictions, or required environment variables are known.

Do not report an unavailable, skipped, or failed required command as successful.

Separate automated validation from manual verification.

Do not improvise unregistered replacement commands unless repository instructions explicitly authorize them.

## Entry-point requirements

The supported root entry point must instruct the agent to:

1. read `.harness/harness.yaml`;
2. classify repository-defined concerns;
3. perform shallow path discovery;
4. select the first matching route;
5. load required context only;
6. load conditional context only after its trigger matches;
7. re-evaluate routing when scope changes;
8. check command availability;
9. report routing and validation evidence.

Keep the entry point concise.

## Representative-task simulation

Before accepting the generated harness, simulate at least three materially different tasks representative of this repository.

At least one simulation should be narrow enough that architecture or full validation guidance is not automatically required, when the repository supports such a task.

For each simulation, record:

- task summary;
- active concerns;
- candidate path evidence;
- selected route;
- required documents;
- conditional documents and whether their triggers match;
- required and conditional validation.

Revise the manifest when:

- unrelated documents would load;
- nearly every route loads nearly every document;
- two routes produce the same context and validation;
- a broad concern is the only selector;
- route order selects a broader route before a narrower route;
- no-match behavior silently loads all documents.

## Verification

After migration:

1. compare original instructions with the new harness;
2. confirm every substantive rule has a destination or a reported exception;
3. validate `harness.yaml` against the pinned draft `0.2` schema;
4. verify identifiers and cross-references;
5. verify registered document and command paths;
6. execute safe availability checks;
7. execute safe required validation commands when possible;
8. confirm command failures return non-zero status;
9. record unavailable and unexecuted commands;
10. confirm the representative-task simulations use selective context;
11. report unresolved questions and manual checks.

Do not claim draft `0.2` conformance unless schema and cross-reference validation succeed.

Do not claim repository validation succeeded when a required or triggered command failed, was unavailable, or was not run.

## Migration report

Create a concise `REPOSITORY_HARNESS_MIGRATION_REPORT.md`, normally under 90 lines.

Use this structure:

```markdown
# Repository Harness Migration Report

Status: Ready for review | Needs decisions | Validation failed

## Summary

Briefly describe what was migrated.

## Changes

- Files created:
- Files modified:

## Exceptions requiring review

List only removed, changed, merged, contradicted, unresolved, or unverifiable instructions.
Write `None` when there are no exceptions.

## Routing audit

| Example task | Concerns and path evidence | Selected route | Required context | Triggered context | Validation |
| --- | --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... | ... |

## Validation

| Check | Result | Notes |
| --- | --- | --- |
| Draft 0.2 schema | Passed/Failed/Not run | |
| Registered references | Passed/Failed/Not run | |
| Command availability | Passed/Failed/Partial/Not run | |
| Repository validation | Passed/Failed/Partial/Not run | |

## Next actions

List only remaining human decisions, environment repairs, or manual checks.
```

Do not include every file inspected, routine shell commands, repeated validation descriptions, or successful details that require no human decision.

Do not claim the migration is ready when schema validation or required repository validation failed.
