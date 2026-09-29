#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare schema ＊/○ labels 1:1 with template ## headings.

Auto-discovers pairs by scanning _schemas/*.schema.json and matching
_templates/DEV-XX-*.md by the same code prefix.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

HEADING = re.compile(r"^##\s+(.+?)\s*$")
CODE_RE = re.compile(r"^(DEV-\d+)\.schema\.json$")

def headings(md: Path) -> list[str]:
    out = []
    for line in md.read_text(encoding="utf-8").splitlines():
        m = HEADING.match(line)
        if m:
            out.append(m.group(1).strip())
    return out

def section_labels(schema: dict) -> list[str]:
    labels = [f["label"] for f in schema.get("required", [])]
    labels += [f["label"] for f in schema.get("optional", [])]
    oi = schema.get("open_items")
    if oi and oi.get("label"):
        labels.append(oi["label"])
    return labels

def check_pair(schema_path: Path, template_path: Path) -> list[str]:
    fails = []
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    if not template_path.exists():
        return [f"MISSING_TEMPLATE {template_path}"]
    hs = headings(template_path)
    for label in section_labels(schema):
        if label not in hs:
            fails.append(f"SCHEMA_NOT_IN_TEMPLATE {schema['code']}: {label}")
    req = {f["label"] for f in schema.get("required", [])}
    opt = {f["label"] for f in schema.get("optional", [])}
    open_l = {(schema.get("open_items") or {}).get("label")}
    known = req | opt | open_l
    for h in hs:
        if h.startswith("＊") and h not in req:
            fails.append(f"TEMPLATE_STAR_NOT_IN_SCHEMA_REQUIRED {schema['code']}: {h}")
        if h.startswith("○") and h not in opt:
            fails.append(f"TEMPLATE_OPT_NOT_IN_SCHEMA {schema['code']}: {h}")
    return fails

def discover_pairs(pkg: Path) -> list[tuple[Path, Path]]:
    schemas_dir = pkg / "_schemas"
    templates_dir = pkg / "_templates"
    pairs: list[tuple[Path, Path]] = []
    for sp in sorted(schemas_dir.glob("DEV-*.schema.json")):
        m = CODE_RE.match(sp.name)
        if not m:
            continue
        code = m.group(1)
        matches = sorted(templates_dir.glob(f"{code}-*.md"))
        if not matches:
            pairs.append((sp, templates_dir / f"{code}-MISSING.md"))
        else:
            pairs.append((sp, matches[0]))
    return pairs

def main() -> int:
    ap = argparse.ArgumentParser(description="schema ↔ template ＊·○ 1:1")
    ap.add_argument(
        "--package",
        default=str(Path(__file__).resolve().parents[1]),
        help="package root (schemas + templates)",
    )
    ap.add_argument("--json", action="store_true", help="machine JSON on stdout")
    ap.add_argument(
        "--summary-only",
        action="store_true",
        help="print one SUMMARY line only",
    )
    args = ap.parse_args()
    pkg = Path(args.package)
    pairs = discover_pairs(pkg)
    fails: list[str] = []
    for sp, tp in pairs:
        if not sp.exists():
            fails.append(f"MISSING_SCHEMA {sp}")
            continue
        fails += check_pair(sp, tp)
    ok = not fails
    summary = (
        f"SUMMARY schema_sync status={'PASS' if ok else 'FAIL'} "
        f"pairs={len(pairs)} fail_n={len(fails)}"
    )
    payload = {
        "tool": "schema_sync_check",
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
        print("FAIL schema_sync_check")
        for f in fails:
            print(" ", f)
        return 1
    codes = ",".join(
        CODE_RE.match(sp.name).group(1) for sp, _ in pairs if CODE_RE.match(sp.name)
    )
    print(f"PASS schema_sync_check ({len(pairs)} pairs ＊·○·미결 1:1; auto-discover)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
