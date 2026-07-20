# Migrate monolithic agent instructions to Repository Harness draft 0.2 without internet access

Migrate the target repository's existing agent instructions into a Repository
Harness conforming to draft `0.2`.

You are operating inside the target repository without internet access.

## Required attached references

Before modifying the repository, confirm these files are attached to the
current agent session and come from the same draft `0.2` commit:

```text
SPECIFICATION.md
harness.schema.json
minimal-harness.yaml
```

The schema is authoritative for manifest structure. The specification is
authoritative for behavior and conformance. The example is illustrative.

Do not copy the attached reference files into the target repository.

If a reference is missing, unreadable, or from a different revision, stop and
report that the migration cannot be verified.

## Working style

Perform the migration. Do not narrate routine repository inspection.

Keep generated documents and the migration report concise. Do not create prose
only to make the harness appear complete.

## Inspect the target repository

Inspect only sources needed to preserve authoritative instructions and derive
routing, including:

- existing agent instructions;
- directory and module boundaries;
- architecture and design documentation;
- build, test, lint, and validation scripts;
- project manifests and CI workflows;
- roadmap or product constraints only when they contain active rules.

Do not turn examples, future plans, or aspirational designs into current rules.

## Objectives

1. Preserve meaningful rules and their original authority.
2. Replace the monolithic instruction file with a small supported entry point.
3. Move detailed knowledge into a small set of repository-appropriate documents.
4. Create `.harness/harness.yaml` according to draft `0.2`.
5. Prefer reusable path scopes over repeated path lists.
6. Use concerns only when path scopes are insufficient.
7. Select the smallest required context set for each route.
8. Make additional context conditional on concrete evidence.
9. Move repeated validation selection into `validation_rules`.
10. Register reproducible commands and availability requirements when justified.
11. Simulate representative tasks and simplify the result.
12. Produce a concise migration and routing audit report.

Do not invent commands, paths, tools, architecture rules, concerns, or project
requirements.

## Target output

Create only artifacts justified by the repository:

```text
AGENTS.md or another supported entry point

.harness/
├── harness.yaml
├── a small set of repository-specific knowledge documents
└── scripts only when justified
```

Also create:

```text
REPOSITORY_HARNESS_MIGRATION_REPORT.md
```

The report is temporary and must not be registered in the manifest.

Do not create empty documents. Do not create one document for every section of
the original instruction file.

## Manifest budget

Generate the smallest manifest that can route representative tasks.

The root `.harness/harness.yaml` must:

- target no more than 200 non-blank, non-comment lines;
- remain below 250 non-blank, non-comment lines;
- target no more than 12 KiB and remain below 16 KiB;
- begin with no more than six routes;
- begin with no more than eight concerns;
- omit empty arrays and empty objects;
- omit `mutates: false` and `requires_approval: false`;
- omit prose that only restates selectors;
- contain no static conditional `reason` fields;
- contain no implementation guidance that belongs in Markdown;
- use scopes when a path group appears more than once;
- avoid routes with identical effective context and validation;
- avoid routes that only load the file already being edited;
- avoid one route per document, directory, task noun, or roadmap file.

These budgets are not an invitation to compress YAML unnaturally. Simplify the
model instead.

A route should require at most two documents. When more are necessary, explain
the repository-specific reason in the migration report, not in repetitive
manifest prose.

## Routing requirements

The routing vocabulary belongs to the target repository.

Start with path scopes. Add concerns only when task intent materially changes
routing and path evidence cannot express that distinction.

Do not create universal `feature`, `bugfix`, `implementation`, `refactoring`,
or `validation` routes unless they select materially different outcomes.

Do not use every file of a programming language as an architecture trigger.

Architecture guidance should be triggered only by concrete boundary indicators,
such as:

- project or package dependency files;
- composition roots;
- public cross-layer contracts;
- responsibility moving between layers;
- repository-defined architectural boundary paths.

Generic workflow guidance must not be loaded for every code change merely
because workflow guidance exists.

Order routes from narrowest to broadest. Use `routing.on_no_match: report` or
`ask` instead of a catch-all route that loads all documents.

## Validation requirements

Prefer existing project commands. Create wrappers only when they improve
reproducibility, portability, or failure propagation.

Use top-level `validation_rules` when the same command set applies to multiple
routes based on changed paths.

Commands must propagate non-zero exit status.

Declare availability requirements when missing tools or platforms are known.
Do not improvise unregistered replacements unless repository instructions
authorize them.

Separate automated validation from manual verification.

## Entry point

The supported root entry point must instruct the agent to:

1. read `.harness/harness.yaml`;
2. perform shallow discovery;
3. select the first matching route;
4. load required context only;
5. load conditional context only after a trigger matches;
6. apply matching validation rules;
7. check command availability;
8. report concise routing and validation evidence.

Keep the entry point concise.

## Representative-task simulation

Before accepting the harness, simulate at least three materially different
repository tasks.

For each simulation record only:

- task summary;
- candidate path and concern evidence;
- selected route;
- required context;
- triggered context;
- selected validation.

At least one simulation must be narrow enough that architecture and generic
workflow guidance are not automatically loaded when the repository supports
such a task.

Revise the manifest when:

- unrelated documents would load;
- a document is referenced by more than 60 percent of routes;
- a route requires more than two documents without clear need;
- two routes produce the same outcome;
- a path group is repeated instead of becoming a scope;
- a broad concern is the only selector;
- route order chooses a broader route first;
- the manifest exceeds the target budgets.

Before completion, calculate:

- non-blank, non-comment line count;
- UTF-8 byte size;
- document, scope, concern, route, command, and validation-rule counts;
- percentage of routes referencing each document.

Continue simplifying until the budgets pass or report the precise blocker.

## Verification

After migration:

1. compare the original instructions with the new harness;
2. confirm every substantive rule has a destination or reported exception;
3. validate `harness.yaml` against the draft `0.2` schema;
4. verify identifiers, references, and paths;
5. execute safe availability checks;
6. execute safe selected validation when possible;
7. record unavailable or unexecuted commands;
8. confirm the task simulations use selective context.

Do not claim conformance unless schema and cross-reference validation succeed.
Do not claim validation succeeded when a selected command failed, was
unavailable, or was not run.

## Migration report

Create `REPOSITORY_HARNESS_MIGRATION_REPORT.md`, normally under 80 lines:

```markdown
# Repository Harness Migration Report

Status: Ready for review | Needs decisions | Validation failed

## Summary

Brief migration summary.

## Changes

- Files created:
- Files modified:

## Exceptions requiring review

List only removed, changed, merged, contradicted, unresolved, or unverifiable
instructions. Write `None` when there are none.

## Manifest audit

- Non-blank, non-comment lines:
- UTF-8 size:
- Documents:
- Scopes:
- Concerns:
- Routes:
- Commands:
- Validation rules:

## Routing audit

| Example task | Evidence | Route | Required context | Triggered context | Validation |
| --- | --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... | ... |

## Validation

| Check | Result | Notes |
| --- | --- | --- |
| Draft 0.2 schema | Passed/Failed/Not run | |
| Registered references | Passed/Failed/Not run | |
| Command availability | Passed/Failed/Partial/Not run | |
| Repository validation | Passed/Failed/Partial/Not run | |

## Next actions

Only remaining human decisions, environment repairs, or manual checks.
```

Do not include every file inspected, routine commands, repeated explanations,
or successful details that require no human decision.
