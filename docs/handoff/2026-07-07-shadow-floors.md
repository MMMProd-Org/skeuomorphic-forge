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

Then generalized §16.13/§16.7 (measured, both HOLD, no patch), validated the skill against a REAL
user artifact (a keypad — skill guides it well), enriched it with a **Thin Ledge Keypad** variant
(user-requested, re-proven), and finally **applied the §16.2 rim fix to real production code in
`Mustang_DSP`**: 88 recessed wells retrofitted (audit found ~94/96 flat), typecheck green + owner
approved the 0.22 rim visually.

**State (updated 2026-07-07): user gave GO — BOTH PRs are OPEN.** Skill PR
`MMMProd-Org/skeuomorphic-forge#27` (`continue/shadow-floors`) and production PR
`MMMProd-Org/Mustang_DSP#1718` (`fix/rim-floor-wells-16-2`, CI green). After opening, a THIRD §16.2
contradiction was found + fixed at a second copy-source (`references/14`) — proven by arm B,
re-proven, locked by the checker (commit `a286f15`, on PR #27). NOT merged — opening only.
See §1 + §5. CI/typecheck green on both.

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
- [x] Tested against a REAL user artifact (not a proxy): `Mustang_DSP` `RetainedOemZoneControl.tsx`
      (a segmented 4-state keypad the user said took ~20 iterations). Audited it + measured arm B 3/3
      on the same "segmented multi-state keypad" pattern (no cue). Skill guides it WELL — no RED, no
      patch. The user's 20 iterations were an ESTHETIC choice (thin keycap-ledge, 3 layers, dropped
      background-clip:text), not a skill defect: the skill routes to `references/11 §43 Mechanical Key`
      and every agent shipped a conformant keypad (>=9 layers, well rim 0.22, full states, zero
      clip:text) first try. See §5.
- [x] Enriched the skill with the user's own idiom (user-requested): added a "Thin Ledge Keypad"
      variant to `references/11 §43` + a routing row in SKILL.md's matrix. RED was proven first
      (3/3 arm-B agents always shipped a bombe keycap, never a ledge — the idiom was missing, not
      contradicted), re-proven after (2/2 arm-B on a compact/flat request routed to the variant and
      applied it: thin ledge, shared well, backlit-not-raised selection, zero background-clip:text,
      both cited the label-doubling trap). Qualitative -> judged on code, no grep checker. commit `a85bad1`.
- [x] Keep the eval harness as the non-regression method (the thing 5 audits lacked).
- [x] **Applied the §16.2 rim fix to REAL production code.** In `Mustang_DSP` (a separate repo where
      the user builds UIs with this skill) audited ~96 recessed wells, found ~94 broken (rim < 0.20 /
      absent / dark), fixed **88** across 3 passes (2 shared copper patterns=37 + BROKEN-absent CRT/
      gauge=32 + low-alpha individual=19), with 6 justified skips. **Type-check green** (`tsc --noEmit`
      exit 0) + **owner approved the 0.22 rim visually** (before/after render, "c parfait"). Repo
      `Mustang_DSP`, branch `fix/rim-floor-wells-16-2` (5 commits), doc `docs/RIM-FLOOR-16.2-AUDIT.md`.
      Nothing pushed. (This IS the "real user output" item that used to be in FUTURE — now done, and it
      confirmed the §16.2 diagnosis at scale: the flat-well bug was everywhere in real code.)
- [x] **Extended the §16.2 fix to `references/14` (a SECOND copy-source).** After the PRs opened,
      measured arm B (no cue) on gauge/well/trough requests: 1/4 reproduced the flat-well RED — a
      trough built from `references/14`'s rimless 4-zone model shipped only the outer 0.06 lip, no
      inset machined rim. Patched `references/14` (ZONE 0 machined rim added to the 4→5-zone anatomy
      + every §16.2-governed well example) + extended `check_shadow_floors.py` to guard it (skips the
      ASCII schematic). Re-proven arm B 3/3 (trough+channel+gauge ship inset 0.22), checker green
      (OK 8 stacks / 2 sources). commit `a286f15` on `continue/shadow-floors` (PR #27).

### ACTIVE (now)
**Both PRs are OPEN (user gave GO 2026-07-07). Nothing left blocking.**
- [x] PR #1 — skill: `MMMProd-Org/skeuomorphic-forge#27` (`continue/shadow-floors`). Now includes the
      `references/14` fix (`a286f15`). Pushing more commits to the branch auto-updates the PR.
- [x] PR #2 — production: `MMMProd-Org/Mustang_DSP#1718` (`fix/rim-floor-wells-16-2`, CI SUCCESS). A
      `style:` commit (`0c6b2e98`) prettier-cleaned 3 touched files (2 carried pre-existing debt on
      main) to pass the repo's pre-push gate. NOT merged — opening only, per the GO.

### FUTURE (options, in ROI order — all optional, low priority)
- [ ] `Mustang_DSP`: the ~6 skipped wells are correct (rimmed by another means / not wells) — nothing
      to do. A handful of the 88 could want per-context tuning if a spot ever reads too hot (0.22 is
      centralizable); owner approved as-is for now.
- [ ] (nice-to-have) Extend `check_shadow_floors.py` beyond `00-golden-examples.md §1` to the other
      recess copy-sources (`references/14`, assets HTML) — LOW ROI: the evals always copied stacks
      from `00-golden`, never from an asset.
- [ ] (nice-to-have) The skill's §16.13 qualitative floor (no light-border on wells) + §16.7 (2
      overlays) hold by measurement but have NO grep guard. Only add one if a regression ever appears.

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
| segmented keypad / multi-state button (REAL user artifact) | no (skill routes to `refs/11 §43 Mechanical Key`) | audited user's `RetainedOemZoneControl` (thin ledge, 3-layer keys — user's esthetic after ~20 iters) + arm B 3/3 on the same pattern (no cue): every agent shipped a conformant keypad (keys 9/10/14 layers >= C6's 5, recessed well rim 0.22, rest/hover/pressed/selected/focus states, label = color+text-shadow, ZERO background-clip:text) | skill guides well, no patch |

| §16.2 rim @ `references/14` (2nd copy-source) | YES (absence: rimless 4-zone model, outer 0.06 only) | pre-patch arm B 1/4 trough shipped flat top (no inset rim); post-patch arm B **3/3 inset 0.22 (no cue)**; checker locks it (OK 8/2 sources) | fixed+locked (`a286f15`) |

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

- Most measured on **sub-agent proxies**, which converge with the user's own §16 (7 feedback iterations)
  but remain proxies. UPDATE: we finally tested a REAL user artifact — `Mustang_DSP`
  `RetainedOemZoneControl.tsx` (segmented keypad, ~20 iterations). The skill guides the pattern well
  (arm B 3/3, no RED). The one real gap is DIRECTIONAL not a defect: the skill's natural output is a
  RICH bombe keycap (9-14 layers); the user's finished taste was a THIN ledge keycap (3 layers, flat
  press, no background-clip:text). RESOLVED (user asked): the ledge idiom is now a documented §43
  variant (commit `a85bad1`). This did NOT break the "no rule without a proven RED" discipline — the
  RED was measured first (3/3 always bombe = the idiom was MISSING, not contradicted) and re-proven
  after (2/2). It is coverage of a missing idiom, not a fix to a §16 contradiction.
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

State (2026-07-07): user gave GO. BOTH PRs OPEN — skill `skeuomorphic-forge#27` (now +`a286f15`
`references/14` fix) and production `Mustang_DSP#1718` (CI green, +`0c6b2e98` prettier). A third §16.2
contradiction (`references/14`, 2nd copy-source) was found→fixed→re-proven→locked after opening. NOT
merged — opening only. Nothing left blocking; remaining items are §1 FUTURE (optional).

1. Read this file fully AND `Mustang_DSP` `docs/RIM-FLOOR-16.2-AUDIT.md`. Re-run the §5 verification
   (skill) → confirm green. The Mustang_DSP branch is already typecheck-green + owner-visually-approved.
2. Do NOT push or open any PR without a fresh explicit GO. When GO comes:
   - Skill PR: `gh pr create --base main --head continue/shadow-floors` (body = summarize §4 + §5).
   - Mustang_DSP PR: FROM the Mustang_DSP worktree, `gh pr create --base main --head
     fix/rim-floor-wells-16-2` (body = summarize `docs/RIM-FLOOR-16.2-AUDIT.md`). PRODUCTION code — care.
3. If instead continuing work: keep the non-negotiable method — measure a RED first (arm B, no cue),
   patch ONLY on a proven contradiction, re-prove, lock. Never patch on a hypothesis. Work in YOUR OWN
   isolated worktree (§8) — never the main checkout, never another LLM's worktree; `pwd` after every `cd`.

Open items are all in §1 FUTURE (optional, low priority). Nothing is blocking; the two branches are done.
