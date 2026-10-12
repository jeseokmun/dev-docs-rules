#!/usr/bin/env python3
"""Run reproducible package regression checks without modifying the checkout."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
from docs_common import cli, run

PKG = Path(__file__).resolve().parents[1]


def collect(package, include_tests=True):
    tool = package / "_tools"
    commands = [
        ("schema_sync", [sys.executable, str(tool / "schema_sync_check.py"), "--package", str(package), "--summary-only"]),
        ("sample_schema", [sys.executable, str(tool / "sample_schema_check.py"), "--package", str(package), "--summary-only"]),
        ("demo_full", [sys.executable, str(tool / "docs_lint.py"), str(package / "demo-docs"), "--package", str(package), "--summary-only"]),
        ("preflight", [sys.executable, str(tool / "plant_light_preflight.py"), "--package", str(package), "--docs-root", str(package / "demo-docs"), "--summary-only"]),
        ("links", [sys.executable, str(tool / "check_links.py"), "--package", str(package)]),
        ("ideal_boundary", [sys.executable, str(tool / "ideal_check_min.py"), "--print-boundary"]),
        ("ideal_json", [sys.executable, str(tool / "ideal_check_min.py"), str(package / "demo-docs"), "--json"]),
    ]
    if include_tests:
        commands.append(("tests", [sys.executable, "-m", "unittest", "discover", "-s", str(package / "tests"), "-v"]))
    rows = []
    for name, command in commands:
        r = run(command)
        detail = (r.stdout + r.stderr).strip()
        ok = r.returncode == 0
        if name == "ideal_json" and ok:
            payload = json.loads(r.stdout)
            ok = payload["tool"] == "ideal_check_min" and payload["draft_gate"] is False
        rows.append(dict(name=name, ok=ok, detail=detail))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--package", type=Path, default=PKG)
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--json", action="store_true")
    group.add_argument("--summary-only", action="store_true")
    args = ap.parse_args()
    rows = collect(args.package.resolve())
    fails = [r["name"] for r in rows if not r["ok"]]
    result = "FAIL" if fails else "PASS"
    summary = f"SUMMARY regress_docs_pipeline {result} checks={len(rows)} fail={len(fails)} plant=no fails={','.join(fails) or '-'}"
    if args.json:
        print(json.dumps(dict(tool="regress_docs_pipeline", result=result, ok=not fails, fail=len(fails), plant=False, fails=fails, rows=rows, summary=summary), ensure_ascii=False))
    else:
        print(summary)
        if not args.summary_only:
            for row in rows:
                if not row["ok"]:
                    print(row["name"], row["detail"])
    return int(bool(fails))


if __name__ == "__main__":
    raise SystemExit(cli(main))