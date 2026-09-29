#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check HabitCheck examples against all DEV-* schemas (＊ headings + no empty cells)."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

HEADING = re.compile(r"^##\s+(.+?)\s*$", re.M)
PKG = Path(__file__).resolve().parents[1]

def headings(text: str) -> set[str]:
    return {m.group(1).strip() for m in HEADING.finditer(text)}

def empty_cell_lines(text: str) -> list[int]:
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith("|") and not re.match(r"^\|[\s\-:|]+\|$", line):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if any(c == "" for c in cells):
                out.append(i)
    return out

def check_one(schema_path: Path, md_path: Path) -> list[str]:
    fails = []
    if not md_path.exists():
        return [f"MISSING {md_path}"]
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    text = md_path.read_text(encoding="utf-8")
    hs = headings(text)
    for f in schema.get("required", []):
        label = f["label"]
        if label not in hs:
            fails.append(f"MISSING_SECTION {md_path.name}: {label}")
    empties = empty_cell_lines(text)
    if empties:
        fails.append(f"EMPTY_CELL {md_path.name}:{empties[0]}")
    return fails

def discover_pairs(pkg: Path) -> list[tuple[Path, Path]]:
    """Prefer habitcheck-schema-samples, else _examples/DEV-*-*.HabitCheck.md."""
    pairs = []
    samples = pkg / "_check" / "habitcheck-schema-samples"
    examples = pkg / "_examples"
    for sp in sorted((pkg / "_schemas").glob("DEV-*.schema.json")):
        code = sp.name.replace(".schema.json", "")
        # known nested samples first
        candidates = []
        if samples.exists():
            candidates += sorted(samples.glob(f"{code}-*.md"))
            candidates += sorted(samples.glob(f"{code}-*/*.md"))
        candidates += sorted(examples.glob(f"{code}-*.HabitCheck.md"))
        # dedupe by resolving; prefer samples dir
        seen = set()
        chosen = None
        for c in candidates:
            key = c.resolve()
            if key in seen:
                continue
            seen.add(key)
            if c.name.endswith(".HabitCheck.md") or c.suffix == ".md":
                chosen = c
                if samples in c.parents or samples == c.parent:
                    break  # prefer sample under habitcheck-schema-samples
        if chosen is None:
            pairs.append((sp, examples / f"{code}-MISSING.HabitCheck.md"))
        else:
            # if we broke early on samples, use that; else last chosen is examples
            # recompute prefer samples
            sample_hits = [c for c in candidates if samples in c.parents or c.parent == samples]
            pairs.append((sp, sample_hits[0] if sample_hits else chosen))
    return pairs

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", default=str(PKG))
    ap.add_argument("--summary-only", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    pkg = Path(args.package)
    pairs = discover_pairs(pkg)
    fails: list[str] = []
    for sp, mp in pairs:
        if not sp.exists():
            fails.append(f"MISSING_SCHEMA {sp.name}")
            continue
        fails += check_one(sp, mp)
    ok = not fails
    summary = (
        f"SUMMARY sample_schema_check status={'PASS' if ok else 'FAIL'} "
        f"pairs={len(pairs)} fail_n={len(fails)}"
    )
    payload = {
        "tool": "sample_schema_check",
        "ok": ok,
        "pairs": len(pairs),
        "fail_n": len(fails),
        "fails": fails,
        "summary": summary,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False))
        return 0 if ok else 1
    if args.summary_only:
        print(summary)
        return 0 if ok else 1
    if fails:
        print("FAIL sample_schema_check")
        for f in fails:
            print(" ", f)
        return 1
    print(f"PASS sample_schema_check (HabitCheck {len(pairs)} schemas ＊ + no empty cells)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
