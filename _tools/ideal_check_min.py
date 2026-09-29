#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minimal IDEAL auto-check for DEV-10/30.

IMPORTANT: IDEAL is NOT a draft fail condition (헌법). This tool is advisory.
Exit 0 always when checks ran (report printed). Exit 2 on usage error.
Mechanically unknowable items → SKIP (not FAIL).
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

HEADING = re.compile(r"^##\s+(.+?)\s*$", re.M)
URL = re.compile(r"https?://\S+|git@\S+")
CMD = re.compile(r"`[^`\n]*(?:npx|npm|pnpm|yarn|expo|flutter|dart|cargo|dotnet|python3?|uv)[^`\n]*`|(?:^|[^\w])(?:npx|npm|expo|flutter|dart)\s+[\w:-]+", re.I | re.M)
PATHISH = re.compile(r"`[^`]+/(?:src|lib|app|Assets)[^`]*`|`[^`]+\.(?:ts|tsx|js|dart|cs|py)`")
MERMAID = re.compile(r"```mermaid\s*\n(.*?)```", re.S)
# ASCII-only node labels heuristic (Korean preferred when language=ko)
ASCII_BOX = re.compile(r"\[[A-Za-z][A-Za-z0-9 _/-]{2,}\]")


def headings(t: str) -> set[str]:
    return {m.group(1).strip() for m in HEADING.finditer(t)}


def row(item: str, status: str, note: str = "") -> dict:
    return {"item": item, "status": status, "note": note}


def check_dev10(path: Path) -> list[dict]:
    t = path.read_text(encoding="utf-8")
    hs = headings(t)
    out = []
    # 1 repo URL / runnable command — weak heuristic
    if URL.search(t) or CMD.search(t):
        out.append(row("1 실행·URL 복붙 힌트", "PASS", "URL 또는 실행 명령 패턴"))
    else:
        out.append(row("1 실행·URL 복붙 힌트", "FAIL", "http(s)/git 또는 실행 명령 패턴 없음"))
    # 2 동기 단락 — can't judge quality
    out.append(row("2 동기 차별점", "SKIP", "내용 품질은 사람 채점"))
    # 3 성공·검증 섹션 존재
    if any("성공" in h or "검증" in h for h in hs):
        out.append(row("3 성공·검증 섹션", "PASS", "헤딩 존재(자동 테스트 연결은 SKIP)"))
    else:
        out.append(row("3 성공·검증 섹션", "FAIL", "○ 성공·검증 헤딩 없음"))
    out.append(row("3b 자동테스트 연결", "SKIP", "CI/테스트 파일 대조 없음"))
    # 4 관련 문서
    if any("관련" in h for h in hs) and ("DEV-20" in t or "DEV-30" in t):
        out.append(row("4 관련 DEV 링크 힌트", "PASS", "관련 문서에 DEV-20/30 언급"))
    elif any("관련" in h for h in hs):
        out.append(row("4 관련 DEV 링크 힌트", "FAIL", "관련 문서는 있으나 DEV-20/30 없음"))
    else:
        out.append(row("4 관련 DEV 링크 힌트", "FAIL", "관련 문서 섹션 없음"))
    out.append(row("4b active/일정", "SKIP", "상태·일정은 사람"))
    # 5 플랫폼 미결
    out.append(row("5 플랫폼 미결 없음", "SKIP", "제품 범위는 사람"))
    return out


def check_dev30(path: Path) -> list[dict]:
    t = path.read_text(encoding="utf-8")
    hs = headings(t)
    out = []
    # 1 paths look pathish — not verified against tree
    if PATHISH.search(t):
        out.append(row("1 경로 표기", "PASS", "path-like 토큰 있음(트리 일치=SKIP)"))
    else:
        out.append(row("1 경로 표기", "FAIL", "src/lib/app 경로 토큰 없음"))
    out.append(row("1b 트리 일치", "SKIP", "레포 트리 대조 없음"))
    # 2 failure/idempotent flow
    out.append(row("2 실패·멱등 흐름", "SKIP", "시퀀스 품질은 사람"))
    # 3 DEV-35/50 links
    if "DEV-35" in t or "DEV-50" in t:
        out.append(row("3 DEV-35/50 연결 힌트", "PASS"))
    else:
        out.append(row("3 DEV-35/50 연결 힌트", "FAIL", "본문에 DEV-35/50 없음(light에선 흔함)"))
    # 4 test hints / DEV-65
    if "DEV-65" in t or re.search(r"테스트|test", t, re.I):
        out.append(row("4 테스트 힌트", "PASS"))
    else:
        out.append(row("4 테스트 힌트", "FAIL", "테스트/DEV-65 힌트 없음"))
    # 5 Mermaid labels
    m = MERMAID.search(t)
    if not m:
        out.append(row("5 Mermaid 존재", "FAIL", "mermaid fence 없음"))
    else:
        body = m.group(1)
        ascii_boxes = ASCII_BOX.findall(body)
        # allow mixed; flag if many ASCII-only boxes and almost no Hangul
        hangul = bool(re.search(r"[가-힣]", body))
        if hangul and len(ascii_boxes) <= 2:
            out.append(row("5 Mermaid 라벨 언어", "PASS", "한글 라벨 감지"))
        elif hangul:
            out.append(row("5 Mermaid 라벨 언어", "PASS", f"한글 있음·ASCII박스 {len(ascii_boxes)}(경고만)"))
        else:
            out.append(row("5 Mermaid 라벨 언어", "FAIL", "한글 라벨 없음(ko 가정)"))
    return out


def print_report(title: str, path: Path, rows: list[dict]) -> None:
    print(f"## {title}  `{path}`")
    print("| 항목 | 결과 | 비고 |")
    print("|---|---|---|")
    for r in rows:
        print(f"| {r['item']} | {r['status']} | {r['note']} |")
    print()


def count_status(rows: list[dict]) -> dict[str, int]:
    out = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    for r in rows:
        s = r["status"]
        if s in out:
            out[s] += 1
    return out


def print_summary(docs_root: Path, all_rows: list[dict], missing: list[str]) -> None:
    c = count_status(all_rows)
    miss = ",".join(missing) if missing else "-"
    print(
        f"SUMMARY docs_root={docs_root} PASS={c['PASS']} FAIL={c['FAIL']} SKIP={c['SKIP']} missing={miss} draft_gate=no"
    )


BOUNDARY_ROWS = [
    # (type, id, ideal_short, machine, skip_reason_or_empty)
    ("DEV-10", "1", "레포 URL·실행 명령", "weak: URL/cmd pattern", ""),
    ("DEV-10", "2", "동기·차별점", "SKIP", "내용 품질은 사람"),
    ("DEV-10", "3", "성공·검증 섹션", "heading only", ""),
    ("DEV-10", "3b", "자동테스트 연결", "SKIP", "CI/테스트 파일 대조 없음"),
    ("DEV-10", "4", "관련 DEV 링크", "hint: 관련+DEV-20/30", ""),
    ("DEV-10", "4b", "active/일정", "SKIP", "상태·일정은 사람"),
    ("DEV-10", "5", "플랫폼 미결 없음", "SKIP", "제품 범위는 사람"),
    ("DEV-30", "1", "경로 표기", "path-like token", ""),
    ("DEV-30", "1b", "트리 일치", "SKIP", "레포 트리 대조 없음"),
    ("DEV-30", "2", "실패·멱등 흐름", "SKIP", "시퀀스 품질은 사람"),
    ("DEV-30", "3", "DEV-35/50 연결", "string hint", ""),
    ("DEV-30", "4", "테스트 힌트", "string hint", ""),
    ("DEV-30", "5", "Mermaid 라벨 언어", "hangul/ascii heuristic", ""),
]


def print_boundary() -> None:
    print("# IDEAL machine/SKIP boundary (advisory; not draft gate)\n")
    print("| 유형 | # | 이상형 | 기계 | SKIP 이유 |")
    print("|---|---|---|---|---|")
    for typ, iid, ideal, machine, skip in BOUNDARY_ROWS:
        print(f"| {typ} | {iid} | {ideal} | {machine} | {skip} |")
    skips = sum(1 for *_, m, s in BOUNDARY_ROWS if m == "SKIP")
    print(f"\nSKIP count={skips} / total={len(BOUNDARY_ROWS)}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("docs_root", nargs="?", default="")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any FAIL (still not draft gate)")
    ap.add_argument("--print-boundary", action="store_true", help="print machine/SKIP inventory and exit")
    ap.add_argument(
        "--summary",
        action="store_true",
        help="one-line PASS/FAIL/SKIP counts (still prints full tables unless --summary-only)",
    )
    ap.add_argument(
        "--summary-only",
        action="store_true",
        help="print only the SUMMARY line (implies --summary)",
    )
    ap.add_argument("--json", action="store_true", help="machine JSON on stdout (no markdown tables)")
    args = ap.parse_args()
    if args.print_boundary:
        print_boundary()
        return 0
    if args.json and args.summary_only:
        print("error: use only one of --json / --summary-only", file=sys.stderr)
        return 2
    if not args.docs_root:
        ap.error("docs_root required unless --print-boundary")
    root = Path(args.docs_root)
    if not root.is_dir():
        print(f"missing docs_root {root}", file=sys.stderr)
        return 2
    want_summary = args.summary or args.summary_only
    show_tables = not args.summary_only and not args.json
    fails = 0
    all_rows: list[dict] = []
    missing: list[str] = []
    reports: list[dict] = []
    p10 = root / "DEV-10-개요서.md"
    p30 = root / "DEV-30-구조명세서.md"
    if show_tables:
        print("# IDEAL 최소 자동검사 (draft 실패 조건 아님)\n")
    if p10.exists():
        rows = check_dev10(p10)
        all_rows.extend(rows)
        reports.append({"type": "DEV-10", "path": str(p10), "rows": rows})
        if show_tables:
            print_report("DEV-10", p10, rows)
        fails += sum(1 for r in rows if r["status"] == "FAIL")
    else:
        missing.append("DEV-10")
        if show_tables:
            print(f"(skip DEV-10 — missing {p10})\n")
    if p30.exists():
        rows = check_dev30(p30)
        all_rows.extend(rows)
        reports.append({"type": "DEV-30", "path": str(p30), "rows": rows})
        if show_tables:
            print_report("DEV-30", p30, rows)
        fails += sum(1 for r in rows if r["status"] == "FAIL")
    else:
        missing.append("DEV-30")
        if show_tables:
            print(f"(skip DEV-30 — missing {p30})\n")
    if show_tables:
        print(f"FAIL count={fails} (advisory). draft 게이트 아님.")
    counts = count_status(all_rows)
    miss = ",".join(missing) if missing else "-"
    summary = (
        f"SUMMARY docs_root={root} PASS={counts['PASS']} FAIL={counts['FAIL']} "
        f"SKIP={counts['SKIP']} missing={miss} draft_gate=no"
    )
    if args.json:
        payload = {
            "tool": "ideal_check_min",
            "docs_root": str(root),
            "ok": fails == 0 and not missing,
            "pass": counts["PASS"],
            "fail": counts["FAIL"],
            "skip": counts["SKIP"],
            "missing": missing,
            "draft_gate": False,
            "reports": reports,
            "summary": summary,
        }
        print(json.dumps(payload, ensure_ascii=False))
    elif want_summary:
        print_summary(root, all_rows, missing)
    if args.strict and fails:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
