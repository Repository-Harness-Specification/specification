# Contributing

Thank you for helping develop the Repository Harness Specification.

## Small changes

Typographical fixes, clarifications, test improvements, and example corrections may be submitted directly as pull requests.

## Design changes

Changes that affect the manifest, conformance rules, terminology, precedence, routing, versioning, or extension model should begin as an RFC.

1. Copy `rfcs/0000-template.md`.
2. Choose the next available RFC number.
3. Describe the problem before proposing a solution.
4. Include alternatives, compatibility impact, and an evaluation plan.
5. Open a pull request for discussion.

## Versioning rules

- Do not modify a published versioned specification, schema, or example snapshot.
- Update root aliases only when the current draft changes.
- Add a new versioned path for incompatible schema changes.
- Keep prompts pinned to a specific draft version.

## Pull requests

A pull request should:

- explain the problem being solved;
- avoid unrelated changes;
- update examples when behavior changes;
- update the schema when manifest fields change;
- update terminology and migration prompts when needed;
- update the changelog for user-visible changes;
- pass repository validation.

## Validation

Install the development dependencies and run:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_repository.py
```

## Communication

Be direct, respectful, and evidence-oriented. Disagreement about the specification is expected. Personal attacks are not acceptable.
