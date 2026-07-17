# Repository Harness Specification

An open, vendor-neutral specification for making software repositories easier for coding agents to understand, operate, validate, and maintain.

> Status: early draft. The current structure is an experiment, not a finalized standard.

## Why this project exists

Coding agents can inspect repositories, modify files, execute commands, run tests, and iterate on failures. Repositories, however, often expose their operating knowledge through one large instruction file.

This project explores a different model:

```text
AGENTS.md
    ↓
.harness/
├── harness.yaml
├── architecture
├── environment
├── validation
└── workflows
```

`AGENTS.md` remains the universal entry point. The repository harness provides modular, versioned, discoverable, and executable context.

## Goals

- Keep the root agent instruction file small.
- Support progressive disclosure of repository context.
- Separate human-readable guidance from executable commands.
- Remain independent from a specific model or coding agent.
- Make repository validation reproducible.
- Allow teams to extend the harness with their own capabilities.
- Measure whether the approach improves quality, token efficiency, or both.

## Non-goals

- Replacing `AGENTS.md`.
- Replacing coding agents, Agent Skills, MCP, CI, or issue trackers.
- Defining one mandatory directory tree for every repository.
- Claiming token savings before reproducible experiments exist.

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
├── rfcs/
├── scripts/
└── .github/
```

## Current work

1. Define the minimum viable repository harness.
2. Apply it manually to a real repository.
3. Build reproducible monolithic-versus-modular benchmarks.
4. Publish results before stabilizing the specification.
5. Build tooling only after the manual workflow is understood.

## Related article

[ Coding Agents Evolved. Our Repositories Didn’t.](https://dev.to/lepsistemas/coding-agents-evolved-our-repositories-didnt-f4)

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Design changes should begin as an RFC.
