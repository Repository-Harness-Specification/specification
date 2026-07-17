# Repository Harness Specification

## Status

Draft `0.1`.

This document defines the first experimental contract for a repository-owned harness. It is intentionally small and expected to change after real-world usage and benchmarking.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** describe requirement levels in this specification.

## 1. Purpose

A Repository Harness is a versioned contract stored with a repository that helps coding agents and humans discover:

- relevant project knowledge;
- operational commands;
- validation requirements;
- task-specific workflows;
- completion criteria;
- optional project-defined extensions.

## 2. Discovery

A conforming repository MUST contain a root-level `AGENTS.md` or another agent-supported entry point.

For version `0.1`, the entry point MUST direct the agent to `.harness/harness.yaml`.

Example:

```markdown
# Agent Instructions

This repository uses a Repository Harness.
Read `.harness/harness.yaml` before making changes.
Load only the documents required for the current task.
Run the required validation commands before reporting completion.
```

The `.harness` directory is a proposed convention. Coding agents are not expected to understand it without instructions from the supported entry point.

## 3. Manifest

A conforming repository MUST contain:

```text
.harness/harness.yaml
```

The manifest MUST declare:

- the specification version;
- a repository name;
- registered documents;
- registered commands;
- task or workflow routes when progressive disclosure is used.

The manifest SHOULD validate against `schema/harness.schema.json`.

## 4. Documents

A document registration describes a repository capability, not a mandatory filename.

Examples of capabilities include:

- architecture;
- bootstrap;
- environment;
- validation;
- testing;
- security;
- workflows;
- Definition of Ready;
- Definition of Done.

A small repository MAY combine multiple capabilities in one document. A larger repository MAY split one capability into multiple documents.

Each registered document MUST have:

- a stable identifier;
- a relative path inside `.harness`;
- a short purpose;
- one or more conditions describing when it is relevant.

## 5. Progressive disclosure

A harness SHOULD help an agent load only the context relevant to the current task.

The harness MUST NOT require every registered document to be loaded for every task unless the repository explicitly chooses that behavior.

Routes MAY be based on task categories such as:

- bootstrap;
- feature;
- bugfix;
- refactoring;
- test change;
- dependency change;
- infrastructure change;
- release;
- completion review.

Routes are guidance in version `0.1`. A coding agent may require explicit instructions to apply them.

## 6. Commands

A harness SHOULD expose reproducible commands for operations such as:

- bootstrap;
- build;
- unit tests;
- integration tests;
- lint;
- architecture checks;
- security checks;
- full validation.

Markdown SHOULD explain when and why a command is used. Scripts or task runners SHOULD define how it is executed.

A command registration MUST include:

- a stable identifier;
- an executable command;
- a short description.

Commands SHOULD be safe to run repeatedly where practical.

## 7. Validation

Validation is the broader capability that may include:

- compilation;
- static analysis;
- formatting;
- unit tests;
- integration tests;
- architecture checks;
- security checks;
- manual verification.

Testing MAY live inside the validation capability or in a dedicated testing capability.

A repository SHOULD define the minimum validation required before an agent reports a task as complete.

An agent MUST NOT claim successful validation when the required command was not executed or did not succeed.

## 8. Definition of Ready and Definition of Done

Teams MAY encode an agreed Definition of Ready and Definition of Done in the harness.

A Definition of Ready may be used to evaluate tasks from Jira, GitHub Issues, Linear, Azure DevOps, another issue tracker, or an internal backlog before implementation begins.

A Definition of Done SHOULD be agreed by the team before implementation and MAY define required tests, reviews, documentation updates, validations, and manual checks.

## 9. Precedence

A repository harness MUST NOT claim precedence over system-level, platform-level, organization-level, or explicit user instructions enforced by the active coding agent.

Inside the repository-owned harness, more specific task or directory rules MAY refine broader rules, but MUST NOT silently contradict repository-wide constraints.

Repositories SHOULD document their internal precedence rules.

## 10. Security

A harness MUST NOT contain secrets, credentials, private keys, or production tokens.

Commands that are destructive, privileged, expensive, or capable of affecting external systems MUST be clearly identified.

The harness SHOULD distinguish read-only validation from mutating operations.

## 11. Extensions

Repositories MAY define custom document capabilities, commands, workflows, metadata, and integrations.

Extensions MUST use namespaced identifiers when collision is possible.

Example:

```yaml
extensions:
  com.example.jira-readiness:
    version: "1"
    config: integrations/jira-readiness.yaml
```

## 12. Conformance

A repository conforms to draft `0.1` when:

1. it has a supported root entry point;
2. the entry point points to `.harness/harness.yaml`;
3. the manifest is syntactically valid;
4. all registered document paths exist;
5. all required command identifiers are unique;
6. the repository declares at least one validation command;
7. no required field violates the published schema.

Conformance does not imply that the harness is complete, optimal, or automatically understood by every coding agent.
