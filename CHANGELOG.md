# Changelog

## v2.3.4 - 2026-06-18

### Changed

- Hardened the skeuomorphic skill execution contract so agents must inspect relevant examples and references before generating UI.
- Added mandatory planning, evidence, and routing requirements for high-fidelity skeuomorphic component work.
- Updated skill integrity checks to validate the nested runtime skill path.

## v2.3.3 - 2026-05-13

### Security

- Hardened GitHub Actions workflows by disabling persisted checkout credentials where repository write access is not needed.
- Reduced the fuzzing workflow top-level token permissions from broad read access to explicit per-job permissions.

### Changed

- Added CI job timeouts and concurrency cancellation to quality workflows to avoid stale or unbounded runs.
- Made ClusterFuzzLite use pull-request `code-change` mode and scheduled `batch` mode for the matching trigger context.

## v2.3.2 - 2026-05-13

### Changed

- Bumped `actions/checkout` from 4.3.1 to 6.0.2 for GitHub Actions workflow hardening.
- Bumped `actions/setup-node` from 4.4.0 to 6.4.0 for GitHub Actions workflow hardening.
- Bumped `actions/dependency-review-action` from 4.9.0 to 5.0.0 for dependency scanning maintenance.
- Bumped `actions/setup-python` from 5.6.0 to 6.2.0 for GitHub Actions workflow hardening.
