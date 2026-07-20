# Repository Harness Specification

An open, vendor-neutral specification for making software repositories easier
for coding agents to understand, operate, validate, and maintain.

> Status: experimental. Draft `0.2` is the current development version and may
> be revised until a release tag freezes it. Draft `0.1` remains available.

## Why this project exists

Coding agents can inspect repositories, modify files, execute commands, run
tests, and iterate on failures.

Repositories often expose their operating knowledge through one large
instruction file such as `AGENTS.md` or `CLAUDE.md`.

The Repository Harness explores a different model:

```text
Root agent entry point
        ↓
small routing manifest
        ↓
repository-defined route
        ↓
small required context
        ↓
triggered context and path-aware validation
```

A supported root instruction file remains the entry point. The manifest routes
work to repository knowledge and executable validation.

## What draft 0.2 is testing

The first benchmark found that draft `0.1` made the coding agent faster but did
not reduce uncached input tokens. Broad routing caused the agent to load most
registered documents.

The first real `0.2` migration exposed a second problem: the generated manifest
grew into a new monolith.

The current draft addresses both failures with:

- repository-defined reusable path scopes;
- optional concerns;
- compact route objects;
- required and conditional context;
- path-aware shared validation rules;
- environment-aware commands;
- routing evidence;
- recommended and hard manifest size budgets;
- migration prompts that require simplification before acceptance.

The specification defines routing mechanics, not universal task names or
directory structures.

## Manifest budget

The root manifest should remain a small routing index:

```text
Recommended: 200 non-blank, non-comment lines and 12 KiB
Hard limit:  250 non-blank, non-comment lines and 16 KiB
```

Large prose explanations belong in registered Markdown documents. Repeated
operations belong in scripts. Repeated path groups belong in scopes.

## Goals

- Keep root agent instructions and the routing manifest small.
- Expose the smallest justified repository context for a task.
- Separate human-readable guidance from executable operations.
- Remain independent from a specific agent, language, or operating system.
- Make validation reproducible and environment-aware.
- Support repository-specific routing without universal project categories.
- Measure quality, token usage, time, and scope discipline.

## Non-goals

- Replacing supported agent entry points.
- Replacing coding agents, agent skills, MCP, CI, or issue trackers.
- Defining one mandatory document tree or concern vocabulary.
- Claiming token savings without reproducible evidence.
- Copying the specification into adopting repositories.

## Current references

- [Current specification](SPECIFICATION.md)
- [Draft 0.2 development specification](versions/0.2/SPECIFICATION.md)
- [Draft 0.2 JSON Schema](schema/0.2/harness.schema.json)
- [Current schema alias](schema/harness.schema.json)
- [Current minimal example](examples/minimal)
- [Draft 0.2 minimal example](examples/0.2/minimal)
- [Draft 0.1 snapshot](versions/0.1/SPECIFICATION.md)
- [RFC 0001](rfcs/0001-context-routing-v0.2.md)

The current aliases follow the active draft. Versioned development paths become
immutable when the draft is frozen by a release or tag.

## Generate a harness

Until the `harness-me` CLI exists, use:

- [Online migration prompt](prompts/migrate-monolithic-agent-instructions.md)
- [Offline migration prompt](prompts/migrate-monolithic-agent-instructions-offline.md)

The prompts require the agent to:

- start with reusable path scopes;
- add concerns only when needed;
- keep the manifest within a concrete budget;
- avoid duplicate routes and speculative context;
- use shared validation rules;
- simulate representative tasks;
- produce a concise migration report.

## Minimal draft 0.2 shape

```yaml
spec: repository-harness/0.2

routing:
  strategy: first-match
  on_no_match: report

documents:
  - id: repository-guidance
    path: .harness/GUIDANCE.md
    purpose: Task-specific repository guidance

scopes:
  - id: source
    paths:
      - src/**
      - tests/**

commands:
  - id: validate
    run: ./.harness/scripts/validate.sh
    description: Run repository validation

validation_rules:
  - match:
      scopes:
        any:
          - source
    commands:
      - validate

routes:
  - id: source-change
    description: Change implementation or tests
    match:
      scopes:
        any:
          - source
    context:
      required:
        - repository-guidance
```

The example is illustrative. The schema and full minimal example are the source
of truth.

## Validate this repository

Use a virtual environment on distributions that enforce PEP 668:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_repository.py
```

The validator checks schemas, aliases, examples, references, paths, manifest
budgets, duplicate outcomes, repeated path groups, and selected routing
anti-patterns.

## Project workflow

The project evolves through:

- real repository migrations;
- reproducible experiments;
- community feedback;
- RFCs;
- versioned reference implementations.

Design changes affecting the manifest, routing, conformance, or extension model
begin as an RFC.

## Related article

[Coding Agents Evolved. Our Repositories Didn’t.](https://dev.to/lepsistemas/coding-agents-evolved-our-repositories-didnt-f4)

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md).
