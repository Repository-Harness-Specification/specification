# Agent Instructions

This repository uses Repository Harness Specification draft `0.2`.

Before changing files:

1. Read `.harness/harness.yaml`.
2. Perform only shallow discovery needed to identify candidate paths.
3. Select the first matching route.
4. Load only the route's required documents.
5. Load conditional documents only after their selector matches evidence.
6. Apply matching validation rules to candidate and changed paths.
7. Check command availability before execution.
8. Report the selected route, loaded documents, trigger evidence, and validation results.

Do not load registered documents speculatively.
Do not claim validation succeeded unless every selected command succeeded.
