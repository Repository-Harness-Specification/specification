# Repository Harness Specification

An open, vendor-neutral specification for making software repositories easier for coding agents to understand, operate, validate, and maintain.

> Status: early draft. The current structure is experimental and is not yet a finalized standard.

## Why this project exists

Coding agents can inspect repositories, modify files, execute commands, run tests, and iterate on failures.

Repositories, however, often expose their operating knowledge through one large instruction file such as `AGENTS.md` or `CLAUDE.md`.

This project explores a different model:

```text
Root agent entry point
        ↓
.harness/
├── harness.yaml
├── architecture
├── environment
├── validation
└── workflows
```

A supported root instruction file, usually `AGENTS.md`, remains the entry point.

The Repository Harness provides modular, versioned, discoverable, and executable context that agents can load according to the current task.

## Goals

- Keep the root agent instruction file small.
- Support progressive disclosure of repository context.
- Separate human-readable guidance from executable commands.
- Remain independent from a specific model or coding agent.
- Make repository validation reproducible.
- Allow teams to extend the harness with their own capabilities.
- Measure whether the approach improves quality, token efficiency, or both.

## Non-goals

- Replacing `AGENTS.md`, `CLAUDE.md`, or other supported agent entry points.
- Replacing coding agents, Agent Skills, MCP, CI, or issue trackers.
- Defining one mandatory document structure for every repository.
- Claiming token savings before reproducible experiments exist.
- Requiring every repository to use the same capabilities or workflows.
- Copying the specification itself into every adopting repository.

## Start with an existing `AGENTS.md` or `CLAUDE.md`

Many repositories already contain a large `AGENTS.md`, `CLAUDE.md`, or another agent-specific instruction file.

Until the `harness-me` CLI is available, this repository provides migration prompts that can be given to a coding agent.

The prompts instruct the agent to:

- inspect the target repository;
- read the official Repository Harness Specification;
- analyze the existing repository instructions;
- preserve meaningful rules and constraints;
- create a small root entry point;
- organize detailed knowledge under `.harness/`;
- create a valid `.harness/harness.yaml`;
- avoid inventing commands or architecture rules;
- identify unresolved or unverifiable information;
- produce a concise migration report for human review.

Two migration modes are available:

- [Online migration prompt](prompts/migrate-monolithic-agent-instructions.md)
- [Offline migration prompt](prompts/migrate-monolithic-agent-instructions-offline.md)

Use the online prompt when the coding agent can access this public repository.

Use the offline prompt when internet access is restricted. In that case, the specification, schema, and minimal example must be downloaded manually and attached to the agent session.

The user does not need to copy `SPECIFICATION.md`, the JSON Schema, or the reference examples into the target repository.

A typical migration result may look like:

```text
AGENTS.md
.harness/
├── harness.yaml
├── README.md
├── PROJECT.md
├── ARCHITECTURE.md
├── BOOTSTRAP.md
├── VALIDATION.md
├── WORKFLOWS.md
└── scripts/
```

The exact document set depends on the repository.

These prompts are adoption helpers. They are not normative parts of the specification.

## Review the migration report

Both migration prompts create:

```text
REPOSITORY_HARNESS_MIGRATION_REPORT.md
```

This file is a temporary human-review artifact.

It is not part of the Repository Harness itself and must not be registered in `.harness/harness.yaml`.

The report is intentionally concise and exception-based. It should normally remain under 60 lines.

It should summarize:

- the migration result;
- files created or modified;
- instructions that were removed, changed, merged, or left unresolved;
- schema and repository validation results;
- manual decisions still required.

It should not include:

- a complete list of every file inspected;
- a mapping for every successfully migrated section;
- repeated descriptions of the same validation result;
- shell commands that are not relevant to the review;
- implementation details that do not require a human decision.

Before accepting the migration, a human reviewer should verify:

- that important instructions were preserved;
- that reported exceptions were handled correctly;
- that schema validation succeeded;
- that repository validation results are understood;
- that unresolved questions have an owner or decision.

The expected workflow is:

```text
generate → review exceptions → correct → validate → approve → remove report
```

The report may be removed after the migration has been reviewed and accepted.

A project may preserve it only when it intentionally wants to retain the migration history.

## Official references

- [Repository Harness Specification](SPECIFICATION.md)
- [Manifest JSON Schema](schema/harness.schema.json)
- [Minimal Repository Harness example](examples/minimal)
- [Minimal manifest example](examples/minimal/.harness/harness.yaml)

These resources are the source of truth for migrations and implementations.

The JSON Schema is authoritative for the structure of `.harness/harness.yaml`.

The minimal example demonstrates one valid implementation. It is not a mandatory directory structure.

## Minimal example

A minimal implementation is available in:

[`examples/minimal`](examples/minimal)

The example demonstrates:

- a small `AGENTS.md` entry point;
- a `.harness/harness.yaml` manifest;
- modular repository documents;
- executable validation;
- progressive discovery of task-relevant context.

## Repository structure

```text
.
├── README.md
├── SPECIFICATION.md
├── TERMINOLOGY.md
├── DESIGN_PRINCIPLES.md
├── ROADMAP.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── schema/
│   └── harness.schema.json
├── examples/
│   └── minimal/
├── prompts/
│   ├── README.md
│   ├── migrate-monolithic-agent-instructions.md
│   └── migrate-monolithic-agent-instructions-offline.md
├── rfcs/
├── scripts/
└── .github/
```

## Current work

1. Define the minimum viable Repository Harness.
2. Apply it manually to real repositories.
3. Document migration patterns and adoption problems.
4. Build reproducible monolithic-versus-modular benchmarks.
5. Measure task success, validation results, token usage, and execution time.
6. Publish results before stabilizing the specification.
7. Build tooling only after the manual workflow is understood.

## Specification status

The current document structure, manifest format, and capability names are experimental.

Draft `0.1` currently uses:

```yaml
spec: repository-harness/0.1
```

References in the migration prompts currently point to the `main` branch while draft `0.1` is evolving.

Once the draft is frozen, migration prompts should reference a specific release tag so that the same prompt always resolves to the same specification version.

The project evolves through:

- real repository migrations;
- reproducible experiments;
- community feedback;
- RFCs;
- reference implementations.

See [ROADMAP.md](ROADMAP.md) for planned work.

## Related article

[Coding Agents Evolved. Our Repositories Didn’t.](https://dev.to/lepsistemas/coding-agents-evolved-our-repositories-didnt-f4)

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md).

Design changes should begin as an RFC.
