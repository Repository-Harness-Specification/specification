# Migrate monolithic agent instructions to a Repository Harness without internet access

Migrate the target repository's existing agent instructions into a Repository Harness.

You are operating inside the target repository without internet access.

## Required attached references

Before modifying the repository, confirm that the following files are attached to the current agent session:

```text
SPECIFICATION.md
harness.schema.json
minimal-harness.yaml
```

They must all come from the same Repository Harness Specification branch, tag, release, or commit.

Treat the attached files as the authoritative specification snapshot.

The attached JSON Schema is authoritative for the structure of `.harness/harness.yaml`.

The minimal example is illustrative. Do not force its exact document structure onto the target repository.

Do not copy the attached specification, schema, or example into the target repository.

Do not reproduce or extend the manifest format based only on this prompt.

If any required reference is missing, unreadable, or from an inconsistent version, stop and report that the migration cannot be verified.

## Inspect the target repository

Inspect relevant sources before creating files, including:

- `AGENTS.md`;
- `CLAUDE.md`;
- Copilot or Cursor instructions;
- architecture documentation;
- testing documentation;
- contributor documentation;
- build and validation scripts;
- project or dependency manifests;
- CI workflows;
- roadmap and product constraints.

Do not infer that an example, planned feature, or aspirational design already exists in the implementation.

## Objectives

1. Preserve meaningful rules and their original authority.
2. Replace the monolithic instruction file with a small supported entry point.
3. Move detailed repository knowledge into `.harness/`.
4. Organize content by capability.
5. Create `.harness/harness.yaml` according to the attached specification and schema.
6. Avoid inventing commands, paths, tools, architecture rules, or project requirements.
7. Identify contradictory, obsolete, duplicated, or unverifiable instructions.
8. Create reproducible validation scripts only when justified.
9. Produce a migration report for human review.

## Target output

Create only the artifacts required by the target repository:

```text
AGENTS.md or another supported entry point

.harness/
├── harness.yaml
├── README.md
├── capability documents
└── scripts when justified
```

Do not create empty capability documents.

Do not create every capability shown by the minimal example unless the repository justifies it.

Create:

```text
REPOSITORY_HARNESS_MIGRATION_REPORT.md
```

The migration report is a temporary review artifact and does not need to be registered in `harness.yaml`.

## Migration rules

- Keep the root entry point small.
- Point the entry point to `.harness/harness.yaml`.
- Register documents, commands, and routes according to the attached schema.
- Preserve distinctions such as must, should, may, prefer, and avoid.
- Do not convert examples into mandatory rules.
- Do not convert future plans into current implementation claims.
- Use repository-relative paths.
- Reference only files and commands that exist.
- Prefer existing project commands over unnecessary wrappers.
- Create scripts only when they improve reproducibility or portability.
- Validation commands must propagate non-zero exit codes.
- Failed builds or tests must not be reported as successful.
- Missing required test suites must not silently become warnings.
- Separate automated validation from manual verification.
- Do not include secrets, credentials, private keys, or production tokens.

## Verification

After migration:

1. compare the original instructions with the new harness;
2. confirm that every substantive rule has a destination;
3. verify that all registered documents and commands exist;
4. verify that routes reference valid document and command IDs;
5. validate `.harness/harness.yaml` against the attached schema;
6. execute safe validation commands when possible;
7. confirm that command failures produce non-zero exit codes;
8. record commands that were not executed;
9. report unresolved questions and manual checks.

Do not claim specification compliance unless schema validation succeeds against the attached schema.

Do not report repository validation as successful when a required command failed, was skipped, or could not be executed.

## Migration report

The migration report must include:

- specification snapshot or version used;
- source files analyzed;
- files created and modified;
- mapping from original sections to harness capabilities;
- duplicated rules intentionally preserved and why;
- contradictions and obsolete instructions;
- assumptions and unresolved questions;
- commands executed and their results;
- commands not executed;
- schema validation result;
- manual review still required.

Do not delete source instructions until the migration has been reviewed.
