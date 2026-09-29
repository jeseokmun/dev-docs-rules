#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""docs-refresh CLI: thin front for docs_draft_cli --from-md.

Requires an existing md under docs_root (or explicit --from-md).
Values JSON stays ephemeral (handled by docs_draft_cli). DEV-10 / DEV-30 only.
"""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
PKG = TOOLS.parent

OUT_NAME = {
    "DEV-10": "DEV-10-개요서.md",
    "DEV-30": "DEV-30-구조명세서.md",
}


def main() -> int:
    ap = argparse.ArgumentParser(description="docs-refresh: extract+patch+render via docs_draft_cli")
    ap.add_argument("--docs-root", required=True)
    ap.add_argument("--type", required=True, choices=["DEV-10", "DEV-30"])
    ap.add_argument("--from-md", help="defaults to docs_root typed filename")
    ap.add_argument("--patch", help="confirmed-facts JSON patch (ephemeral input)")
    ap.add_argument("--package", default=str(PKG))
    ap.add_argument("--skip-lint", action="store_true")
    ap.add_argument("--keep-temp", action="store_true")
    args = ap.parse_args()

    docs_root = Path(args.docs_root)
    src = Path(args.from_md) if args.from_md else docs_root / OUT_NAME[args.type]
    if not src.exists():
        print(f"missing md for refresh: {src} (use docs-draft for new)", file=sys.stderr)
        return 2

    cmd = [
        sys.executable, str(TOOLS / "docs_draft_cli.py"),
        "--docs-root", str(docs_root),
        "--type", args.type,
        "--from-md", str(src),
        "--package", str(args.package),
    ]
    if args.patch:
        cmd.extend(["--patch", args.patch])
    if args.skip_lint:
        cmd.append("--skip-lint")
    if args.keep_temp:
        cmd.append("--keep-temp")
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
