#!/usr/bin/env python3
"""Non-regression guard for numeric shadow-floor contradictions in the golden file.

Two documented recurring failures came from the golden/SKILL specs holding a value
BELOW the §16 floor, so agents copied the low value:
  - §16.2: a recess/well top machined-lip rim must be >= 0.20 (else the well looks
    flat despite deep shadows -- the "#1 recurring failure").
  - §16.5: screw heads need >= 7 shadow layers (they sit ON the surface and need
    pronounced depth); the golden shipped a 5-layer stack.

This guard fails CI if the golden drops either below its floor, so a future edit
cannot silently reintroduce a failure mode that survived 5 manual audits.

Usage:
  python3 scripts/check_shadow_floors.py            # check golden, exit 1 on failure
  python3 scripts/check_shadow_floors.py --selftest # verify the detector logic itself
"""

import re
import sys
from pathlib import Path

GOLDEN = Path(__file__).parent.parent / "references" / "00-golden-examples.md"
RIM_FLOOR = 0.20
SCREW_MIN_LAYERS = 7
RECESS_RE = re.compile(r"well|display|recess", re.I)
SCREW_RE = re.compile(r"screw head", re.I)

# A top machined-lip rim layer: "(inset) 0 1px 0 rgba(255, g, b, a)".
RIM_LAYER_RE = re.compile(
    r"(?:inset\s+)?0\s+1px\s+0\s+rgba\(\s*255\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)"
)
# A box-shadow declaration value, JSX (`...`) or CSS (...;).
BOXSHADOW_RE = re.compile(r"boxShadow\s*:\s*`([^`]*)`|box-shadow\s*:\s*([^;]*);", re.I)


def block_has_rim(block: str) -> bool:
    """True if the block has a warm (g>=240) top-lip rim at alpha >= RIM_FLOOR."""
    for g, _, a in RIM_LAYER_RE.findall(block):
        if int(g) >= 240 and float(a) >= RIM_FLOOR:
            return True
    return False


def is_recess(block: str) -> bool:
    """A recess/well carries depth via multiple inset layers; a flat surface does not."""
    return block.count("inset") >= 3


def count_layers(decl: str) -> int:
    """Count comma-separated shadow layers at parenthesis depth 0."""
    depth, segs = 0, 1
    for ch in decl:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            segs += 1
    return segs


def max_boxshadow_layers(block: str) -> int:
    best = 0
    for m in BOXSHADOW_RE.finditer(block):
        decl = (m.group(1) or m.group(2) or "").strip()
        if decl:
            best = max(best, count_layers(decl))
    return best


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
        if RECESS_RE.search(context) and is_recess(code):
            checked += 1
            if not block_has_rim(code):
                failures.append((context.strip(), f"recess rim < {RIM_FLOOR} (16.2)"))
        if SCREW_RE.search(context):
            checked += 1
            layers = max_boxshadow_layers(code)
            if layers < SCREW_MIN_LAYERS:
                failures.append(
                    (
                        context.strip(),
                        f"screw stack {layers} layers, need >= {SCREW_MIN_LAYERS} (16.5)",
                    )
                )
    return checked, failures


def selftest() -> int:
    rim_ok = "inset x,\ninset y,\ninset z,\ninset 0 1px 0 rgba(255,250,240,0.22)"
    rim_bad = "inset x,\ninset y,\ninset z,\ninset 0 1px 0 rgba(255,255,255,0.05)"
    assert block_has_rim(rim_ok), "must accept a warm rim >= 0.20"
    assert not block_has_rim(rim_bad), "must reject a faint/cold rim < 0.20"
    assert is_recess(rim_ok), "3+ inset layers is a recess"

    screw7 = (
        "boxShadow: `\n" + ",\n".join(f"a{i} rgba(0,0,0,1)" for i in range(7)) + "\n`,"
    )
    screw5 = (
        "boxShadow: `\n" + ",\n".join(f"a{i} rgba(0,0,0,1)" for i in range(5)) + "\n`,"
    )
    assert max_boxshadow_layers(screw7) == 7, "must count 7 layers"
    assert max_boxshadow_layers(screw5) == 5, "must count 5 layers"
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
            print(f"::error::shadow floor violated ({reason}) near: {ctx[:120]}")
        print(f"FAIL: {len(failures)}/{checked} golden stacks below a shadow floor")
        return 1
    print(f"OK: {checked} golden stacks all meet their shadow floor")
    return 0


if __name__ == "__main__":
    sys.exit(main())
