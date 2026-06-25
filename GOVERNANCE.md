# Project Governance

## Roles

Skeuomorphic Forge is currently maintained by a single maintainer (see
[`.github/CODEOWNERS`](.github/CODEOWNERS)). The maintainer reviews and merges
contributions, triages issues, handles security reports, and publishes releases.

## Decision making

Changes are proposed via pull requests and merged after review per the
requirements in [`CONTRIBUTING.md`](CONTRIBUTING.md). The maintainer holds final
decision authority and is responsible for the project's direction.

## Granting elevated permissions

New collaborators are **not** granted write or administrative access by default.
Before any contributor is granted escalated permissions to sensitive resources
(write access, branch-ruleset bypass, repository administration, or release
publishing rights):

- the contributor must have a track record of reviewed, accepted contributions;
- the maintainer reviews and **explicitly approves** the access grant;
- access is granted at the **least privilege** necessary for the contributor's
  role and is revoked when no longer needed.

This review of collaborators prior to permission escalation is a standing policy
for the project.

## Releases

Releases are cut from `main` as tagged versions (`vX.Y.Z`) by the maintainer,
following the support and security policies in [`SECURITY.md`](SECURITY.md).
