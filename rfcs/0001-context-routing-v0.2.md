# RFC 0001: Selective context routing for draft 0.2

- Status: Draft
- Authors: Repository Harness Specification contributors
- Created: 2026-07-19

## Summary

Introduce repository-defined concerns, path-aware ordered routes, required and conditional context, command availability metadata, and a mandatory routing evidence report in draft `0.2`.

## Problem

Draft `0.1` modularized repository knowledge but did not make context loading selective enough.

Its document-level `load_when` values were broad, and routes typically grouped architecture, workflow, and validation guidance for generic categories such as `feature` and `bugfix`. In the first benchmark, the modular harness preserved a 100% manual success rate and completed the task faster, but used more uncached input tokens than the monolithic `AGENTS.md` variant.

The benchmark showed that splitting documentation does not automatically create progressive disclosure. The specification needs an explicit, repository-owned, auditable routing protocol.

Draft `0.1` also contained an ambiguous path model: the specification described document paths as relative to `.harness`, while migration guidance used repository-relative paths.

## Goals

- Make route selection repository-specific instead of standardizing project categories.
- Combine concern classification with repository-defined path scopes.
- Load a small required context set first.
- Prevent speculative loading of additional registered documents.
- Make additional context conditional on concrete concern or path evidence.
- Check command availability before execution.
- Make context and validation selection auditable.
- Define one unambiguous repository-relative path model.
- Preserve vendor neutrality.

## Non-goals

- Standardizing concern names such as gameplay, database, frontend, or infrastructure.
- Defining a universal repository directory structure.
- Requiring deterministic natural-language classification without agent reasoning.
- Guaranteeing token reduction for every repository or task.
- Replacing CI, task runners, agent skills, or runtime permission systems.

## Proposal

### Repository-defined concerns

A manifest declares concern identifiers, descriptions, and optional signals. The repository owns this vocabulary.

### Ordered route matching

Routes are evaluated in manifest order using `first-match` semantics. A route may match concerns, repository-relative glob paths, or both. Narrow routes should appear before broad routes.

### Required and conditional context

Documents no longer declare global `load_when` or `required` fields.

Each route declares:

- `context.required`, loaded immediately after route selection;
- `context.conditional`, loaded only when a declared selector matches concrete evidence.

### Environment-aware commands

Commands may declare required executables, platforms, and environment variables. Agents check availability before execution and report unavailable commands instead of repeatedly improvising alternatives.

### Routing evidence

Before reporting completion, the agent reports active concerns, the selected route, path evidence, loaded documents, conditional trigger evidence, selected validation, and command results.

### Repository-relative paths

All manifest paths are relative to the repository root, use `/`, and prohibit absolute paths and `..` traversal.

## Examples

```yaml
routes:
  - id: source-change
    description: Change implementation or tests
    match:
      concerns:
        any:
          - source-change
      paths:
        any:
          - src/**
          - tests/**
    context:
      required:
        - workflows
      conditional:
        - document: architecture
          when:
            concerns:
              any:
                - architecture-boundary
          reason: Load architecture only after boundary-changing evidence appears
    validation:
      required:
        - validate
      conditional: []
```

The identifiers and patterns above are illustrative. Each repository defines its own routes.

## Compatibility

Draft `0.2` is intentionally not schema-compatible with `0.1`.

Migration requires:

- changing the specification identifier;
- converting document paths to repository-root-relative paths;
- removing document-level loading rules;
- defining concerns and routing policy;
- replacing route `load` and `validate` arrays with context and validation objects;
- updating the root entry point.

Versioned `0.1` specification, schema, and example snapshots remain available.

## Security and safety

Availability checks must be read-only. Command mutation and approval metadata remain explicit. A route cannot override runtime or user permissions.

Conditional context reduces the amount of repository information exposed to an agent, but it does not create a security boundary.

## Alternatives considered

### Keep descriptive `load_when` labels

Rejected because broad labels did not constrain actual document loading.

### Standardize universal task categories

Rejected because repositories have different domains, architecture, paths, and operational needs.

### Route only by directory

Rejected because a path alone may not reveal whether a change is architectural, behavioral, security-sensitive, or documentation-only.

### Route only by concern

Rejected because natural-language concern matching can remain too broad. Path evidence provides a second repository-owned signal.

### Allow agents to load any optional document

Rejected because speculative optional loading recreates the draft `0.1` behavior. Draft `0.2` requires concrete conditional triggers.

## Evaluation plan

1. Migrate the same benchmark repository to draft `0.2`.
2. Validate all registered commands manually in the benchmark environment.
3. Run the same warm-up and measured task sequence used for draft `0.1`.
4. Record selected route, loaded documents, trigger evidence, validation, command count, execution time, total input, cached input, uncached input, output, and success.
5. Compare draft `0.2` against the monolithic baseline and draft `0.1` results.

Success requires preserving implementation quality while loading fewer documents and reducing uncached input without losing the execution-time improvement observed in draft `0.1`.

## Open questions

- Should a future version define machine-verifiable glob matching semantics more precisely?
- Should route transitions replace or accumulate validation obligations?
- Should context budgets or maximum document counts become optional manifest fields?
- Should command availability support a registered read-only probe command?
