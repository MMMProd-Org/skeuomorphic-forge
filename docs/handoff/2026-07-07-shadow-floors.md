# HANDOFF — skeuomorphic-forge shadow-floor fixes (zero-context resume)

**Date:** 2026-07-07
**Branch:** `fix/rim-floor-visibility` (2 commits above `main`, working tree clean)
**Commits:** `fa06344` (rim §16.2) · `7b2841a` (screws §16.5 + generalized checker)
**Role for whoever continues:** senior dev / lead architect. No omission, no regression.

---

## 0. TL;DR — where we are RIGHT NOW

The skeuomorphic-forge skill produced flat/"unfinished" UI. After 5 failed audits, we
found the real cause by **measuring before/after with sub-agents**, not by adding rules:
the skill had **exactly 2 numeric contradictions** where the golden examples / SKILL.md
stated a value *below* the `§16` benchmark floor, so agents copied the low value.

Both are now **fixed AND locked by a CI checker**:
- **§16.2 rim light** (recess top lip): SKILL said "max 0.25" (a ceiling, no floor); §16.2 = ">=0.20". → fixed.
- **§16.5 screw layers**: golden said "5 layers"; §16.5 = ">=7". → fixed.

We then **generalized**: tested 3 more floors — all **hold already** (no patch): §16.3 text,
§16.15 light-bars (focus + incident). Conclusion: the skill was NOT globally broken; it had
2 point contradictions, now closed.

**Immediate state: waiting for the user's GO to open the PR** for `fix/rim-floor-visibility`.
Nothing is pushed. CI reproduced locally is green.

---

## 1. GOALS TRACKER (passive / active / future)

### PASSIVE (done, verified, committed)
- [x] Diagnose why LLMs produce flat skeuomorphic UI (root cause, not symptom).
- [x] Prove the cause by measurement (9-run, 3-arm eval), not by adding rules.
- [x] Fix §16.2 rim floor at the point of use + in the golden stacks. (commit `fa06344`)
- [x] Build a non-regression CI checker (`scripts/check_shadow_floors.py`). (commit `fa06344`, generalized in `7b2841a`)
- [x] Fix §16.5 screw floor (5→7 layers), sync the 3 coupled spots + CI heading. (commit `7b2841a`)
- [x] Generalize the pattern: measure §16.3 text (holds 4/4), §16.15 light-bars focus (3/3) + incident (4/4). No patch needed.
- [x] Generalize §16.13 (no border on display wells) + §16.7 (2 screen overlays) — measured arm B 4/4
      (natural CRT-in-metal request, no cue). BOTH HOLD, no patch. Work done on branch
      `continue/shadow-floors` (off `fix/rim-floor-visibility`). See §5 for the numbers.
- [x] Keep the eval harness as the non-regression method (the thing 5 audits lacked).

### ACTIVE (now — the decision point)
- [ ] **User GO to open the PR** for `fix/rim-floor-visibility` (2 commits). Reco = open it.
      Do NOT push / open PR without explicit user GO.

### FUTURE (options, in ROI order — all optional, low priority)
- [ ] (if user says continue) Measure §16.13 (no border on display wells) and §16.7 (2 mandatory
      overlays) — qualitative floors; predicted to hold (rule already at point of use). Use the
      "judge on the code" protocol (see §5), not a grep checker.
- [ ] (highest value if reachable) Test against a REAL user output, not proxies. Everything so far
      is measured on sub-agent proxies (they converge with the user's own §16 benchmark, but are
      still proxies).
- [ ] (nice-to-have) Extend `check_shadow_floors.py` beyond `00-golden-examples.md §1` to the other
      recess copy-sources (`references/14`, assets HTML) — LOW ROI: the 9 evals always copied stacks
      from `00-golden`, never from an asset.

---

## 2. THE PROJECT (context for zero-context resume)

- Repo = a Claude Code **plugin** exposing ONE skill: `skeuomorphic-forge` (physically-realistic
  skeuomorphic UI in React + Tailwind + inline styles). Published, versioned (`plugin.json` v2.3.4),
  MIT, `marketplace.json`. **Target surface: everywhere incl. web/claude.ai without a shell** — so
  the runtime forcing mechanism must be textual/structural, NOT shell-dependent. (A CI checker is
  fine as a repo guard; it is not a runtime mechanism.)
- Skill anatomy: `skills/skeuomorphic-forge/SKILL.md` (the always-loaded body), `references/00..18`
  (19 files, `00-golden-examples.md` is the canonical copy-source), `assets/*.html` (21 golden
  components), `scripts/search.py` (BM25 search over refs+assets), `scripts/check_shadow_floors.py`
  (the new non-regression guard), `.github/workflows/skill-integrity.yml` (CI).
- **`references/16-benchmark-lessons.md` (§16.x) is the source of truth**: its header says it
  OVERRIDES SKILL.md on conflict. It encodes 7-10 iterations of the user's own visual feedback.
  Contradictions were resolved in favor of §16.

---

## 3. ROOT CAUSE (proven) + the mechanism

**The flat/"unfinished" look = a few numeric FINISHING floors sitting below their §16 value in the
copy-sources, so the model copies the low value.** It is NOT "the model skips the workflow" and NOT
"the resources are poor" — on rich tasks the model DOES read the resources and produces deep stacks.

Diagnostic method (repeatable — this is the deliverable that breaks the 5-audit loop):
- Spawn N sub-agents with the skill active + a natural request; each returns the component + a
  machine-readable `METRICS` line (resources opened, layer counts, the exact rim/opacity values,
  and the exact code line producing them so values are code-verifiable, not just self-reported).
- 3 arms: **A** = no-skill control (turned out contaminated — agents found the skill via cwd, so A is
  not a clean baseline; note this), **B** = skill active (natural behavior + variance), **C** = value
  forced in the prompt (upper bound).
- The FIX is proven only when arm **B re-run AFTER the patch, with NO floor mentioned in the prompt**,
  now meets the floor. (Arm C alone is near-tautological — don't trust it as proof.)

Triage rule discovered: a floor is broken **only if there is a CONTRADICTION or ABSENCE at the point
of use** (golden/SKILL states a value below §16). If SKILL already carries the floor at the point of
use (e.g. U6 for text), it holds. Numeric floors → grep checker possible. Qualitative rules
(§16.15/§16.13/§16.7) → judge the code, no grep.

---

## 4. WHAT WAS DELIVERED (files + commits)

### commit `fa06344` — rim §16.2
- `references/00-golden-examples.md`: added the top-rim layer `inset 0 1px 0 rgba(255,250,240,0.22)`
  to the "display well" stack (label 9→10 layers); raised the Ultra CRT external lip `0.05 → 0.22`.
- `skills/skeuomorphic-forge/SKILL.md`: "rim max 0.25" → **"floor 0.20 non-negotiable"** (Rim Light
  section); Éclairage table gained a distinct "recess RIM 0.20-0.25 vs flat-surface edge catch
  0.03-0.08" row; **Metal Recesses** section states the floor at the point of use.
- `scripts/check_rim_floors.py` (new): non-regression guard + `--selftest`.
- `.github/workflows/skill-integrity.yml`: CI step running the guard.

### commit `7b2841a` — screws §16.5 + generalize the guard
- `references/00-golden-examples.md`: `## 4. SCREW HEAD (5 layers…)` → `(7 layers…)`; added 2 shadow
  layers (far cast + ambient) to the screw stack.
- `skills/skeuomorphic-forge/SKILL.md`: aligned the 3 "5 couches" mentions (U4, patterns table incl.
  the cited golden heading, anti-pattern) → "7 couches".
- `.github/workflows/skill-integrity.yml`: synced the exact-line SCREW HEAD heading in the validated
  list; CI step now runs the renamed guard.
- **renamed** `scripts/check_rim_floors.py` → `scripts/check_shadow_floors.py`, generalized to guard
  BOTH the §16.2 rim floor (recess/well stacks) AND the §16.5 screw floor (>=7 layers). `--selftest`
  covers both.

⚠️ **CI coupling to remember**: `skill-integrity.yml` validates that specific `## N.` headings in
`00-golden-examples.md` exist as EXACT lines, AND that certain contract texts exist in SKILL.md
(`## CONTRAT D'EXECUTION OBLIGATOIRE`, `### Bloc FORGE PLAN`, `## ROUTAGE OBLIGATOIRE PAR BESOIN`,
`sources consultees`, `commandes \`python3 scripts/search.py ...\` exactes`). If you rename a golden
heading, update BOTH the golden file AND the CI list AND the SKILL.md citation together.

---

## 5. PROOF (numbers)

| Floor | Contradiction? | Measurement | Verdict |
|---|---|---|---|
| §16.2 rim | YES (SKILL "max 0.25" vs >=0.20) | pre-patch rim 0.06-0.14 (0/6, arms A+B); post-patch arm B **0.22 (3/3, no floor cue)** | fixed+locked |
| §16.5 screw | YES (golden 5 vs >=7) | ~15 prior eval components had 5-layer screws | fixed+locked |
| §16.3 text | no (U6 already aligned >=0.85/0.5/0.35) | 4/4 conforme (0.9 / 0.55-0.6 / 0.40-0.42) | holds, no patch |
| §16.15 light-bar focus | no | 3/3 (agents read §16.15 -> build a real slit) | holds, no patch |
| §16.15 light-bar incident | no | 4/4 (premium prompt, no light requested -> still sourced) | holds, no patch |
| §16.7 screen overlays | no (rule lives in §16, agents read it) | 4/4 (glass reflection 125deg + phosphor emission; agent-1 exact 270deg content-depth + 125deg reflection opposed) | holds, no patch |
| §16.13 no border on well | no VISUAL failure (literal divergence only) | 4/4 wells read as recessed (13-34 inset, rim 0.22). All 4 put a DARK `border` (rgba(0,0,0,.9)/#010101/#050403) = occlusion line, NEVER the light border that makes glass "stick out". Not a RED. | holds, no patch |

Eval verification commands (all pass locally):
```
cd <worktree>
ruff check scripts/ && ruff format --check scripts/check_shadow_floors.py
python3 scripts/check_shadow_floors.py --selftest
python3 scripts/check_shadow_floors.py            # -> "OK: 3 golden stacks all meet their shadow floor"
npx --no-install prettier --check ".github/workflows/skill-integrity.yml"
python3 scripts/search.py "screw" -n 1 | grep -i "sections scanned"   # -> 1699 sections / 40 files
wc -c < skills/skeuomorphic-forge/SKILL.md   # -> 29021 (< 40960 cap)
```

---

## 6. DECISIONS & RATIONALE (do NOT re-litigate)

- **Don't add more rules.** 5 audits added rules and failed. The fix is aligning contradicted numeric
  floors at the point of use + a checker. Confirmed by measurement.
- **§16 overrides SKILL.md** (repo rule) -> contradictions resolved toward §16 (rim 0.20, screw 7).
- **Measure before patching.** Every patch was preceded by a RED (reproduced failure). §16.3 and
  §16.15 were measured and found to HOLD -> deliberately NOT patched (no invented fix).
- **Surface = everywhere (incl. web, no shell).** The runtime lever is textual/structural; the CI
  checker is a repo guard only.
- **Scope was closed on evidence:** 5 floors examined, only the 2 with contradictions were broken.

---

## 7. CAVEATS / LIMITS (integrity — keep these visible)

- All measured on **sub-agent proxies**, never a real user output. They converge with the user's own
  §16 (7 feedback iterations) but remain proxies. A real user artifact would strengthen everything.
- Metrics are self-reported by agents BUT each cites the exact code line -> code-verifiable.
- ~3 agent glitches over ~25 launches (0 tool calls, garbage preamble) were discarded.
- Arm A (no-skill control) was contaminated (agents found the skill via cwd) -> no clean baseline.
- §16.13 (border-on-well) and §16.7 (overlays) now MEASURED (arm B, 4/4, no cue, natural CRT-in-metal
  request) -> both HOLD, no patch (see §5). Nuance to keep visible: all 4 agents put a DARK `border:` on
  the recess (literal divergence from §16.13 `border:none`), but it reads as an occlusion line, never the
  "glass sticks out" failure a LIGHT border causes -> deliberately NOT patched (would be an invented fix
  for a non-problem). §16.7 held richly (4-6 overlays each); agent-1 implemented the 270deg+125deg pair
  verbatim. These stay qualitative -> judged on the code, no grep checker added.
- Optional diagnostic script `hd_audit.py` (audits the 21 assets vs floors) lives in the session
  scratchpad, NOT in the repo. Not needed to continue; the repo guard is `check_shadow_floors.py`.

---

## 8. HOW TO RESUME — WORKTREE DISCIPLINE (critical)

Other LLMs work in other worktrees. **Do NOT work in the main repo checkout and do NOT reuse another
LLM's worktree. Create your OWN isolated worktree. Verify PWD after every cd.**

Main repo (source of truth, currently on `fix/rim-floor-visibility`; leave it alone):
`/home/mmmpr/src/skeuomorphic-forge`

Create a dedicated worktree on a NEW branch off `fix/rim-floor-visibility` (a worktree cannot check
out a branch already checked out in the main repo, so use `-b`):
```
git -C /home/mmmpr/src/skeuomorphic-forge worktree list          # see what's taken; avoid all of them
NEWDIR=/home/mmmpr/src/skeuomorphic-forge.wt/shadow-floors-cont   # pick a path that does NOT exist yet
git -C /home/mmmpr/src/skeuomorphic-forge worktree add -b continue/shadow-floors "$NEWDIR" fix/rim-floor-visibility
cd "$NEWDIR" && pwd    # CONFIRM you are in the new worktree, not a sibling worktree
```
This new worktree inherits both fix commits + this handoff doc. Run the §5 verification commands to
confirm green before doing anything.

If the task is ONLY "open the PR" (no code): you can open it from the main repo state without a
worktree — `gh pr create --base main --head fix/rim-floor-visibility` — but ONLY after user GO.

---

## 9. NEXT ACTION for the continuing LLM

1. Read this file fully. Run the §5 verification commands. Confirm green.
2. Ask the user (or confirm the standing decision): **open the PR**, or **continue generalization**
   (§16.13 / §16.7), or **stop**.
3. If continuing generalization: apply the §3 method — measure a RED first (sub-agent eval, arm B,
   no floor cue), only patch if a contradiction is proven, then re-prove with arm B, then lock with
   the checker. Never patch on a hypothesis.
4. If opening the PR: this handoff commit can be dropped/kept as you prefer (`git rm` before merge if
   it should not ship). PR body should summarize §4 + §5.
