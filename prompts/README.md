# Repository Harness Migration Prompts

This directory contains reusable prompts that help teams adopt the Repository Harness Specification before dedicated tooling is available.

## Purpose

Many repositories already contain agent instructions in files such as:

- `AGENTS.md`;
- `CLAUDE.md`;
- `.github/copilot-instructions.md`;
- Cursor rules;
- internal repository handbooks;
- other agent-specific instruction files.

These files may contain valuable knowledge about architecture, testing, validation, environment setup, workflows, product constraints, and delivery expectations.

The prompts in this directory help a coding agent reorganize that knowledge into a modular Repository Harness.

## Available prompts

### Migrate monolithic agent instructions

[`migrate-monolithic-agent-instructions.md`](migrate-monolithic-agent-instructions.md)

Use this prompt to convert an existing large `AGENTS.md`, `CLAUDE.md`, or similar instruction file into a Repository Harness.

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
└── additional documents and scripts when justified
```

This is an example, not a mandatory document structure.

The exact capabilities and files depend on the target repository.

The prompt instructs the coding agent to:

- consult the official specification online;
- inspect the target repository before making changes;
- preserve existing rules;
- avoid unsupported assumptions;
- create a manifest compatible with the official schema;
- validate references and commands when possible;
- produce a migration report.

## The specification is not copied into the target repository

The migration prompt references the official public resources:

- `SPECIFICATION.md`;
- `schema/harness.schema.json`;
- the minimal `harness.yaml` example.

The coding agent uses those resources as external references.

The target repository should normally receive only:

- an updated or newly created root agent entry point;
- the `.harness/` directory;
- scripts required by that repository;
- a temporary migration report for human review.

The following files should not be copied into the target repository merely to perform a migration:

```text
SPECIFICATION.md
schema/harness.schema.json
examples/minimal/
prompts/
```

Those files remain maintained by the Repository Harness Specification project.

## How to use

1. Open the target repository with a coding agent.
2. Create a new branch for the migration.
3. Ensure the existing instruction file is available.
4. Copy the complete contents of the migration prompt into the agent session.
5. Ask the agent to perform the migration.
6. Review every created or modified file.
7. Compare the new harness with the original instruction file.
8. Run the repository's real validation commands.
9. Review the migration report.
10. Commit the migration only after human review.

Example request:

```text
Follow the instructions in the prompt below.

Migrate this repository's current AGENTS.md into a Repository Harness.

Preserve all meaningful rules, create a migration report, and identify
anything that could not be verified.

<paste the complete migration prompt here>
```

A coding agent with web access should retrieve the official specification resources directly.

If the agent cannot access the official references, it must disclose that limitation and must not claim verified specification compliance.

## Important limitations

These prompts do not guarantee a correct migration.

A coding agent may still:

- misunderstand an architectural rule;
- classify information under the wrong capability;
- preserve obsolete instructions;
- miss contradictions;
- reference commands that do not work in every environment;
- generate a manifest that was not formally validated;
- create validation scripts that do not propagate failure correctly.

Every migration requires human review and real validation.

## Non-normative status

The files in this directory are adoption helpers.

They are not normative requirements of the Repository Harness Specification.

A repository can conform to the specification without using these prompts.

Future versions may replace or complement these prompts with the `harness-me` CLI.

## Contributing a prompt

A new prompt should:

- solve a specific Repository Harness adoption problem;
- remain vendor-neutral when possible;
- avoid depending on one coding agent;
- reference an explicit specification version;
- state its assumptions and limitations;
- preserve human review as a required step;
- avoid presenting generated output as automatically correct.

Prompt additions or major changes should be proposed through the repository's RFC process.
