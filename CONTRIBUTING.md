# Contributing to Skeuomorphic Forge

Thanks for your interest in improving Skeuomorphic Forge! This document explains
how to propose changes and what is expected of every contribution.

## How to contribute

- **Bugs / ideas:** open a GitHub issue describing the problem or proposal.
- **Code / docs:** open a pull request against `main` from a topic branch.

```bash
git checkout -b feature/my-change
# make changes
git commit -m "Describe the change"
git push origin feature/my-change
# then open a pull request
```

## Review and merge requirements

All changes land through pull requests on `main`. The branch ruleset requires:

- at least **one approving review** from a non-author,
- **code-owner review** (see [`.github/CODEOWNERS`](.github/CODEOWNERS)),
- approval of the **most recent push**,
- all **conversation threads resolved**,
- the **`required-ci`** status check passing,
- **linear history** (squash or rebase merges only).

## Testing policy

- Automated unit tests live in `scripts/test_*.py` and run in CI via
  `python3 -m unittest discover -s scripts -p 'test_*.py'` (the **Skill
  Integrity** workflow, which provides the `required-ci` check).
- **Any major change to functionality MUST add or update automated tests** that
  cover the new or changed behaviour. Pull requests that change behaviour
  without corresponding test updates will be asked to add them before merge.
- Run the suite locally before opening a PR:

```bash
python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

## Continuous integration

Every pull request to `main` triggers:

- **Skill Integrity** — validates the `SKILL.md` contract and runs the unit
  tests (`required-ci`).
- **CodeQL** — static application security testing (SAST).
- **Dependency Review** — fails on `high`+ dependency vulnerabilities (SCA).
- **Fuzzing** — fuzz tests the search engine (`fuzz/search_fuzzer.py`).
- **OpenSSF Scorecard** — supply-chain posture scoring.

## Reporting security issues

Do not open public issues for vulnerabilities. Follow the process in
[`SECURITY.md`](SECURITY.md).
