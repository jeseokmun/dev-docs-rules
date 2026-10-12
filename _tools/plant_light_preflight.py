#!/usr/bin/env python3
"""Read-only readiness check for the package and an optional light docs_root."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
from docs_common import cli, run

PKG = Path(__file__).resolve().parents[1]
LIGHT_PKG = ["DEV-CONSTITUTION.md", "DOC-CONFIG.md",
             "_templates/DEV-10-개요서.md", "_templates/DEV-30-구조명세서.md",
             "_schemas/DEV-10.schema.json", "_schemas/DEV-30.schema.json",
             "_tools/render_doc.py", "_tools/extract_values.py", "_tools/document_edit.py",
             "_tools/docs_common.py", "_tools/docs_lint.py", "_tools/schema_sync_check.py",
             "_tools/docs_draft_cli.py", "_tools/docs_refresh_cli.py",
             "_skills/docs-draft.md", "_skills/docs-refresh.md", "_skills/docs-lint.md"]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--package", type=Path, default=PKG)
    ap.add_argument("--docs-root", type=Path, help="existing target; never inferred")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--json", action="store_true")
    group.add_argument("--summary-only", action="store_true")
    args = ap.parse_args()
    missing = [name for name in LIGHT_PKG if not (args.package / name).is_file()]
    fails = list(missing)
    lint = None
    if not missing:
        sync = run([sys.executable, str(args.package / "_tools/schema_sync_check.py"), "--package", str(args.package), "--summary-only"])
        if sync.returncode:
            fails.append("SCHEMA_SYNC")
    if args.docs_root is not None:
        for name in ("DOC-CONFIG.md", "DEV-CONSTITUTION.md"):
            if not (args.docs_root / name).is_file():
                fails.append(f"TARGET_MISSING {name}")
        if args.docs_root.is_dir() and not missing:
            result = run([sys.executable, str(args.package / "_tools/docs_lint.py"), str(args.docs_root),
                          "--package", str(args.package), "--skip-schema-sync", "--profile", "light", "--json"])
            lint = json.loads(result.stdout) if result.stdout.startswith("{") else {"ok": False}
            if result.returncode:
                fails.append("TARGET_LINT")
        else:
            fails.append("TARGET_MISSING docs_root")
    code = 2 if missing else 1 if fails else 0
    verdict = "FAIL_PACKAGE" if missing else "FAIL" if fails else "TARGET_READY" if args.docs_root else "PACKAGE_READY"
    summary = f"SUMMARY plant_light_preflight {verdict} package_ready={str(not missing).lower()} target_checked={str(args.docs_root is not None).lower()} plant=no"
    payload = dict(tool="plant_light_preflight", ok=code == 0, package_ready=not missing,
                   package_missing=missing, target=str(args.docs_root) if args.docs_root else None,
                   lint=lint, fails=fails, plant=False, verdict=verdict, summary=summary)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(summary)
        if not args.summary_only:
            print("\n".join(fails))
    return code


if __name__ == "__main__":
    raise SystemExit(cli(main))
