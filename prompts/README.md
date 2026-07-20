# Repository Harness Migration Prompts

These prompts help teams adopt the current Repository Harness draft before dedicated tooling is available.

## Current target

The current prompts generate draft `0.2` manifests and are pinned to versioned `0.2` references.

They require repository-specific concern and path routing. They do not permit copying the minimal example's route names into an unrelated repository without evidence.

## Available prompts

### Online migration

[`migrate-monolithic-agent-instructions.md`](migrate-monolithic-agent-instructions.md)

Use this prompt when the coding agent can access public internet resources.

### Offline migration

[`migrate-monolithic-agent-instructions-offline.md`](migrate-monolithic-agent-instructions-offline.md)

Use this prompt when internet access is restricted. Attach the draft `0.2` specification, schema, and minimal manifest from the same versioned snapshot.

## Online usage

1. Open the target repository with the coding agent.
2. Create a branch for the migration.
3. Copy the complete online prompt into the session.
4. Allow the agent to read the pinned draft `0.2` references.
5. Review the generated harness and migration report.
6. Manually verify command availability in the target environment.
7. Run repository validation before merging.

## Offline usage

Attach these draft `0.2` files using the recognizable names below:

```text
SPECIFICATION.md
harness.schema.json
minimal-harness.yaml
```

Sources:

- [`versions/0.2/SPECIFICATION.md`](../versions/0.2/SPECIFICATION.md)
- [`schema/0.2/harness.schema.json`](../schema/0.2/harness.schema.json)
- [`examples/0.2/minimal/.harness/harness.yaml`](../examples/0.2/minimal/.harness/harness.yaml)

All attached files must come from the same draft version, release, or commit.

## Expected target changes

A typical migration creates or updates:

```text
AGENTS.md or another supported entry point

.harness/
├── harness.yaml
├── repository-specific documents
└── scripts when justified
```

The exact structure depends on the target repository.

The migration also creates a temporary:

```text
REPOSITORY_HARNESS_MIGRATION_REPORT.md
```

## Routing audit

Before accepting generated routes, review at least three representative task simulations.

Each simulation should identify:

- active repository-defined concerns;
- candidate path evidence;
- selected route;
- required context;
- conditional context and triggers;
- validation commands.

Reject or revise routes that load nearly all documents, duplicate another route, or depend only on broad labels without path or repository-specific evidence.

## Source of truth

1. Versioned specification.
2. Matching versioned JSON Schema.
3. Matching versioned official examples.

The JSON Schema is authoritative for manifest structure. The specification is authoritative for behavior and conformance.

## Limitations

Migration prompts do not guarantee correct routes, current commands, or complete repository knowledge. Every generated harness requires human review, schema validation, environment verification, and real repository validation.

These prompts are adoption helpers, not normative requirements.
