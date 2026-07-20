# Repository Harness Specification

## Status

Draft `0.2`.

This draft remains experimental and may be revised until a release tag freezes it.
Tagged or released snapshots are immutable. Files on the development branch may
change while the draft is being benchmarked.

Draft `0.2` incorporates findings from the first monolithic-versus-modular
benchmark and from the first real `0.2` migration. The first `0.2` migration
showed that selective fields alone are insufficient when the manifest itself
becomes a large repository handbook. This revision adds reusable scopes,
manifest size budgets, optional concerns, compact route objects, and
path-based validation rules.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY**
describe requirement levels in this specification.

## 1. Purpose

A Repository Harness is a versioned, repository-owned contract that helps
coding agents and humans discover:

- the smallest justified set of project knowledge for a task;
- reproducible operational commands;
- repository-defined task routes;
- validation requirements;
- completion evidence;
- optional repository-defined extensions.

The specification defines routing mechanics. Each repository defines its own
documents, scopes, concerns, commands, and routes.

## 2. Versioning

A conforming manifest MUST declare:

```yaml
spec: repository-harness/0.2
```

The current development aliases are:

```text
SPECIFICATION.md
schema/harness.schema.json
examples/minimal
```

Versioned development files live under:

```text
versions/0.2/
schema/0.2/
examples/0.2/
```

A draft snapshot becomes immutable only after it is frozen by a release or tag.
A `0.1` manifest does not conform to `0.2` without migration.

## 3. Discovery

A conforming repository MUST contain a root-level `AGENTS.md` or another entry
point supported by the active coding agent.

The entry point MUST direct the agent to `.harness/harness.yaml` and MUST
instruct it to apply the routing protocol before loading detailed repository
documents.

Example:

```markdown
# Agent Instructions

This repository uses Repository Harness Specification draft `0.2`.

Before changing files:

1. Read `.harness/harness.yaml`.
2. Perform shallow discovery to identify likely paths.
3. Select the first matching route.
4. Load only required documents.
5. Load conditional documents only after a trigger matches.
6. Apply matching validation rules to changed paths.
7. Report route, loaded documents, trigger evidence, and validation results.
```

Coding agents are not expected to understand `.harness` without instructions
from a supported entry point.

## 4. Repository-relative paths

Every path registered by the manifest MUST be relative to the repository root.

A registered path MUST:

- use `/` as the separator;
- not begin with `/`;
- not contain a Windows drive prefix;
- not contain `..` path traversal segments.

Documents may live under `.harness/` or may reference authoritative repository
documents elsewhere.

## 5. Manifest role and size

The root manifest is a routing index. It is not a repository knowledge document.

Implementation rules, architectural explanations, workflows, and validation
instructions that are useful to humans belong in registered documents or
executable scripts, not in long manifest descriptions.

A manifest:

- MUST omit empty arrays and empty objects;
- MUST omit optional fields whose value only repeats a schema default;
- MUST NOT include prose that merely restates a machine-readable selector;
- MUST NOT create a route only to tell the agent to read the file already being
  edited;
- MUST NOT duplicate the same path group in multiple selectors when a reusable
  scope can express it;
- SHOULD remain at or below 200 non-blank, non-comment lines;
- SHOULD remain at or below 12 KiB encoded as UTF-8;
- MUST remain below 250 non-blank, non-comment lines;
- MUST remain below 16 KiB encoded as UTF-8.

A validator MUST warn above the recommended budgets and MUST fail above the hard
budgets.

A repository SHOULD begin with no more than six routes and eight concerns.
Additional entries require evidence that they select materially different
context or validation.

## 6. Manifest fields

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
- registered commands;
- ordered routes.

The manifest MAY declare:

- reusable path scopes;
- repository-defined concerns;
- path-aware validation rules;
- namespaced extensions.

The manifest MUST validate against the draft `0.2` JSON Schema.

## 7. Documents

A document registration identifies repository knowledge. It does not decide
when that knowledge is loaded.

Each registered document MUST contain:

- a stable identifier;
- a repository-relative path;
- a short purpose.

A purpose SHOULD be one concise sentence.

A small repository MAY combine multiple knowledge areas in one document. A
larger repository MAY split them. The specification does not mandate filenames
or capability names.

## 8. Scopes

A scope is a reusable repository-defined group of path patterns.

Each scope MUST contain:

- a stable identifier;
- one or more repository-relative path patterns.

A scope MAY include a short description.

Repositories SHOULD define a scope when the same path group would otherwise
appear in more than one selector.

Examples are repository-specific:

```yaml
scopes:
  - id: engine-neutral
    paths:
      - src/**
      - tests/**

  - id: composition
    paths:
      - src/**/Composition/**
      - "**/*.csproj"
```

Scope identifiers are not standardized by this specification.

## 9. Concerns

A concern is an optional repository-defined classification signal used when
task intent materially changes routing and path evidence alone is insufficient.

Each concern MUST contain:

- a stable identifier;
- a short description.

A concern MAY include up to three concise `signals`.

Concerns SHOULD NOT repeat path scopes in prose. Broad labels such as `feature`,
`implementation`, `change`, or `validation` SHOULD NOT be used unless they
select a meaningfully distinct context or validation set.

A repository that can route safely using scopes alone SHOULD omit `concerns`.

## 10. Routing protocol

Before loading registered documents, an agent applying this specification MUST:

1. read only the supported entry point and `.harness/harness.yaml`;
2. infer active concerns from the user request when concerns exist;
3. perform shallow discovery only to identify candidate paths;
4. evaluate routes in manifest order;
5. select the first matching route;
6. load only that route's required context;
7. load conditional context only when its selector matches concrete evidence;
8. re-evaluate routing when candidate or changed paths materially change;
9. combine route validation with matching validation rules;
10. check command availability before execution;
11. report routing and validation evidence before reporting completion.

Shallow discovery means locating likely files, directories, project manifests,
or symbols without loading unrelated registered guidance.

An agent MUST NOT open a registered document merely because it might be useful.

If no route matches, the agent MUST follow `routing.on_no_match` and MUST NOT
load all registered documents as a fallback.

## 11. Selector matching

Draft `0.2` uses ordered `first-match` route selection.

A selector MAY contain:

- concern groups;
- direct path-pattern groups;
- reusable scope groups.

Within a selector:

- `any` matches when at least one listed item matches;
- `all` matches when every listed item matches;
- when multiple selector kinds are present, each kind must match;
- path and scope patterns are evaluated against candidate paths before changes
  and changed paths after changes.

For `scopes.any`, at least one referenced scope must match at least one path.
For `scopes.all`, every referenced scope must match at least one path.

Repositories SHOULD order narrow routes before broad routes.

An agent that changes routes MUST report the transition and retain validation
obligations already created by work performed under the earlier route.

## 12. Required and conditional context

A route MAY define `context.required` and `context.conditional`.

Required documents MUST be loaded immediately after route selection.

A conditional document entry MUST declare:

- a document identifier;
- a trigger selector under `when`.

A conditional document MUST NOT be loaded before its trigger matches. When it
matches, the agent MUST report the matching concern, scope, or path evidence.

Static `reason` text is not part of draft `0.2`. Runtime trigger evidence is the
authoritative reason.

A route SHOULD require no more than two documents. A validator SHOULD warn when
a route requires more.

A registered document referenced by more than 60 percent of routes SHOULD be
reviewed for over-broad routing or truly universal guidance.

## 13. Commands and availability

A command registration MUST contain:

- a stable identifier;
- an executable command;
- a short description.

Commands run from the repository root unless `working_directory` is declared.

Operational behavior SHOULD live in scripts or task runners. Commands SHOULD be
safe to run repeatedly where practical and MUST propagate non-zero exit status
on failure.

A command MAY declare availability requirements:

- executable names;
- supported platforms;
- required environment variables;
- behavior when requirements are unavailable.

An agent MUST check declared availability before execution.

When `on_unavailable` is `report`, the agent MUST report the command as
unavailable and MUST NOT claim it succeeded.

When `on_unavailable` is `fail`, missing availability is a validation failure.

An agent MUST NOT improvise an unregistered replacement command merely because
a command is unavailable unless repository or user instructions authorize it.

## 14. Validation

Validation may be selected in two ways:

1. route-specific validation under `route.validation`;
2. reusable path-aware rules under top-level `validation_rules`.

A validation rule declares:

- a selector;
- one or more command identifiers.

Before reporting completion, the agent MUST combine unique commands selected by
the active route and every validation rule matching candidate or changed paths.

This allows repositories to avoid repeating the same build and test commands in
many routes.

A route or validation rule MAY use conditional commands with the same selector
semantics as conditional context.

An agent MUST report every selected command as:

- passed;
- failed;
- unavailable;
- not run, with a reason.

An agent MUST NOT claim successful validation when a selected required command
failed, was unavailable, or was not run.

Manual verification MUST be reported separately from automated command success.

## 15. Routing report

Before reporting completion, an agent applying draft `0.2` MUST report
concisely:

- active concerns, when used;
- selected route;
- candidate or changed path evidence;
- required documents loaded;
- conditional documents loaded and trigger evidence;
- validation commands selected;
- command availability and results;
- route transitions, when any.

The report SHOULD contain only evidence needed to understand context selection
and validation. It SHOULD NOT narrate routine repository exploration.

## 16. Definition of Ready and Definition of Done

Teams MAY encode Definition of Ready and Definition of Done knowledge as
registered documents and route them only where relevant.

A Definition of Done MAY define required tests, reviews, documentation updates,
validations, and manual checks. It MUST NOT be treated as satisfied when required
validation evidence is missing.

## 17. Precedence

A Repository Harness MUST NOT claim precedence over system-level,
platform-level, organization-level, or explicit user instructions enforced by
the active coding agent.

Inside repository-owned guidance, a more specific route or directory rule MAY
refine broader rules but MUST NOT silently contradict repository-wide
constraints.

## 18. Security

A harness MUST NOT contain secrets, credentials, private keys, or production
tokens.

Commands that are destructive, privileged, expensive, mutating, or capable of
affecting external systems MUST be clearly identified.

Commands requiring approval MUST NOT run without approval from the active agent
runtime or user.

Availability checks SHOULD be read-only.

## 19. Extensions

Repositories MAY define namespaced extensions.

Extensions MUST NOT change the meaning of normative core fields.

Large-repository route catalogs are not standardized in this draft. A project
that experiments with external route sources MUST use a namespaced extension
and MUST document how an agent avoids loading every source.

## 20. Conformance

A repository conforms to draft `0.2` when:

1. it has a supported root entry point;
2. the entry point points to `.harness/harness.yaml`;
3. the manifest declares `repository-harness/0.2`;
4. the manifest validates against the draft `0.2` schema;
5. registered paths are repository-relative and valid;
6. registered document paths exist;
7. identifiers are unique within their collections;
8. selector and route references resolve;
9. every route has a selector and context or validation;
10. at least one command is used by route validation or a validation rule;
11. executable repository-relative command paths exist;
12. the entry point requires routing and evidence reporting;
13. the manifest remains below the hard line and byte budgets.

Conformance does not imply that route design is optimal. Validators SHOULD warn
when routes duplicate outcomes, repeat path groups, load most documents, rely
only on broad concerns, or exceed recommended budgets.

## 21. Migration from draft 0.1 or earlier draft 0.2 manifests

A migration SHOULD:

1. use repository-root-relative paths;
2. remove document-level `load_when` and `required`;
3. replace repeated path lists with scopes;
4. omit concerns when scopes are sufficient;
5. remove static conditional `reason` text;
6. omit empty collections and schema-default values;
7. make route context and validation sections optional when unused;
8. move repeated validation into `validation_rules`;
9. keep each route's required context minimal;
10. update the entry point with the routing protocol;
11. simulate representative tasks;
12. reduce the root manifest to the recommended budget before acceptance.
