# Changelog

All notable changes to the Repository Harness Specification are documented here.

## Unreleased

### Added

- Draft `0.2` repository-defined concerns and path-aware ordered routes.
- Required and conditional context with concrete selectors and reasons.
- Environment-aware command metadata.
- Mandatory routing and validation evidence reporting.
- Versioned specification, schema, and minimal-example snapshots.
- RFC 0001 describing the draft `0.2` routing proposal and benchmark plan.
- Real YAML and cross-reference validation for repository examples.
- Migration-prompt route simulations.

### Changed

- All manifest paths are now unambiguously relative to the repository root.
- The current specification, schema alias, example, prompts, terminology, design principles, roadmap, and documentation target draft `0.2`.
- Document-level `load_when` and `required` fields were replaced by route-owned context selection.
- Route `load` and `validate` arrays were replaced by structured context and validation objects.

### Preserved

- Draft `0.1` remains available under versioned specification, schema, and example paths.

## Draft 0.1

### Added

- Initial draft specification.
- Initial JSON Schema for `harness.yaml`.
- Minimal example harness.
- RFC process and contribution guidelines.
