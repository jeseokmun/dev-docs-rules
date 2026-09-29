#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression: schema sync + render fixtures + docs_lint on rendered + selection."""
from __future__ import annotations
import argparse, json, subprocess, sys, tempfile
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
FIX = TOOLS / "_fixtures"

def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True)

def main(args: argparse.Namespace) -> int:
    fails: list[str] = []
    r = run([sys.executable, str(TOOLS / "schema_sync_check.py"), "--package", str(PKG)])
    if r.returncode:
        fails.append("schema_sync\n" + (r.stdout or r.stderr))
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        for schema, values, out_name in [
            ("DEV-10.schema.json", "habitcheck-dev10.values.json", "DEV-10-개요서.md"),
            ("DEV-30.schema.json", "habitcheck-dev30.values.json", "DEV-30-구조명세서.md"),
        ]:
            out = td_path / out_name
            r = run([
                sys.executable, str(TOOLS / "render_doc.py"),
                "--schema", str(PKG / "_schemas" / schema),
                "--values", str(FIX / values),
                "--out", str(out),
            ])
            if r.returncode or not out.exists():
                fails.append(f"render {schema}\n" + (r.stdout or r.stderr))
        empty30 = FIX / "empty-dev30.values.json"
        if not empty30.exists():
            empty30.write_text(json.dumps({"product": "Empty", "meta": {"상태": "draft"}, "open": []}, ensure_ascii=False), encoding="utf-8")
        e_root = td_path / "empty"
        e_root.mkdir()
        for schema, values, out_name in [
            ("DEV-10.schema.json", FIX / "empty-dev10.values.json", "DEV-10-개요서.md"),
            ("DEV-30.schema.json", empty30, "DEV-30-구조명세서.md"),
        ]:
            out = e_root / out_name
            r = run([
                sys.executable, str(TOOLS / "render_doc.py"),
                "--schema", str(PKG / "_schemas" / schema),
                "--values", str(values),
                "--out", str(out),
            ])
            if r.returncode:
                fails.append(f"render_empty {schema}\n" + (r.stdout or r.stderr))
            elif "## 미결" not in out.read_text(encoding="utf-8"):
                fails.append(f"empty_missing_open {out_name}")
        r = run([sys.executable, str(TOOLS / "docs_lint.py"), str(td_path), "--package", str(PKG), "--skip-schema-sync"])
        if r.returncode:
            fails.append("lint_rendered_full\n" + (r.stdout or r.stderr))
        # empty docs MUST fail missing ＊ headings (미결 alone is not enough)
        r = run([sys.executable, str(TOOLS / "docs_lint.py"), str(e_root), "--package", str(PKG), "--skip-schema-sync"])
        if r.returncode == 0:
            fails.append("empty_should_FAIL_missing_star_headings but PASSED")
        elif "MISSING_SECTION" not in (r.stdout or ""):
            fails.append("empty_fail_without_MISSING_SECTION\n" + (r.stdout or r.stderr))
    # extract → re-render round-trip on HabitCheck fixtures
    with tempfile.TemporaryDirectory() as td2:
        td2p = Path(td2)
        for md_name, schema, out_name in [
            ("out-DEV-10.md", "DEV-10.schema.json", "rt-DEV-10.md"),
            ("out-DEV-30.md", "DEV-30.schema.json", "rt-DEV-30.md"),
        ]:
            vals = td2p / (out_name + ".values.json")
            r = run([sys.executable, str(TOOLS / "extract_values.py"), "--md", str(FIX / md_name), "--out", str(vals)])
            if r.returncode or not vals.exists():
                fails.append(f"extract {md_name}\n" + (r.stdout or r.stderr))
                continue
            out = td2p / out_name
            r = run([
                sys.executable, str(TOOLS / "render_doc.py"),
                "--schema", str(PKG / "_schemas" / schema),
                "--values", str(vals),
                "--out", str(out),
            ])
            if r.returncode:
                fails.append(f"re-render {md_name}\n" + (r.stdout or r.stderr))
                continue
            if out.read_text(encoding="utf-8") != (FIX / md_name).read_text(encoding="utf-8"):
                fails.append(f"roundtrip_mismatch {md_name}")
    # docs_draft_cli: values → docs_root + no leftover json
    with tempfile.TemporaryDirectory() as td3:
        droot = Path(td3) / "docs"
        r = run([
            sys.executable, str(TOOLS / "docs_draft_cli.py"),
            "--docs-root", str(droot),
            "--type", "DEV-10",
            "--values", str(FIX / "habitcheck-dev10.values.json"),
            "--package", str(PKG),
        ])
        if r.returncode:
            fails.append("docs_draft_cli DEV-10\n" + (r.stdout or "") + (r.stderr or ""))
        elif not (droot / "DEV-10-개요서.md").exists():
            fails.append("docs_draft_cli missing out")
        elif list(droot.glob("*.json")):
            fails.append("docs_draft_cli left json in docs_root")
        # from-md + patch
        patch = Path(td3) / "patch.json"
        patch.write_text(json.dumps({"one_liner": "regress-patch"}, ensure_ascii=False), encoding="utf-8")
        r = run([
            sys.executable, str(TOOLS / "docs_draft_cli.py"),
            "--docs-root", str(droot),
            "--type", "DEV-10",
            "--from-md", str(FIX / "out-DEV-10.md"),
            "--patch", str(patch),
            "--package", str(PKG),
            "--skip-lint",
        ])
        if r.returncode:
            fails.append("docs_draft_cli from-md\n" + (r.stdout or "") + (r.stderr or ""))
        elif "regress-patch" not in (droot / "DEV-10-개요서.md").read_text(encoding="utf-8"):
            fails.append("docs_draft_cli patch not applied")

    # docs_refresh_cli: from docs_root typed md + patch
    with tempfile.TemporaryDirectory() as td4:
        droot = Path(td4) / "docs"
        droot.mkdir()
        # seed from fixture via draft
        r = run([
            sys.executable, str(TOOLS / "docs_draft_cli.py"),
            "--docs-root", str(droot),
            "--type", "DEV-30",
            "--values", str(FIX / "habitcheck-dev30.values.json"),
            "--package", str(PKG),
            "--skip-lint",
        ])
        if r.returncode:
            fails.append("seed for refresh\n" + (r.stdout or "") + (r.stderr or ""))
        else:
            patch = Path(td4) / "rpatch.json"
            patch.write_text(json.dumps({"summary": "refresh-regress"}, ensure_ascii=False), encoding="utf-8")
            r = run([
                sys.executable, str(TOOLS / "docs_refresh_cli.py"),
                "--docs-root", str(droot),
                "--type", "DEV-30",
                "--patch", str(patch),
                "--package", str(PKG),
                "--skip-lint",
            ])
            out = droot / "DEV-30-구조명세서.md"
            if r.returncode:
                fails.append("docs_refresh_cli\n" + (r.stdout or "") + (r.stderr or ""))
            elif "refresh-regress" not in out.read_text(encoding="utf-8"):
                fails.append("docs_refresh_cli patch not applied")
            elif list(droot.glob("*.json")):
                fails.append("docs_refresh_cli left json in docs_root")

    sel = Path("/workspace/selection/docs")
    if sel.is_dir():
        r = run([sys.executable, str(TOOLS / "docs_lint.py"), str(sel), "--package", str(PKG)])
        if r.returncode:
            fails.append("lint_selection\n" + (r.stdout or r.stderr))

    # plant preflight: fail only if package incomplete (exit 2). GatewAI BLOCKED is ok.
    r = run([sys.executable, str(TOOLS / "plant_light_preflight.py"), "--package", str(PKG)])
    if r.returncode == 2:
        fails.append("plant_light_preflight package\n" + (r.stdout or "") + (r.stderr or ""))
    elif r.returncode not in (0, 1):
        fails.append("plant_light_preflight unexpected\n" + (r.stdout or "") + (r.stderr or ""))

    # ideal advisory smoke (must run; must NOT fail regress on FAIL rows)
    r = run([sys.executable, str(TOOLS / "ideal_check_min.py"), "--print-boundary"])
    if r.returncode or "SKIP count=6" not in (r.stdout or ""):
        fails.append("ideal_print_boundary\n" + (r.stdout or "") + (r.stderr or ""))
    r = run([
        sys.executable,
        str(TOOLS / "ideal_check_min.py"),
        str(PKG / "_check" / "habitcheck-light"),
        "--summary-only",
    ])
    if r.returncode not in (0, 1) or "SUMMARY" not in (r.stdout or "") or "draft_gate=no" not in (r.stdout or ""):
        fails.append("ideal_summary_only\n" + (r.stdout or "") + (r.stderr or ""))
    r = run([
        sys.executable,
        str(TOOLS / "ideal_check_min.py"),
        str(PKG / "_check" / "habitcheck-light"),
        "--json",
    ])
    out = (r.stdout or "").strip()
    if r.returncode not in (0, 1) or '"tool": "ideal_check_min"' not in out or '"draft_gate": false' not in out:
        fails.append("ideal_json\n" + (r.stdout or "") + (r.stderr or ""))
    if sel.is_dir():
        r = run([sys.executable, str(TOOLS / "ideal_check_min.py"), str(sel)])
        if r.returncode not in (0, 1):
            fails.append("ideal_check_min usage/error\n" + (r.stdout or "") + (r.stderr or ""))
        elif "IDEAL 최소 자동검사" not in (r.stdout or ""):
            fails.append("ideal_check_min no report")

    # HabitCheck IDEAL fixed paths must exist + advisory run
    hc = PKG / "_check" / "habitcheck-light"
    if not (hc / "DEV-10-개요서.md").exists() or not (hc / "DEV-30-구조명세서.md").exists():
        fails.append("habitcheck-light docs missing")
    else:
        r = run([sys.executable, str(TOOLS / "ideal_check_min.py"), str(hc)])
        if r.returncode not in (0, 1) or "IDEAL 최소 자동검사" not in (r.stdout or ""):
            fails.append("ideal habitcheck-light\n" + (r.stdout or "") + (r.stderr or ""))


    # quality_regress_check: presence + --help only (full run is separate; avoids nested regress)
    qrc = TOOLS / "quality_regress_check.py"
    if not qrc.exists():
        fails.append("quality_regress_check.py missing")
    else:
        r = run([sys.executable, str(qrc), "--help"])
        help_txt = (r.stdout or "") + (r.stderr or "")
        if r.returncode or "QUALITY" not in help_txt:
            fails.append("quality_regress_check --help\n" + help_txt)
        elif "--json" not in help_txt or "--summary-only" not in help_txt:
            fails.append("quality_regress_check missing --json/--summary-only in --help")


    # HabitCheck examples ↔ all schemas
    r = run([sys.executable, str(TOOLS / "sample_schema_check.py"), "--package", str(PKG), "--summary-only"])
    if r.returncode or "SUMMARY sample_schema_check" not in (r.stdout or ""):
        fails.append("sample_schema_check\n" + (r.stdout or "") + (r.stderr or ""))

    # schema_sync / docs_lint Studio one-liners
    r = run([sys.executable, str(TOOLS / "schema_sync_check.py"), "--summary-only", "--package", str(PKG)])
    if r.returncode or "SUMMARY schema_sync" not in (r.stdout or ""):
        fails.append("schema_sync --summary-only\n" + (r.stdout or "") + (r.stderr or ""))
    if sel.is_dir():
        r = run([
            sys.executable, str(TOOLS / "docs_lint.py"), str(sel),
            "--package", str(PKG), "--summary-only",
        ])
        if r.returncode or "SUMMARY docs_lint" not in (r.stdout or ""):
            fails.append("docs_lint --summary-only\n" + (r.stdout or "") + (r.stderr or ""))


    fail_names = []
    for f in fails:
        first = (f.split("\n", 1)[0] or f).strip()
        fail_names.append(first[:80])

    result = "PASS" if not fails else "FAIL"
    summary = (
        f"SUMMARY regress_docs_pipeline {result} "
        f"fail={len(fails)} plant=no "
        f"fails={','.join(fail_names) if fail_names else '-'}"
    )
    payload = {
        "result": result,
        "ok": not fails,
        "fail": len(fails),
        "plant": False,
        "fails": fail_names,
        "summary": summary,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False))
    elif args.summary_only:
        print(summary)
    else:
        if fails:
            print("FAIL regress_docs_pipeline")
            for f in fails:
                print(" ", f)
        else:
            print(
                "PASS regress_docs_pipeline "
                "(… + sample_schema + plant_preflight + ideal + quality_regress_check --help + lint/sync summary)"
            )
        print(summary)

    return 0 if not fails else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="house docs pipeline regression (no plant)")
    ap.add_argument("--json", action="store_true", help="machine JSON on stdout")
    ap.add_argument(
        "--summary-only",
        action="store_true",
        help="print one SUMMARY line only (suppress verbose FAIL dumps)",
    )
    args = ap.parse_args()
    raise SystemExit(main(args))
