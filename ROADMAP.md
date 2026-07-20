# Roadmap

## Phase 1: Problem definition

- [x] Publish the initial problem statement.
- [x] Define initial Repository Harness terminology.
- [x] Create the draft specification repository.

## Phase 2: Manual implementation

- [x] Migrate one real repository from a monolithic `AGENTS.md`.
- [x] Record ambiguities and missing capabilities.
- [x] Create the draft `0.1` manifest and migration prompts.

## Phase 3: First benchmark

- [x] Create a reproducible implementation task.
- [x] Compare monolithic and draft `0.1` modular context.
- [x] Measure task success, validation results, token usage, execution time, command attempts, and changed-file scope.
- [x] Identify that broad routing loaded too many documents.

## Phase 4: Draft 0.2 selective routing

- [ ] Review RFC 0001.
- [ ] Introduce repository-defined concerns and path scopes.
- [ ] Introduce required and conditional context.
- [ ] Introduce environment-aware command metadata.
- [ ] Add routing evidence to entry points and migration prompts.
- [ ] Validate generated routes using representative-task simulations.
- [ ] Repair and manually verify the WSL benchmark environment.

## Phase 5: Second benchmark

- [ ] Generate a fresh draft `0.2` harness for the same real repository.
- [ ] Re-run the original benchmark task with the same baseline and validation criteria.
- [ ] Compare monolithic, draft `0.1`, and draft `0.2` results.
- [ ] Publish loaded-document, uncached-token, execution-time, command, and success results.
- [ ] Test additional task categories after the controlled repeat.

## Phase 6: Tooling

- [ ] Build `harness-me init` only after draft `0.2` routing is manually validated.
- [ ] Build `harness-me validate`.
- [ ] Build `harness-me audit`.
- [ ] Generate entry-point adapters only after the source format stabilizes.

## Phase 7: Ecosystem

- [ ] Publish reusable Agent Skills.
- [ ] Add community-maintained examples.
- [ ] Accept third-party benchmark results.
- [ ] Evaluate a stable `1.0` specification.
