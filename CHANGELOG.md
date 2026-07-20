# Changelog

All notable changes to the Repository Harness Specification are documented here.

## Unreleased

### Added

- Draft `0.2` reusable path scopes.
- Optional concerns for cases where path scopes are insufficient.
- Shared path-aware `validation_rules`.
- Recommended and hard manifest line and byte budgets.
- Validator checks for manifest size, repeated paths, duplicate route outcomes,
  unused registrations, broad routing, and overused documents.
- Migration-prompt manifest audits and strict simplification requirements.
- Environment-aware command metadata.
- Mandatory routing and validation evidence reporting.
- Versioned specification, schema, and minimal-example development snapshots.

### Changed

- Conditional document and command entries no longer contain static `reason`
  fields; runtime trigger evidence is authoritative.
- Empty context and validation arrays are no longer valid or required.
- Route context and validation blocks are optional when unused.
- Concerns are no longer required when scopes are sufficient.
- Repeated route validation may be moved to top-level `validation_rules`.
- Draft `0.2` development snapshots may evolve until frozen by a release or tag.
- All manifest paths remain relative to the repository root.
- Migration prompts now target a manifest below 200 lines and reject generated
  verbosity before human review.

### Preserved

- Draft `0.1` remains available under versioned specification, schema, and
  example paths.

## Draft 0.1

### Added

- Initial draft specification.
- Initial JSON Schema for `harness.yaml`.
- Minimal example harness.
- RFC process and contribution guidelines.
