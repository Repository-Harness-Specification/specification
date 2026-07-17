# Repository Harness Migration Prompts

This directory contains prompts that help teams adopt the Repository Harness Specification before dedicated tooling is available.

## Available prompts

### Online migration

[`migrate-monolithic-agent-instructions.md`](migrate-monolithic-agent-instructions.md)

Use this prompt when the coding agent can access public internet resources.

The agent reads the official specification, schema, and minimal example directly from this repository.

### Offline migration

[`migrate-monolithic-agent-instructions-offline.md`](migrate-monolithic-agent-instructions-offline.md)

Use this prompt when the coding agent cannot access the internet because of network restrictions, security policies, isolated environments, or corporate controls.

The required reference files must be downloaded manually and attached to the agent session.

## Online usage

1. Open the target repository with the coding agent.
2. Create a branch for the migration.
3. Copy the complete online migration prompt into the agent session.
4. Allow the agent to read the official public references.
5. Review the generated harness and migration report.
6. Run the repository validation commands before merging.

The official references are:

- `SPECIFICATION.md`
- `schema/harness.schema.json`
- `examples/minimal/.harness/harness.yaml`

The target repository does not need to contain copies of these files.

## Offline usage

Download the following files from the same specification version:

- [`SPECIFICATION.md`](../SPECIFICATION.md)
- [`schema/harness.schema.json`](../schema/harness.schema.json)
- [`examples/minimal/.harness/harness.yaml`](../examples/minimal/.harness/harness.yaml)

Attach them to the coding agent session using these recognizable filenames:

```text
SPECIFICATION.md
harness.schema.json
minimal-harness.yaml
```

Then copy the complete offline migration prompt into the same session.

The attached files are reference material for the migration session. They should not be copied into the target repository.

All reference files must come from the same branch, tag, release, or commit.

When stable releases are available, prefer files from a fixed release tag instead of `main`.

## Expected target repository changes

A typical migration creates or updates:

```text
AGENTS.md or another supported entry point

.harness/
├── harness.yaml
├── README.md
├── capability documents
└── scripts when justified
```

The exact structure depends on the target repository.

The migration also creates:

```text
REPOSITORY_HARNESS_MIGRATION_REPORT.md
```

## Review the migration report

`REPOSITORY_HARNESS_MIGRATION_REPORT.md` is a temporary human-review artifact.

It is not:

- a harness capability;
- a normative specification file;
- a document that should be registered in `.harness/harness.yaml`.

The report should be concise, exception-based, and normally no longer than 60 lines.

It should contain:

- a short migration status;
- files created or modified;
- instructions that were removed, changed, merged, or left unresolved;
- a single validation summary;
- manual decisions still required.

It should not contain:

- every file inspected by the agent;
- a complete mapping of sections migrated without issues;
- repeated validation descriptions;
- routine shell commands;
- implementation details that require no human decision.

A detailed section mapping is only necessary when:

- an instruction was not migrated;
- multiple rules were merged and their meaning may have changed;
- a rule was intentionally removed;
- conflicting sources required a decision;
- the agent could not determine the correct destination.

Before merging the migration, review:

- reported exceptions;
- assumptions and unresolved questions;
- schema validation status;
- repository validation results;
- manual checks still required.

The expected workflow is:

```text
generate → review exceptions → correct → validate → approve → remove report
```

The report may be removed after the migration has been reviewed and accepted.

A project may preserve it only when it intentionally wants to retain the migration history.

## Source of truth

The authoritative sources are:

1. `SPECIFICATION.md`
2. `schema/harness.schema.json`
3. official examples

The JSON Schema is authoritative for the structure of `.harness/harness.yaml`.

The minimal example demonstrates one valid implementation. It is not a mandatory directory structure.

The prompts intentionally do not reproduce the schema or manifest format. This prevents them from becoming outdated copies of the specification.

## Important limitations

These prompts do not guarantee a correct migration.

A coding agent may still:

- misunderstand an architectural rule;
- classify information under the wrong capability;
- preserve obsolete instructions;
- miss contradictions;
- register invalid commands;
- create validation scripts that do not correctly propagate failures.

Every migration requires human review and real repository validation.

## Non-normative status

These prompts are adoption helpers.

They are not normative requirements of the Repository Harness Specification.

A repository can conform to the specification without using them.

Future versions may replace or complement these prompts with the `harness-me` CLI.
