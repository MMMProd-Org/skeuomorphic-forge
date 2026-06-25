# Security Policy

## Supported Versions

Security fixes are developed on the default branch (`main`) and shipped in the
next tagged release. Only the **latest released minor version** receives
security updates.

| Version              | Supported          |
| -------------------- | ------------------ |
| latest minor release | :white_check_mark: |
| older releases       | :x:                |

A release stops receiving security updates as soon as a newer minor version is
published. Users are expected to upgrade to the latest release to stay covered.

## Reporting a Vulnerability

Please report suspected vulnerabilities privately through GitHub Security Advisories:

https://github.com/MMMProd-Org/skeuomorphic-forge/security/advisories/new

If that is unavailable, contact the repository owner through GitHub and include:

- A concise description of the issue
- Steps to reproduce or validate it
- Potential impact
- Any suggested mitigation

Please do not open a public issue for unpatched vulnerabilities.

We aim to acknowledge vulnerability reports within 7 days, provide an initial
assessment within 30 days, and coordinate public disclosure after a fix or
mitigation is available.

## Secrets and Credentials

The project keeps no long-lived secrets in source control or CI:

- GitHub Actions workflows run with `persist-credentials: false` and the default
  least-privilege `GITHUB_TOKEN`, declaring explicit least-privilege permissions
  (top-level `permissions: {}` or `contents: read`, with minimal per-job scopes).
- Workflows that publish security telemetry (e.g. OpenSSF Scorecard) use
  short-lived OIDC tokens (`id-token: write`) instead of stored credentials.
- No API keys, tokens, or passwords are required to build, test, or run the
  project.

If a secret is ever required, it must be stored as an encrypted GitHub Actions
secret, never committed to the repository, and rotated immediately on suspected
exposure.

## Dependency (SCA) Remediation Policy

- Every pull request to `main` runs `actions/dependency-review-action`, which
  **fails the build on any dependency vulnerability of `high` severity or
  above**. Such pull requests cannot be merged until the finding is remediated
  (upgrade, replace, or remove the dependency).
- This `high`-and-above threshold is the project's remediation threshold for
  Software Composition Analysis (SCA) findings.
- No release is published while a known, unresolved SCA violation at or above the
  threshold is present on `main`.

## Static Analysis (SAST) Remediation Policy

- CodeQL code scanning runs on every push and pull request to `main`.
- Newly introduced code-scanning alerts of `error` / `high` severity are treated
  as release-blocking and must be fixed, or explicitly dismissed with a
  documented rationale, before the next release.

## Verifying Releases

Releases are published as git tags (`vX.Y.Z`) with GitHub-generated source
archives. To verify a release:

1. Confirm the tag exists in this repository and matches the GitHub release page.
2. Compare the downloaded archive against the commit the tag points to (the
   archive SHA is shown on the GitHub release and via the GitHub API).
3. Releases are authored only by the repository maintainer (see
   `.github/CODEOWNERS`); the tag author/committer identity is visible in git
   history and on GitHub.
