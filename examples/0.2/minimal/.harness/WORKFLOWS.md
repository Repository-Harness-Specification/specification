# Workflows

## Source change

1. Confirm the expected behavior and acceptance criteria.
2. Identify the module that owns the change.
3. Make the smallest coherent implementation.
4. Add or update tests when the repository provides a relevant suite.
5. Run route-selected validation.
6. Report changed files, decisions, and remaining manual checks.

## Regression fix

1. Reproduce or characterize the failure.
2. Add a regression test when practical.
3. Fix the narrowest responsible behavior.
4. Run related and route-selected validation.
5. Report root cause and evidence.

## Refactoring signal

When a change moves responsibilities, changes dependency direction, or introduces a new module boundary, classify the `architecture-boundary` concern so the route can load architecture guidance.
