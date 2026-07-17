# Design Principles

## 1. Vendor neutrality

The specification must not depend on a single coding agent, model provider, issue tracker, CI platform, programming language, or operating system.

## 2. Human readability

Harness files must remain useful to developers, reviewers, architects, QA engineers, and product teams.

## 3. Progressive disclosure

Repositories should expose the smallest useful context for the current task.

## 4. Executability

Operational knowledge should point to reproducible commands instead of relying only on prose.

## 5. Evidence over claims

The project should measure task success, regressions, token usage, execution time, and scope discipline before claiming improvements.

## 6. Extensibility

The core should remain small while allowing project-specific capabilities and integrations.

## 7. Repository ownership

The harness belongs to the repository, evolves with it, and is reviewed through normal version-control workflows.

## 8. Explicit uncertainty

Draft features, unsupported automation, manual checks, and unavailable metrics should be identified clearly.

## 9. No hidden precedence

The specification must distinguish repository-owned rules from instructions enforced by the agent runtime or user.

## 10. Start manually

Tooling should automate a workflow only after the workflow has been tested manually in real repositories.
