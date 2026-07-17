# Contributing

Thank you for helping develop the Repository Harness Specification.

## Small changes

Typographical fixes, clarifications, and example improvements may be submitted directly as pull requests.

## Design changes

Changes that affect the manifest, conformance rules, terminology, precedence, routing, or extension model should begin as an RFC.

1. Copy `rfcs/0000-template.md`.
2. Choose the next available RFC number.
3. Describe the problem before proposing a solution.
4. Include alternatives and compatibility impact.
5. Open a pull request for discussion.

## Pull requests

A pull request should:

- explain the problem being solved;
- avoid unrelated changes;
- update examples when behavior changes;
- update the schema when manifest fields change;
- update the changelog for user-visible changes;
- pass repository validation.

## Validation

Run:

```bash
python3 scripts/validate_repository.py
```

## Communication

Be direct, respectful, and evidence-oriented. Disagreement about the specification is expected. Personal attacks are not acceptable.
