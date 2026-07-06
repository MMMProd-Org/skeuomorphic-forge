#!/usr/bin/env python3
"""Non-regression check: recess/well shadow stacks in the golden file MUST carry a
visible top machined-lip RIM (warm rgba, alpha >= 0.20) — the §16.2 hard floor.

A missing or too-faint rim is the skill's documented "#1 recurring failure": the
well looks flat despite deep shadows. This guard fails CI if a targeted recess
stack drops its rim below 0.20, so a future edit cannot silently reintroduce the
bug (the failure mode that survived 5 prior manual audits).

Targets: golden code blocks whose nearest heading OR immediate label names a
well / display / recess (the copy-source stacks agents reproduce). Rails, chassis
and button stacks are intentionally excluded — a raised surface has no recess lip.

Usage:
  python3 scripts/check_rim_floors.py            # check golden, exit 1 on failure
  python3 scripts/check_rim_floors.py --selftest # verify the detector logic itself
"""

import re
import sys
from pathlib import Path

GOLDEN = Path(__file__).parent.parent / "references" / "00-golden-examples.md"
RIM_FLOOR = 0.20
TARGET_RE = re.compile(r"well|display|recess", re.I)

# A top machined-lip rim layer: "(inset) 0 1px 0 rgba(255, g, b, a)".
RIM_LAYER_RE = re.compile(
    r"(?:inset\s+)?0\s+1px\s+0\s+rgba\(\s*255\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)"
)


def block_has_rim(block: str) -> bool:
    """True if the block has a warm (g>=240) top-lip rim at alpha >= RIM_FLOOR."""
    for g, _, a in RIM_LAYER_RE.findall(block):
        if int(g) >= 240 and float(a) >= RIM_FLOOR:
            return True
    return False


def is_recess(block: str) -> bool:
    """A recess/well carries depth via multiple inset layers; a flat surface does not."""
    return block.count("inset") >= 3


def parse_blocks(text: str):
    """Yield (context, code) per fenced code block. context = nearest heading + the
    immediate preceding non-empty text line (enough to name the stack)."""
    lines = text.split("\n")
    heading = ""
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if line.startswith("#"):
            heading = line
            i += 1
            continue
        if line.strip().startswith("```"):
            label = ""
            j = i - 1
            while j >= 0:
                s = lines[j].strip()
                if s and not s.startswith("```"):
                    label = lines[j]
                    break
                j -= 1
            code = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            yield (heading + " || " + label, "\n".join(code))
        i += 1


def check(text: str):
    """Return (n_checked, failures) where failures is a list of (context, reason)."""
    failures = []
    checked = 0
    for context, code in parse_blocks(text):
        if not TARGET_RE.search(context) or not is_recess(code):
            continue
        checked += 1
        if not block_has_rim(code):
            failures.append(
                (context.strip(), f"no top rim layer with alpha >= {RIM_FLOOR}")
            )
    return checked, failures


def selftest() -> int:
    ok = (
        "inset 0 12px 30px rgba(0,0,0,0.95),\n"
        "inset 0 6px 14px rgba(0,0,0,0.85),\n"
        "inset 0 -12px 30px rgba(0,0,0,0.8),\n"
        "inset 0 1px 0 rgba(255,250,240,0.22)"
    )
    bad = ok.replace("rgba(255,250,240,0.22)", "rgba(255,255,255,0.05)")
    assert block_has_rim(ok) is True, "must accept a warm rim >= 0.20"
    assert block_has_rim(bad) is False, "must reject a faint/cold rim < 0.20"
    assert is_recess(ok) is True, "3+ inset layers is a recess"
    assert is_recess("0 2px 4px rgba(0,0,0,0.3)") is False, (
        "single drop is not a recess"
    )
    print("selftest OK")
    return 0


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    if not GOLDEN.exists():
        print(f"::error::golden file not found: {GOLDEN}")
        return 1
    checked, failures = check(GOLDEN.read_text(encoding="utf-8", errors="replace"))
    if failures:
        for ctx, reason in failures:
            print(
                f"::error::recess stack missing §16.2 rim ({reason}) near: {ctx[:120]}"
            )
        print(
            f"FAIL: {len(failures)}/{checked} recess/well stacks miss rim floor >= {RIM_FLOOR}"
        )
        return 1
    print(f"OK: {checked} recess/well stacks all carry a top rim >= {RIM_FLOOR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
