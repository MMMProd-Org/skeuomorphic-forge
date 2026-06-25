# Threat Model & Attack Surface

This document summarises the threat model and attack-surface analysis for
Skeuomorphic Forge. It is reviewed when significant changes are made and before
releases.

## What the project is

Skeuomorphic Forge is a **source-only Claude Code skill**: Markdown skill
definitions, HTML/CSS examples, reference guides, and small Python/Shell helper
scripts (a local search engine over the skill corpus). It ships no compiled
binaries and runs no network services.

## Assets

- Integrity of the skill content and reference examples consumed by agents.
- Integrity of the repository and its release tags.
- The CI/CD pipeline and its permissions.

## Trust boundaries

- **Contributors → repository:** mediated by pull requests, required reviews,
  code-owner approval, and CI (see [`CONTRIBUTING.md`](CONTRIBUTING.md)).
- **Dependencies → build:** third-party GitHub Actions and Python/Node
  dependencies, mediated by SHA-pinned actions and Dependency Review.
- **Repository → consumers:** users install the skill from tagged releases.

## Primary threats and mitigations

| Threat | Mitigation |
| ------ | ---------- |
| Malicious or accidental code injection via PR | Required non-author + code-owner review, last-push approval, `required-ci` (branch ruleset on `main`). |
| Compromised dependency | `dependency-review-action` (fail on `high`+), SHA-pinned actions. |
| Vulnerable code introduced | CodeQL SAST + fuzzing on every PR. |
| CI privilege abuse / token theft | Explicit least-privilege workflow permissions (`{}` or `contents: read`) with minimal per-job scopes, `persist-credentials: false`, OIDC instead of stored secrets. |
| Tampered / forced history | Force-push and deletion blocked, linear history required. |
| Supply-chain posture drift | OpenSSF Scorecard runs on push and weekly. |

## Out of scope

There is no runtime service, no user-data processing, and no authentication
surface; classic runtime threats (network attacks, data exfiltration from a
running service) do not apply to this static skill repository.

## Search helper scripts

The Python search helpers (`scripts/search.py`) operate only on local repository
files and accept no untrusted network input; they are exercised by unit tests
(`scripts/test_search.py`) and a fuzz harness (`fuzz/search_fuzzer.py`).
