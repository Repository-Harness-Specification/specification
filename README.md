# Repository Harness Specification

An open, vendor-neutral specification for making software repositories easier for coding agents to understand, operate, validate, and maintain.

> Status: experimental. Draft `0.2` is the current development version. Draft `0.1` remains available as a versioned snapshot.

## Why this project exists

Coding agents can inspect repositories, modify files, execute commands, run tests, and iterate on failures.

Repositories often expose their operating knowledge through one large instruction file such as `AGENTS.md` or `CLAUDE.md`.

The Repository Harness explores a different model:

```text
Root agent entry point
        ↓
.harness/harness.yaml
        ↓
repository-defined route
        ↓
small required context
        ↓
conditional context and validation
```

A supported root instruction file remains the entry point. The manifest defines how the repository classifies work, selects context, and validates changes.

## What changed in draft 0.2

The first benchmark found that draft `0.1` made the coding agent faster but did not reduce token consumption. Broad route labels caused the agent to load most registered documents for the tested task.

Draft `0.2` addresses that implementation flaw with:

- repository-defined concerns;
- repository-relative path scopes;
- ordered first-match routes;
- required and conditional context;
- concrete triggers for additional documents;
- environment-aware command registration;
- mandatory routing and validation evidence;
- unambiguous repository-root-relative paths.

The specification does not define universal task names or directory structures. Each repository defines its own vocabulary and routes.

See [RFC 0001](rfcs/0001-context-routing-v0.2.md) for the problem, alternatives, and evaluation plan.

## Goals

- Keep root agent instructions small.
- Expose the smallest justified repository context for a task.
- Separate human-readable guidance from executable operations.
- Remain independent from a specific model, agent, language, or operating system.
- Make validation reproducible and environment-aware.
- Allow repository-specific routing without imposing universal project categories.
- Measure quality, token efficiency, execution time, and scope discipline.

## Non-goals

- Replacing supported agent entry points.
- Replacing coding agents, agent skills, MCP, CI, or issue trackers.
- Defining one mandatory document tree, concern vocabulary, or route set.
- Claiming token savings without reproducible evidence.
- Copying the specification itself into adopting repositories.

## Current references

- [Current specification](SPECIFICATION.md)
- [Draft 0.2 immutable specification](versions/0.2/SPECIFICATION.md)
- [Draft 0.2 JSON Schema](schema/0.2/harness.schema.json)
- [Current schema alias](schema/harness.schema.json)
- [Current minimal example](examples/minimal)
- [Draft 0.2 minimal example](examples/0.2/minimal)
- [Draft 0.1 snapshot](versions/0.1/SPECIFICATION.md)
- [Draft 0.1 schema](schema/0.1/harness.schema.json)
- [Draft 0.1 minimal example](examples/0.1/minimal)

The current aliases follow the active draft. Versioned paths are immutable snapshots.

## Generate a harness from existing instructions

Until the `harness-me` CLI is available, migration prompts can be given to a coding agent.

- [Online migration prompt](prompts/migrate-monolithic-agent-instructions.md)
- [Offline migration prompt](prompts/migrate-monolithic-agent-instructions-offline.md)

The draft `0.2` prompts require the agent to:

- derive concerns and path scopes from the target repository;
- avoid universal `feature`, `bugfix`, or `implementation` routes unless they select meaningfully different context;
- distinguish required from conditional context;
- define environment-aware commands;
- simulate representative tasks before accepting the generated routes;
- produce a concise migration and routing audit report.

The exact `.harness` document set depends on the target repository.

## Minimal draft 0.2 shape

```yaml
spec: repository-harness/0.2

routing:
  strategy: first-match
  on_no_match: report

documents:
  - id: repository-defined-document
    path: .harness/REPOSITORY_DEFINED_DOCUMENT.md
    purpose: Repository-defined knowledge

concerns:
  - id: repository-defined-concern
    description: Repository-defined classification signal

commands:
  - id: repository-defined-validation
    run: ./.harness/scripts/validate.sh
    description: Repository-defined validation

routes:
  - id: repository-defined-route
    description: Repository-defined route
    match:
      concerns:
        any:
          - repository-defined-concern
    context:
      required:
        - repository-defined-document
      conditional: []
    validation:
      required:
        - repository-defined-validation
      conditional: []
```

This shape is illustrative. Use the schema and full example as the source of truth.

## Validate this repository

Install the small development dependency set and run:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_repository.py
```

The validator checks the current and versioned schemas, examples, references, paths, and selected routing anti-patterns.

## Project workflow

The project evolves through:

- real repository migrations;
- reproducible experiments;
- community feedback;
- RFCs;
- versioned reference implementations.

Design changes affecting the manifest, routing, conformance, or extension model begin as an RFC.

## Related article

[Coding Agents Evolved. Our Repositories Didn’t.](https://dev.to/lepsistemas/coding-agents-evolved-our-repositories-didnt-f4)

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md).
