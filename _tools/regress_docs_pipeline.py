#!/usr/bin/env python3
"""Run reproducible package regression checks without modifying the checkout."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
from docs_common import atomic_write, cli, run

PKG = Path(__file__).resolve().parents[1]


def collect(package):
    tool = package / "_tools"
    commands = [
        ("schema_sync", [sys.executable, str(tool / "schema_sync_check.py"), "--package", str(package), "--summary-only"]),
        ("sample_schema", [sys.executable, str(tool / "sample_schema_check.py"), "--package", str(package), "--summary-only"]),
        ("demo_full", [sys.executable, str(tool / "docs_lint.py"), str(package / "demo-docs"), "--package", str(package), "--skip-schema-sync", "--summary-only"]),
        ("links", [sys.executable, str(tool / "check_links.py"), "--package", str(package)]),
        ("tests", [sys.executable, "-m", "unittest", "discover", "-s", str(package / "tests"), "-v"]),
    ]
    rows = []
    for name, command in commands:
        r = run(command)
        detail = (r.stdout + r.stderr).strip()
        ok = r.returncode == 0
        rows.append(dict(name=name, ok=ok, detail=detail))
    return rows


def main(tool="regress_docs_pipeline"):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--package", type=Path, default=PKG)
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--json", action="store_true")
    group.add_argument("--summary-only", action="store_true")
    if tool == "quality_regress_check":
        write = ap.add_mutually_exclusive_group()
        write.add_argument("--write", action="store_true", help="save a Markdown result report")
        write.add_argument("--no-write", action="store_true", help="read-only (default)")
    args = ap.parse_args()
    rows = collect(args.package.resolve())
    fails = [r["name"] for r in rows if not r["ok"]]
    result = "FAIL" if fails else "PASS"
    name = "quality_regress" if tool == "quality_regress_check" else tool
    summary = f"SUMMARY {name} {result} checks={len(rows)} fail={len(fails)} plant=no fails={','.join(fails) or '-'}"
    payload = dict(tool=tool, result=result, ok=not fails, fail=len(fails), plant=False, fails=fails, rows=rows, summary=summary)
    if tool == "quality_regress_check":
        target = args.package / "_check/QUALITY-REGRESS-LAST.md"
        payload["last_path"] = str(target) if args.write else None
        if args.write:
            lines = ["# 회귀 검사 결과", "", "| 검사 | 결과 |", "|---|---|"]
            lines += [f"| {r['name']} | {'PASS' if r['ok'] else 'FAIL'} |" for r in rows]
            atomic_write(target, "\n".join(lines) + "\n")
    if args.json:
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(summary)
        if not args.summary_only:
            for row in rows:
                if not row["ok"]:
                    print(row["name"], row["detail"])
    return int(bool(fails))


if __name__ == "__main__":
    raise SystemExit(cli(main))
