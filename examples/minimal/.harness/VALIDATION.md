# Validation

## Required completion check

Run:

```bash
./.harness/scripts/validate.sh
```

Do not report completion unless the command exits successfully.

## Validation categories

Adapt this list to the repository:

- build or compilation;
- formatting and linting;
- static type checks;
- unit tests;
- integration tests;
- architecture checks;
- security checks;
- manual verification.

Testing may remain in this document or move to a dedicated testing capability when the repository needs more detailed guidance.

## Manual verification

List checks that cannot yet be automated. Report them explicitly when they remain incomplete.
