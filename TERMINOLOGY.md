# Terminology

## Agent Harness

The runtime around a model that provides tools, state, execution loops, permissions, and feedback. Codex, Claude Code, and similar products provide agent-harness capabilities.

## Repository Harness

A repository-owned, versioned contract that describes how agents and humans discover project knowledge, select task-relevant context, execute operations, validate changes, and determine completion.

## Entry Point

A file already understood by a coding agent, such as `AGENTS.md`, that directs the agent to the repository harness.

## Manifest

The machine-readable `.harness/harness.yaml` file that registers documents, concerns, commands, ordered routes, and extensions.

## Document

A human-readable repository file registered in the manifest. Draft `0.2` routes decide when it is loaded.

## Concern

A repository-defined classification signal used to match routes or trigger conditional context. Concern names are not standardized by the specification.

## Signal

A short repository-defined indicator that helps an agent classify a concern from the request or implementation evidence.

## Candidate Path

A repository-relative path likely to be affected, identified through shallow discovery before modification.

## Changed Path

A repository-relative path modified during the task. Changed paths are used to re-evaluate routing and conditional triggers.

## Route

An ordered repository-defined mapping from concern and path selectors to required context, conditional context, and validation commands.

## Selector

A set of concern or path conditions using `any` and `all` matching semantics.

## Required Context

Documents loaded immediately after a route is selected.

## Conditional Context

Documents that must not be loaded until a declared selector matches concrete concern or path evidence.

## Command

A reproducible operation registered in the manifest, usually backed by a script or task runner.

## Command Availability

Declared executable, platform, or environment-variable requirements checked before a command runs.

## Routing Report

The concise evidence record containing active concerns, selected route, path evidence, loaded documents, conditional triggers, and validation results.

## Progressive Disclosure

Loading the smallest justified repository context first and adding registered context only when declared evidence makes it relevant.

## Definition of Ready

Team-agreed criteria used to determine whether a task contains enough information to begin implementation.

## Definition of Done

Team-agreed criteria, established before implementation, that define what must be true before work is considered complete.
