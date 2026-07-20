# Agent Instructions

This repository uses Repository Harness Specification draft `0.2`.

Before changing files:

1. Read `.harness/harness.yaml`.
2. Classify the task using the repository-defined concerns.
3. Perform only the shallow file discovery needed to select the first matching route.
4. Load only the selected route's required documents.
5. Load conditional documents only after their declared trigger matches concrete concern or path evidence.
6. Re-evaluate routing when candidate or changed paths leave the selected route's scope.
7. Check command availability before executing validation.
8. Report active concerns, the selected route, loaded documents, trigger evidence, and validation results.

Do not load every registered document as a fallback.
Do not claim validation succeeded unless every required or triggered command completed successfully.
