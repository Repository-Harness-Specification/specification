# Design Principles

## 1. Vendor neutrality

The specification must not depend on a single coding agent, model provider,
issue tracker, CI platform, programming language, operating system, project
domain, or directory structure.

## 2. Human readability

Harness files must remain useful to developers, reviewers, architects, QA
engineers, and product teams.

## 3. Selective progressive disclosure

Repositories should expose the smallest justified context for the current task.

Modular files alone are not progressive disclosure. Additional context should
require repository-defined concern, scope, or path evidence.

## 4. Manifest economy

The root manifest is a routing index, not a second repository handbook.

Repeated paths should become scopes, repeated validation should become shared
rules, and explanatory guidance should remain in documents.

## 5. Repository-owned routing

The specification defines routing mechanics. Each repository defines its own
scopes, concerns, route order, context, and validation.

## 6. Executability

Operational knowledge should point to reproducible commands instead of relying
only on prose.

## 7. Environment awareness

A command should declare checkable availability requirements when missing tools
or platform differences would otherwise produce repeated failures.

## 8. Evidence over claims

The project should measure task success, regressions, loaded context, token
usage, execution time, command attempts, and scope discipline before claiming
improvements.

## 9. Auditability

An agent should report which route it selected, which documents it loaded, why
conditional context triggered, and which validations ran.

## 10. Extensibility

The core should remain small while allowing project-specific scopes, concerns,
commands, and integrations.

## 11. Repository ownership

The harness belongs to the repository, evolves with it, and is reviewed through
normal version-control workflows.

## 12. Explicit uncertainty

Draft features, unsupported automation, unavailable commands, manual checks,
and missing metrics should be identified clearly.

## 13. No hidden precedence

The specification must distinguish repository-owned rules from instructions
enforced by the agent runtime or user.

## 14. Start manually

Tooling should automate a workflow only after the workflow has been tested
manually in real repositories.
