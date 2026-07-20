# Repository Harness Specification

## Status

Draft `0.2`.

This version incorporates findings from the first monolithic-versus-modular benchmark. Draft `0.1` made repository knowledge modular and discoverable, but its broad `load_when` labels and route definitions did not reliably reduce context consumption. Draft `0.2` introduces repository-defined concerns, path-aware route selection, required and conditional context, environment-aware commands, and an auditable routing protocol.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** describe requirement levels in this specification.

## 1. Purpose

A Repository Harness is a versioned, repository-owned contract that helps coding agents and humans discover:

- the smallest justified set of project knowledge for a task;
- reproducible operational commands;
- validation requirements;
- repository-defined task routes;
- completion criteria;
- optional project-defined extensions.

The specification defines routing mechanics. Each repository defines its own vocabulary, concerns, paths, documents, and commands.

## 2. Versioning

A manifest conforming to this draft MUST declare:

```yaml
spec: repository-harness/0.2
```

Published versioned specification and schema files are immutable snapshots. The root `SPECIFICATION.md`, `schema/harness.schema.json`, and `examples/minimal` paths refer to the current draft.

A `0.1` manifest does not conform to `0.2` without migration.

## 3. Discovery

A conforming repository MUST contain a root-level `AGENTS.md` or another entry point supported by the active coding agent.

The entry point MUST direct the agent to `.harness/harness.yaml` and MUST instruct it to apply the routing protocol before loading detailed repository documents.

Example:

```markdown
# Agent Instructions

This repository uses Repository Harness Specification draft `0.2`.

Before changing files:

1. Read `.harness/harness.yaml`.
2. Classify the task using repository-defined concerns.
3. Perform only the shallow discovery needed to select the first matching route.
4. Load only the route's required documents.
5. Load conditional documents only after their declared trigger matches.
6. Re-evaluate routing when candidate or changed paths leave the selected scope.
7. Check command availability before validation.
8. Report the selected route, loaded documents, trigger evidence, and validation results.
```

Coding agents are not expected to understand `.harness` without instructions from a supported entry point.

## 4. Repository-relative paths

Every path registered by the manifest MUST be relative to the repository root.

A registered path MUST:

- use `/` as the separator;
- not begin with `/`;
- not contain a Windows drive prefix;
- not contain `..` path traversal segments.

Documents may live under `.harness/` or may reference authoritative repository documents elsewhere, such as `docs/architecture.md`.

This rule replaces the ambiguous draft `0.1` wording that described document paths as relative to `.harness` while migration guidance used repository-relative paths.

## 5. Manifest

A conforming repository MUST contain:

```text
.harness/harness.yaml
```

The manifest MUST declare:

- the specification version;
- repository metadata;
- the supported entry point;
- routing behavior;
- registered documents;
- repository-defined concerns;
- registered commands;
- ordered routes.

The manifest MUST validate against the draft `0.2` JSON Schema.

## 6. Documents

A document registration identifies repository knowledge. It does not decide when that knowledge is loaded.

Each registered document MUST contain:

- a stable identifier;
- a repository-relative path;
- a short purpose.

Draft `0.2` removes document-level `load_when` and `required` fields. Relevance and requirement level belong to routes because a document may be required for one route and irrelevant to another.

A small repository MAY combine multiple knowledge areas in one document. A larger repository MAY split them. The specification does not mandate filenames or capabilities.

## 7. Concerns

A concern is a repository-defined classification signal used by routes.

Each concern MUST contain:

- a stable identifier;
- a description.

A concern MAY include short `signals` that help an agent classify the task or evidence discovered during implementation.

Examples are repository-specific. A game may define `input`, `gameplay`, and `scene-lifecycle`. A service may define `api-contract`, `database`, and `observability`. These names are not standardized by this specification.

Broad labels such as `feature`, `implementation`, or `change` SHOULD NOT be the only selector for a route unless they produce a meaningfully distinct context and validation set.

## 8. Routing protocol

Before loading registered documents, an agent applying this specification MUST:

1. read only the supported entry point and `.harness/harness.yaml`;
2. infer active concerns from the user request and explicit repository-defined signals;
3. perform shallow file discovery only to identify candidate paths;
4. evaluate routes in manifest order;
5. select the first route whose declared selector matches;
6. load only that route's required context;
7. load conditional context only when its trigger matches concrete evidence;
8. re-evaluate routes when active concerns or candidate or changed paths materially change;
9. check command availability before executing route validation;
10. report routing and validation evidence before reporting completion.

Shallow discovery means locating likely files, directories, project manifests, or symbols without loading unrelated registered guidance.

An agent MUST NOT open a registered document merely because it might be useful.

If no route matches, the agent MUST follow `routing.on_no_match` and MUST NOT load all registered documents as a fallback.

## 9. Route matching

Routes are ordered. Draft `0.2` uses `first-match` selection.

A route selector MAY contain concern and path groups.

Within a selector:

- `any` matches when at least one listed item matches;
- `all` matches when every listed item matches;
- when both concern and path groups are present, both groups must match;
- path patterns are matched against candidate paths before modification and changed paths after modification.

Repositories SHOULD order narrow routes before broad routes.

An agent that changes routes after discovering new evidence MUST report the route transition. It MUST retain all validation obligations already created by work performed under the earlier route.

## 10. Required and conditional context

A route's `context.required` documents MUST be loaded immediately after route selection.

A route's `context.conditional` entries MUST declare:

- a document identifier;
- a trigger selector under `when`;
- a concise reason.

A conditional document MUST NOT be loaded before its trigger matches. When the trigger matches, the agent MUST load the document and report the matching concern or path evidence.

A repository SHOULD prefer narrow conditional triggers over adding documents to every route's required context.

## 11. Commands and availability

A command registration MUST contain:

- a stable identifier;
- an executable command;
- a short description.

Commands run from the repository root unless `working_directory` is declared.

Operational behavior SHOULD live in scripts or task runners rather than duplicated prose. Commands SHOULD be safe to run repeatedly where practical and MUST propagate non-zero exit status on failure.

A command MAY declare availability requirements:

- required executable names;
- supported platforms;
- required environment variables;
- behavior when requirements are unavailable.

An agent MUST check declared availability before execution.

When `on_unavailable` is `report`, the agent MUST report the command as unavailable and MUST NOT claim that command or route validation succeeded.

When `on_unavailable` is `fail`, missing availability is a validation failure.

An agent MUST NOT improvise an unregistered replacement command merely because a registered command is unavailable, unless an explicit user instruction or repository rule authorizes it.

## 12. Validation

A route's `validation.required` commands MUST be attempted when available before the task is reported complete.

A route MAY define conditional validation commands using the same selector semantics as conditional context.

An agent MUST report each required or triggered command as one of:

- passed;
- failed;
- unavailable;
- not run, with a reason.

An agent MUST NOT claim successful validation when a required or triggered command failed, was unavailable, or was not run.

Manual verification MAY be described by repository documents, but it MUST be reported separately from automated command success.

## 13. Routing report

Before reporting completion, an agent applying draft `0.2` MUST report:

- active concerns;
- the selected route;
- candidate or changed path evidence used for selection;
- required documents loaded;
- conditional documents loaded and their trigger evidence;
- validation commands selected;
- command availability and results;
- route transitions, when any.

This report MAY be concise. Its purpose is to make context consumption and validation auditable.

## 14. Definition of Ready and Definition of Done

Teams MAY encode Definition of Ready and Definition of Done knowledge as registered documents and route them only where relevant.

A Definition of Done MAY define required tests, reviews, documentation updates, validations, and manual checks. It MUST NOT be treated as successfully satisfied when required validation evidence is missing.

## 15. Precedence

A Repository Harness MUST NOT claim precedence over system-level, platform-level, organization-level, or explicit user instructions enforced by the active coding agent.

Inside repository-owned guidance, a more specific route or directory rule MAY refine broader rules but MUST NOT silently contradict repository-wide constraints.

Repositories SHOULD document internal precedence rules when multiple sources overlap.

## 16. Security

A harness MUST NOT contain secrets, credentials, private keys, or production tokens.

Commands that are destructive, privileged, expensive, mutating, or capable of affecting external systems MUST be clearly identified.

Commands requiring approval MUST NOT run without approval from the active agent runtime or user.

Availability checks SHOULD be read-only.

## 17. Extensions

Repositories MAY define custom documents, concerns, commands, routing metadata, workflows, and integrations.

Extensions MUST use namespaced identifiers when collision is possible.

Extensions MUST NOT change the meaning of normative core fields.

## 18. Conformance

A repository conforms to draft `0.2` when:

1. it has a supported root entry point;
2. the entry point points to `.harness/harness.yaml`;
3. the manifest declares `repository-harness/0.2`;
4. the manifest validates against the draft `0.2` schema;
5. every registered document and working-directory path is repository-relative and valid;
6. registered document paths exist;
7. document, concern, command, and route identifiers are unique within their collections;
8. route references resolve to registered identifiers;
9. every route has a selector and is evaluated using manifest order;
10. the repository declares at least one command used by route validation;
11. executable repository-relative command paths exist;
12. the entry point requires routing and evidence reporting.

Conformance does not imply that route design is optimal. Validators SHOULD warn when routes load nearly all documents, duplicate another route's context and validation, or rely only on broad concern labels.

## 19. Migration from draft 0.1

A draft `0.1` harness migrating to `0.2` SHOULD:

1. change `spec` to `repository-harness/0.2`;
2. make every document path repository-root-relative;
3. remove document-level `load_when` and `required` fields;
4. define repository-specific concerns and optional classification signals;
5. add a `routing` policy;
6. replace route `load` with `context.required` and narrowly triggered `context.conditional` entries;
7. replace route `validate` with `validation.required` and optional conditional validation;
8. add command availability metadata where the environment can be checked;
9. update the entry point with the draft `0.2` routing protocol;
10. simulate representative tasks and revise routes that load unrelated context.
