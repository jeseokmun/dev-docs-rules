#!/usr/bin/env python3
"""Validate every bundled HabitCheck example against its document schema."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from docs_common import cli
from docs_lint import check_file
from schema_sync_check import catalog_fails
from docs_common import load_object


def discover_pairs(pkg):
    pairs = []
    for schema in sorted((pkg / "_schemas").glob("DEV-*.schema.json")):
        code = schema.name.removesuffix(".schema.json")
        examples = sorted((pkg / "_examples").glob(f"{code}-*.HabitCheck.md"))
        pairs.extend((schema, example) for example in examples)
        if not examples:
            pairs.append((schema, pkg / "_examples" / f"{code}-MISSING.HabitCheck.md"))
    return pairs


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--package", type=Path, default=Path(__file__).resolve().parents[1])
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--summary-only", action="store_true")
    group.add_argument("--json", action="store_true")
    args = ap.parse_args()
    pairs = discover_pairs(args.package)
    fails = catalog_fails(args.package)
    for schema, example in pairs:
        fails.extend(check_file(example, load_object(schema)))
    ok = not fails
    summary = f"SUMMARY sample_schema_check status={'PASS' if ok else 'FAIL'} pairs={len(pairs)} fail_n={len(fails)}"
    if args.json:
        print(json.dumps(dict(tool="sample_schema_check", ok=ok, pairs=len(pairs), fail_n=len(fails), fails=fails, summary=summary), ensure_ascii=False))
    else:
        print(summary)
        if not args.summary_only:
            print("\n".join(fails))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(cli(main))