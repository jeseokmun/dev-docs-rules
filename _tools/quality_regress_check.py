#!/usr/bin/env python3
"""QUALITY package regression; scores require a separate evidence-based review."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from docs_common import atomic_write, cli
from regress_docs_pipeline import collect, PKG


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--package", type=Path, default=PKG)
    write = ap.add_mutually_exclusive_group()
    write.add_argument("--write", action="store_true", help="opt in to saving the Markdown report")
    write.add_argument("--no-write", action="store_true", help="read-only (default)")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--json", action="store_true")
    group.add_argument("--summary-only", action="store_true")
    args = ap.parse_args()
    rows = collect(args.package.resolve())
    fails = [r["name"] for r in rows if not r["ok"]]
    result = "FAIL" if fails else "PASS"
    summary = f"SUMMARY quality_regress {result} PASS={len(rows)-len(fails)} FAIL={len(fails)} checks={len(rows)} plant=no fails={','.join(fails) or '-'}"
    lines = ["# QUALITY 회귀 결과", "", datetime.now(timezone.utc).isoformat(), "",
             "| 검사 | 결과 |", "|---|---|"]
    lines += [f"| {r['name']} | {'PASS' if r['ok'] else 'FAIL'} |" for r in rows]
    lines += ["", "이 결과는 자동 검사 통과 여부다. 품질 점수는 QUALITY-REVIEW.md의 근거와 한계를 함께 본다.", ""]
    target = args.package / "_check" / "QUALITY-REGRESS-LAST.md"
    if args.write:
        atomic_write(target, "\n".join(lines))
    if args.json:
        print(json.dumps(dict(tool="quality_regress_check", result=result, ok=not fails,
                              plant=False, fail=len(fails), fails=fails, rows=rows,
                              last_path=str(target) if args.write else None, summary=summary), ensure_ascii=False))
    else:
        print(summary)
        if not args.summary_only:
            print("\n".join(lines))
            for r in rows:
                if not r["ok"]:
                    print(r["detail"])
    return int(bool(fails))


if __name__ == "__main__":
    raise SystemExit(cli(main))