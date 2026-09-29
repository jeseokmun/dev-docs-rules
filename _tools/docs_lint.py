#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""docs-lint: check ＊ coverage on real docs_root files (DEV-10/30)."""
from __future__ import annotations
import argparse, json, re, sys, subprocess
from pathlib import Path

FAKE = re.compile(r"(^|\s)(_+|TBD TBD|lorem ipsum)(\s|$)", re.I)
SECRET = re.compile(r"(api[_-]?key\s*=\s*\S+|sk-[A-Za-z0-9]{10,}|Bearer\s+[A-Za-z0-9\-._]{12,})", re.I)
HEADING = re.compile(r"^##\s+(.+?)\s*$", re.M)

def star_labels(schema_path: Path) -> list[str]:
    if not schema_path.exists():
        return []
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    return [f["label"] for f in data.get("required", [])]

def headings(text: str) -> set[str]:
    return {m.group(1).strip() for m in HEADING.finditer(text)}

def check_file(path: Path, reqs: list[str]) -> list[str]:
    fails = []
    if not path.exists():
        return [f"MISSING {path}"]
    t = path.read_text(encoding="utf-8")
    hs = headings(t)
    for r in reqs:
        bare = r.split(" ", 1)[-1] if " " in r else r
        if r in hs:
            continue
        if any(bare in h and ("＊" in h or "○" in h) for h in hs):
            continue
        fails.append(f"MISSING_SECTION {path.name}: {r}")
    if FAKE.search(t):
        fails.append(f"FAKEFILL {path}")
    if SECRET.search(t):
        fails.append(f"SECRET_LIKE {path}")
    for i, line in enumerate(t.splitlines(), 1):
        if line.startswith("|") and "|---|" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if any(c == "" for c in cells):
                fails.append(f"EMPTY_CELL {path.name}:{i}")
                break
    return fails

def main() -> int:
    ap = argparse.ArgumentParser(description="docs-lint DEV-10/30 ＊ headings + empty/secret")
    ap.add_argument("docs_root")
    ap.add_argument("--package", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--skip-schema-sync", action="store_true")
    ap.add_argument("--only", choices=["DEV-10", "DEV-30"], help="check one type only")
    ap.add_argument("--json", action="store_true", help="machine JSON on stdout")
    ap.add_argument(
        "--summary-only",
        action="store_true",
        help="print one SUMMARY line only",
    )
    args = ap.parse_args()
    root = Path(args.docs_root)
    pkg = Path(args.package)
    req10 = star_labels(pkg / "_schemas" / "DEV-10.schema.json") or [
        "＊ 한 줄 소개", "＊ 누구를 위한가", "＊ 핵심 기능", "＊ 실행·설치", "＊ 시스템 경계"
    ]
    req30 = star_labels(pkg / "_schemas" / "DEV-30.schema.json") or [
        "＊ 한 줄 구조 요약", "＊ 모듈/레이어", "＊ 구조도 (Mermaid)", "＊ 의존 규칙", "＊ 건드리기 위험 구역"
    ]
    fails: list[str] = []
    checked = []
    if args.only in (None, "DEV-10"):
        checked.append("DEV-10")
        fails += check_file(root / "DEV-10-개요서.md", req10)
    if args.only in (None, "DEV-30"):
        checked.append("DEV-30")
        fails += check_file(root / "DEV-30-구조명세서.md", req30)
    sync_line = ""
    pkg_check = pkg / "_check" / "check_docs.py"
    if pkg_check.exists():
        r = subprocess.run([sys.executable, str(pkg_check), str(pkg)], capture_output=True, text=True)
        if r.returncode != 0:
            fails.append("TEMPLATE_CHECK\n" + (r.stdout or r.stderr))
    if not args.skip_schema_sync:
        sync = Path(__file__).with_name("schema_sync_check.py")
        if sync.exists():
            cmd = [sys.executable, str(sync), "--package", str(pkg)]
            if args.summary_only or args.json:
                cmd.append("--summary-only")
            r = subprocess.run(cmd, capture_output=True, text=True)
            sync_line = (r.stdout or "").strip()
            if r.returncode != 0:
                fails.append("SCHEMA_SYNC\n" + sync_line + (r.stderr or ""))
    ok = not fails
    summary = (
        f"SUMMARY docs_lint status={'PASS' if ok else 'FAIL'} "
        f"docs_root={root} types={','.join(checked)} fail_n={len(fails)}"
    )
    payload = {
        "tool": "docs_lint",
        "ok": ok,
        "docs_root": str(root),
        "types": checked,
        "fail_n": len(fails),
        "fails": fails,
        "schema_sync": sync_line,
        "summary": summary,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False))
        return 0 if ok else 1
    if args.summary_only:
        print(summary)
        return 0 if ok else 1
    if sync_line and not args.skip_schema_sync:
        print(sync_line)
    if fails:
        print("FAIL")
        for f in fails:
            print(" ", f)
        return 1
    print("PASS docs-lint (DEV-10/30 ＊ headings from schema + empty/secret + schema_sync)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
