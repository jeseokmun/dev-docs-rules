#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Light-profile plant preflight. Confirmed facts only — does not invent product docs.

Checks house package readiness + optional existing docs_root.
GatewAI: reports blockers when docs_root/repo not confirmed; never writes product md.
"""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
PKG = TOOLS.parent

LIGHT_PKG = [
    "DEV-CONSTITUTION.md",
    "DOC-CONFIG.md",
    "_templates/DEV-10-개요서.md",
    "_templates/DEV-30-구조명세서.md",
    "_schemas/DEV-10.schema.json",
    "_schemas/DEV-30.schema.json",
    "_tools/render_doc.py",
    "_tools/docs_lint.py",
    "_tools/docs_draft_cli.py",
    "_skills/docs-draft.md",
    "_skills/docs-refresh.md",
    "_skills/docs-lint.md",
]

LIGHT_DOCS = [
    "DOC-CONFIG.md",
    "DEV-CONSTITUTION.md",
    "DEV-10-개요서.md",
    "DEV-30-구조명세서.md",
]


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def check_pkg(package: Path) -> list[str]:
    miss = []
    for rel in LIGHT_PKG:
        if not (package / rel).exists():
            miss.append(rel)
    return miss


def check_docs_root(docs_root: Path, package: Path) -> dict:
    out = {"exists": docs_root.is_dir(), "files": {}, "lint": None}
    if not out["exists"]:
        return out
    for name in LIGHT_DOCS:
        out["files"][name] = (docs_root / name).exists()
    r = run(
        [
            sys.executable,
            str(package / "_tools" / "docs_lint.py"),
            str(docs_root),
            "--package",
            str(package),
            "--only",
            "DEV-10",
        ]
    )
    r2 = run(
        [
            sys.executable,
            str(package / "_tools" / "docs_lint.py"),
            str(docs_root),
            "--package",
            str(package),
            "--only",
            "DEV-30",
        ]
    )
    out["lint"] = {
        "DEV-10": "PASS" if r.returncode == 0 else (r.stdout or r.stderr).strip()[:200],
        "DEV-30": "PASS" if r2.returncode == 0 else (r2.stdout or r2.stderr).strip()[:200],
    }
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Light plant preflight (no invent)")
    ap.add_argument("--package", default=str(PKG))
    ap.add_argument("--docs-root", help="existing planted docs_root to verify")
    ap.add_argument("--selection-docs", default="/workspace/selection/docs")
    ap.add_argument("--gatewai-preview", default="/workspace/gatewai-docs-preview")
    ap.add_argument("--json", action="store_true")
    ap.add_argument(
        "--summary-only",
        action="store_true",
        help="print one SUMMARY line only (Studio one-liner)",
    )
    args = ap.parse_args()
    if args.json and args.summary_only:
        print("error: use only one of --json / --summary-only", file=sys.stderr)
        raise SystemExit(2)

    package = Path(args.package)
    miss = check_pkg(package)
    selection = check_docs_root(Path(args.selection_docs), package)
    preview = Path(args.gatewai_preview)
    preview_10 = preview / "DEV-10-개요서.md"
    preview_30 = preview / "DEV-30-구조명세서.md"

    report = {
        "package_ready": len(miss) == 0,
        "package_missing": miss,
        "selection_reference": selection,
        "gatewai": {
            "docs_root_confirmed": False,
            "docs_root_path": None,
            "planted_light": False,
            "preview_dev10": preview_10.is_file(),
            "preview_dev30": preview_30.is_file(),
            "preview_is_not_plant": True,
            "repo_public_check": "404_or_private (api.github.com Berrysoft-git/26_E_GatewAIStudio)",
            "gh_cli": "not_authenticated",
            "blockers": [
                "docs_root 실제 경로 미확인",
                "DEV-30 미리보기/심기 없음",
                "소스 레포 공개 fetch 404 · gh 미인증 → 원격 tree 확인 불가",
                "심기 PR/커밋 증거 없음 (Selection만 실증)",
            ],
            "do_not": [
                "미리보기 DEV-10을 docs_root SSOT로 승격",
                "제품 사실 발명해 DEV-10/30 작성",
                "31종 카탈로그 채우기",
            ],
        },
        "verdict": None,
    }

    if args.docs_root:
        target = check_docs_root(Path(args.docs_root), package)
        report["target_docs_root"] = target
        report["gatewai"]["docs_root_path"] = args.docs_root
        report["gatewai"]["docs_root_confirmed"] = True
        files_ok = all(target.get("files", {}).values()) if target["exists"] else False
        lint_ok = target.get("lint") == {"DEV-10": "PASS", "DEV-30": "PASS"}
        report["gatewai"]["planted_light"] = bool(files_ok and lint_ok)

    sel_ok = (
        selection.get("exists")
        and all(selection.get("files", {}).values())
        and selection.get("lint") == {"DEV-10": "PASS", "DEV-30": "PASS"}
    )

    if miss:
        report["verdict"] = "FAIL_PACKAGE"
        code = 2
    elif not sel_ok:
        report["verdict"] = "WARN_SELECTION_REFERENCE"
        code = 1
    elif report["gatewai"]["planted_light"]:
        report["verdict"] = "GATEWAI_LIGHT_PLANTED"
        code = 0
    else:
        report["verdict"] = "BLOCKED_NEED_CONFIRMED_DOCS_ROOT_AND_FACTS"
        code = 0  # honesty check succeeded; plant itself blocked

    g = report["gatewai"]
    summary = (
        f"SUMMARY plant_light_preflight {report['verdict']} "
        f"package_ready={str(report['package_ready']).lower()} "
        f"selection_ok={str(bool(sel_ok)).lower()} "
        f"gatewai_planted={str(bool(g['planted_light'])).lower()} "
        f"blockers={len(g['blockers'])}"
    )
    if args.json:
        report["summary"] = summary
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.summary_only:
        print(summary)
    else:
        print(f"package_ready={report['package_ready']} missing={miss or '-'}")
        print(
            "selection="
            f"exists={selection.get('exists')} "
            f"files={selection.get('files')} lint={selection.get('lint')}"
        )
        print(
            "gatewai="
            f"preview10={g['preview_dev10']} preview30={g['preview_dev30']} "
            f"docs_root_confirmed={g['docs_root_confirmed']} planted={g['planted_light']}"
        )
        for b in g["blockers"]:
            print(f"  blocker: {b}")
        print(f"verdict={report['verdict']}")

    return code


if __name__ == "__main__":
    raise SystemExit(main())
