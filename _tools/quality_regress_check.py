#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run the QUALITY × 회귀 checklist and stamp _check/QUALITY-REGRESS-LAST.md.

Does not plant product docs. GatewAI BLOCKED (preflight exit 1) is allowed.
Exit 0 only when every required check passes.

Studio/board helpers:
  --summary-only   one SUMMARY line (no markdown dump)
  --json           machine JSON on stdout (LAST md still written unless --no-write)
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
PKG = TOOLS.parent
CHECK = PKG / "_check"
KST = timezone(timedelta(hours=9))


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def row(name: str, ok: bool, detail: str) -> dict:
    return {"name": name, "ok": ok, "detail": detail.strip()[:400]}


def main() -> int:
    ap = argparse.ArgumentParser(description="QUALITY × 회귀 실행 + LAST 리포트")
    ap.add_argument("--package", type=Path, default=PKG)
    ap.add_argument("--selection", type=Path, default=Path("/workspace/selection/docs"))
    ap.add_argument("--write", action="store_true", default=True, help="write QUALITY-REGRESS-LAST.md")
    ap.add_argument("--no-write", action="store_true", help="skip writing LAST report")
    ap.add_argument("--json", action="store_true", help="print machine JSON to stdout")
    ap.add_argument(
        "--summary-only",
        action="store_true",
        help="print one SUMMARY line to stdout (suppresses markdown dump)",
    )
    args = ap.parse_args()
    package = args.package.resolve()
    tools = package / "_tools"
    check = package / "_check"
    rows: list[dict] = []

    # 1) 통합 회귀
    r = run([sys.executable, str(tools / "regress_docs_pipeline.py")])
    rows.append(row("regress_docs_pipeline", r.returncode == 0, r.stdout or r.stderr or ""))

    # 2) IDEAL HabitCheck light
    hc = check / "habitcheck-light"
    if (hc / "DEV-10-개요서.md").exists():
        r = run([sys.executable, str(tools / "ideal_check_min.py"), str(hc)])
        out = r.stdout or ""
        m = re.search(r"FAIL count=(\d+)", out)
        fail_n = int(m.group(1)) if m else None
        ok = (
            r.returncode in (0, 1)
            and "IDEAL 최소 자동검사" in out
            and fail_n == 0
        )
        rows.append(row("ideal HabitCheck light", ok, f"FAIL count={fail_n}; " + (out[-200:] if out else (r.stderr or ""))))
    else:
        rows.append(row("ideal HabitCheck light", False, "habitcheck-light missing"))

    # 3) IDEAL Selection
    sel = args.selection
    if sel.is_dir():
        r = run([sys.executable, str(tools / "ideal_check_min.py"), str(sel)])
        out = r.stdout or ""
        m = re.search(r"FAIL count=(\d+)", out)
        fail_n = int(m.group(1)) if m else None
        ok = (
            r.returncode in (0, 1)
            and "IDEAL 최소 자동검사" in out
            and fail_n == 0
        )
        rows.append(row("ideal Selection", ok, f"FAIL count={fail_n}; " + (out[-200:] if out else (r.stderr or ""))))
    else:
        rows.append(row("ideal Selection", False, f"missing {sel}"))

    # 4) docs_lint Selection
    if sel.is_dir():
        r = run([sys.executable, str(tools / "docs_lint.py"), str(sel), "--package", str(package)])
        rows.append(row("docs_lint Selection", r.returncode == 0, r.stdout or r.stderr or ""))
    else:
        rows.append(row("docs_lint Selection", False, f"missing {sel}"))

    # 5) plant preflight — exit 2 = package incomplete (fail); 0/1 OK (1=GatewAI BLOCKED)
    r = run([sys.executable, str(tools / "plant_light_preflight.py"), "--package", str(package)])
    ok = r.returncode in (0, 1)
    rows.append(row("plant_light_preflight", ok, (r.stdout or r.stderr or "")[-350:]))

    now = datetime.now(KST).strftime("%Y-%m-%d %H:%M KST")
    all_ok = all(x["ok"] for x in rows)
    pass_n = sum(1 for x in rows if x["ok"])
    fail_n = sum(1 for x in rows if not x["ok"])
    result = "PASS" if all_ok else "FAIL"
    fail_names = [x["name"] for x in rows if not x["ok"]]

    lines = [
        f"# QUALITY × 회귀 LAST ({now})",
        "",
        f"결과: **{result}** · A–F 점수는 `_check/QUALITY.md` 참고 (이 스크립트는 검사만).",
        "",
        "| 검사 | 결과 | 비고 |",
        "|---|---|---|",
    ]
    for x in rows:
        mark = "PASS" if x["ok"] else "FAIL"
        detail = x["detail"].replace("\n", " ").replace("|", "/")[:120]
        lines.append(f"| `{x['name']}` | {mark} | {detail} |")
    lines += [
        "",
        "## 명령",
        "```bash",
        "python3 _tools/quality_regress_check.py",
        "python3 _tools/quality_regress_check.py --summary-only",
        "python3 _tools/quality_regress_check.py --json",
        "```",
        "",
        "심기 금지 구간에서는 GatewAI BLOCKED(preflight 1)를 허용한다.",
        "",
    ]
    report = "\n".join(lines)

    summary = (
        f"SUMMARY quality_regress {result} PASS={pass_n} FAIL={fail_n} "
        f"checks={len(rows)} plant=no A-F=see_QUALITY.md "
        f"fails={','.join(fail_names) if fail_names else '-'}"
    )

    payload = {
        "when": now,
        "result": result,
        "ok": all_ok,
        "pass": pass_n,
        "fail": fail_n,
        "checks": len(rows),
        "plant": False,
        "scores": "see _check/QUALITY.md (A-F=4 declared)",
        "fails": fail_names,
        "rows": [{"name": x["name"], "ok": x["ok"], "detail": x["detail"][:200]} for x in rows],
        "summary": summary,
        "last_path": str(check / "QUALITY-REGRESS-LAST.md"),
    }

    if args.write and not args.no_write:
        out_path = check / "QUALITY-REGRESS-LAST.md"
        out_path.write_text(report, encoding="utf-8")
        print(f"wrote {out_path}", file=sys.stderr)

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif args.summary_only:
        print(summary)
    else:
        print(report)
        print(summary, file=sys.stderr)

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
