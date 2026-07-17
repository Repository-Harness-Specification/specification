# Migrate monolithic agent instructions to a Repository Harness

Migrate the target repository's existing agent instructions into a Repository Harness.

## Authoritative references

Before making changes, read the official Repository Harness Specification:

- Specification:
  https://github.com/Repository-Harness-Specification/specification/blob/main/SPECIFICATION.md

- Manifest schema:
  https://raw.githubusercontent.com/Repository-Harness-Specification/specification/main/schema/harness.schema.json

- Minimal example:
  https://github.com/Repository-Harness-Specification/specification/tree/main/examples/minimal

These official resources are the source of truth.

Do not reproduce, reinterpret, or extend the manifest schema based only on this prompt.

Do not copy the specification, schema, or reference example into the target repository.

If these references cannot be accessed, stop the migration and report that specification compliance could not be verified.

## Source instructions

Inspect the target repository for relevant sources, including:

- `AGENTS.md`;
- `CLAUDE.md`;
- Copilot or Cursor instructions;
- architecture documentation;
- testing documentation;
- build and validation scripts;
- CI workflows;
- roadmap and product constraints.

## Objectives

1. Preserve all meaningful rules and their original authority.
2. Replace the monolithic instruction file with a small supported entry point.
3. Move detailed repository knowledge into `.harness/`.
4. Organize content by capability.
5. Create `.harness/harness.yaml` according to the official specification and schema.
6. Avoid inventing commands, paths, architecture rules, or project requirements.
7. Identify contradictory, obsolete, or unverifiable instructions.
8. Create reproducible validation scripts only when justified by the repository.
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

Do not force the minimal example's exact document structure onto the target repository.

Create `REPOSITORY_HARNESS_MIGRATION_REPORT.md` as a temporary review artifact.

## Migration rules

- Keep the root entry point small.
- Point the entry point to `.harness/harness.yaml`.
- Register harness documents, commands, and routes according to the official schema.
- Preserve distinctions such as must, should, may, prefer, and avoid.
- Do not convert examples or future plans into current requirements.
- Use repository-relative paths.
- Reference only files and commands that actually exist.
- Validation commands must propagate non-zero exit codes.
- Missing required builds or test suites must not be reported as success.
- Clearly separate automated validation from manual verification.
- Do not include secrets or credentials.

## Verification

After migration:

1. compare the original instructions with the new harness;
2. confirm that every substantive rule has a destination;
3. validate `harness.yaml` against the official schema;
4. verify all registered paths, document IDs, command IDs, and routes;
5. execute safe validation commands when possible;
6. record commands that were not executed;
7. report unresolved questions and manual checks.

Do not claim specification compliance unless validation against the official schema succeeds.

## Migration report

The report must include:

- source files analyzed;
- files created and modified;
- mapping from original sections to harness capabilities;
- contradictions and obsolete instructions;
- assumptions and unresolved questions;
- commands executed and their results;
- schema validation result;
- manual review still required.
