# RFC 0001: Selective and compact context routing for draft 0.2

- Status: Draft
- Authors: Repository Harness Specification contributors
- Created: 2026-07-19
- Revised: 2026-07-19

## Summary

Introduce repository-defined path scopes, optional concerns, ordered routes,
required and conditional context, environment-aware commands, shared validation
rules, manifest size budgets, and auditable routing evidence.

## Problem

Draft `0.1` modularized repository knowledge but did not make context loading
selective enough.

Its broad labels typically grouped architecture, workflow, and validation
guidance for generic categories. In the first benchmark, the modular harness
preserved a 100 percent manual success rate and completed the task faster, but
used more uncached input tokens than the monolithic `AGENTS.md` variant.

The first real draft `0.2` migration exposed another failure mode. The generated
`harness.yaml` exceeded 500 lines. Routes, repeated paths, static reasons, empty
arrays, and duplicated validation turned the routing manifest into a new
monolith.

Splitting documents is not progressive disclosure, and a large routing index is
not a solution to a large instruction file.

## Goals

- Keep the root manifest compact and maintainable.
- Make route selection repository-specific.
- Reuse path scopes instead of repeating globs.
- Use concerns only where paths are insufficient.
- Load a small required context set first.
- Prevent speculative loading of additional documents.
- Share validation rules across routes.
- Check command availability before execution.
- Make context and validation selection auditable.
- Preserve vendor neutrality.

## Non-goals

- Standardizing concern or scope names.
- Defining a universal directory structure.
- Requiring deterministic natural-language classification.
- Guaranteeing token reduction for every task.
- Replacing CI, task runners, agent skills, or runtime permissions.
- Standardizing external route catalogs in this revision.

## Proposal

### Manifest budget

The manifest should remain below 200 non-blank, non-comment lines and 12 KiB.
It must remain below 250 lines and 16 KiB.

The manifest omits empty collections, default false values, static reasons, and
prose that belongs in documents.

### Reusable scopes

A repository registers named path groups once and references them from routes,
conditional context, and validation rules.

### Optional concerns

Concerns are used only when intent changes routing and paths alone are
insufficient.

### Ordered route matching

Routes use first-match semantics and are ordered from narrowest to broadest.

### Required and conditional context

A route loads required context immediately. Conditional context loads only after
its selector matches concrete evidence.

Runtime evidence replaces static `reason` prose.

### Shared validation rules

Validation that depends on changed paths may be declared once under
`validation_rules` instead of repeated in every route.

### Environment-aware commands

Commands may declare executables, platforms, and environment variables.
Unavailable commands are reported without repeated improvisation.

### Routing evidence

The agent reports the selected route, evidence, loaded documents, triggered
context, validation selection, and command results.

## Example

```yaml
scopes:
  - id: source
    paths:
      - src/**
      - tests/**

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
        - workflows
      conditional:
        - document: architecture
          when:
            scopes:
              any:
                - architecture-boundary
```

## Compatibility

Draft `0.2` is not schema-compatible with `0.1`.

Earlier development revisions of `0.2` also require migration:

- remove conditional `reason`;
- omit empty collections;
- add reusable scopes where paths repeat;
- make concerns optional;
- move repeated route validation into `validation_rules`;
- reduce the root manifest to the published budget.

Draft `0.1` remains preserved.

## Security and safety

Availability checks must be read-only. Command mutation and approval metadata
remain explicit. Routes cannot override runtime or user permissions.

Reducing context does not create a security boundary.

## Alternatives considered

### Change only the migration prompt

Rejected. A prompt-only fix would still leave verbose manifests valid and would
not provide validator enforcement.

### Keep static reasons

Rejected. Selectors already declare triggers, and runtime evidence is more
accurate than repeated static prose.

### Require concerns in every repository

Rejected. Many repositories can route accurately using path scopes alone.

### Duplicate validation inside routes

Rejected when validation depends on shared changed-path rules.

### Enforce only a line limit

Rejected as the only control. Line limits can be gamed by compressed YAML, so
byte budgets and semantic anti-pattern checks are also required.

## Evaluation plan

1. Regenerate the benchmark repository harness using the revised prompt.
2. Verify the generated manifest is within budget.
3. Simulate the benchmark task and confirm only the smallest expected document
   set is loaded.
4. Validate all registered commands manually in the benchmark environment.
5. Run the same warm-up and measured sequence used previously.
6. Record loaded documents, route evidence, command count, execution time,
   cached and uncached input, output, and success.
7. Compare revised draft `0.2` with the monolithic baseline and draft `0.1`.

Success requires preserving implementation quality while loading fewer
documents and reducing uncached input without losing the execution-time
improvement observed in draft `0.1`.

## Open questions

- Should external route catalogs become a core feature for very large monorepos?
- Should future schemas define exact glob semantics?
- Should route transitions replace or accumulate validation obligations?
- Should commands support a registered read-only availability probe?
