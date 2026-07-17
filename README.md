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

Until the `harness-me` CLI is available, this repository provides a migration prompt that can be given to a coding agent.

The prompt instructs the agent to:

- inspect the target repository;
- read the official Repository Harness Specification online;
- analyze the existing monolithic instruction file;
- preserve meaningful rules and constraints;
- create a small root entry point;
- organize detailed knowledge under `.harness/`;
- create a valid `.harness/harness.yaml`;
- avoid inventing commands or architecture rules;
- identify unresolved or unverifiable information;
- produce a migration report for human review.

See:

[`prompts/migrate-monolithic-agent-instructions.md`](prompts/migrate-monolithic-agent-instructions.md)

The user does not need to copy `SPECIFICATION.md`, the JSON Schema, or the reference examples into the target repository.

The coding agent reads those resources from this official public repository and creates only the harness artifacts required by the target project.

A typical result may look like:

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

## Official references

- [Repository Harness Specification](SPECIFICATION.md)
- [Manifest JSON Schema](schema/harness.schema.json)
- [Minimal Repository Harness example](examples/minimal)
- [Minimal manifest example](examples/minimal/.harness/harness.yaml)

The public raw versions of these files may be consumed directly by coding agents during migration.

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
│   └── migrate-monolithic-agent-instructions.md
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

References in the migration prompt currently point to the `main` branch while draft `0.1` is evolving.

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
