# Terminology

## Agent Harness

The runtime around a model that provides tools, state, execution loops, permissions, and feedback. Codex, Claude Code, and similar products provide agent-harness capabilities.

## Repository Harness

A repository-owned, versioned contract that describes how agents and humans discover project knowledge, execute operations, validate changes, and determine completion.

## Entry Point

A file already understood by a coding agent, such as `AGENTS.md`, that directs the agent to the repository harness.

## Manifest

The machine-readable `.harness/harness.yaml` file that registers documents, commands, routes, and extensions.

## Capability

A semantic area exposed by the harness, such as architecture, bootstrap, validation, testing, security, readiness, or completion.

## Document

A human-readable file registered in the manifest that explains a capability.

## Command

A reproducible operation registered in the manifest, usually backed by a script or task runner.

## Route

A mapping from a task category to relevant documents and required commands.

## Progressive Disclosure

Loading repository context as it becomes relevant instead of loading the entire repository operating manual for every task.

## Definition of Ready

Team-agreed criteria used to determine whether a task contains enough information to begin implementation.

## Definition of Done

Team-agreed criteria, established before implementation, that define what must be true before work is considered complete.
