#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""docs-draft CLI: values(JSON ephemeral) → render → lint. Optional extract-from-md merge.

md under docs_root is SSOT. Values JSON is written only under a temp dir and deleted.
Does not invent facts. DEV-10 / DEV-30 only.
"""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys, tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
PKG = TOOLS.parent

OUT_NAME = {
    "DEV-10": "DEV-10-개요서.md",
    "DEV-30": "DEV-30-구조명세서.md",
}
SCHEMA = {
    "DEV-10": PKG / "_schemas" / "DEV-10.schema.json",
    "DEV-30": PKG / "_schemas" / "DEV-30.schema.json",
}


def deep_merge(base: dict, patch: dict) -> dict:
    out = dict(base)
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="docs-draft: render DEV-10/30 into docs_root")
    ap.add_argument("--docs-root", required=True)
    ap.add_argument("--type", required=True, choices=["DEV-10", "DEV-30"])
    ap.add_argument("--values", help="confirmed facts JSON (ephemeral input)")
    ap.add_argument("--from-md", help="existing md to extract base values from (refresh-style draft)")
    ap.add_argument("--patch", help="JSON patch merged onto extracted/base values")
    ap.add_argument("--package", default=str(PKG))
    ap.add_argument("--skip-lint", action="store_true")
    ap.add_argument("--keep-temp", action="store_true", help="debug only — do not use in skills")
    args = ap.parse_args()

    code = args.type
    docs_root = Path(args.docs_root)
    docs_root.mkdir(parents=True, exist_ok=True)
    out_md = docs_root / OUT_NAME[code]
    schema = Path(args.package) / "_schemas" / f"{code}.schema.json"
    if not schema.exists():
        schema = SCHEMA[code]

    if not args.values and not args.from_md:
        print("need --values and/or --from-md", file=sys.stderr)
        return 2

    td = tempfile.mkdtemp(prefix="docs-draft-")
    try:
        vals_path = Path(td) / "vals.json"
        base: dict = {}
        if args.from_md:
            src = Path(args.from_md)
            if not src.exists():
                print(f"missing --from-md {src}", file=sys.stderr)
                return 2
            extracted = Path(td) / "extracted.json"
            r = run([sys.executable, str(TOOLS / "extract_values.py"), "--md", str(src), "--out", str(extracted)])
            if r.returncode:
                print(r.stdout or r.stderr, file=sys.stderr)
                return r.returncode or 1
            base = json.loads(extracted.read_text(encoding="utf-8"))
        if args.values:
            incoming = json.loads(Path(args.values).read_text(encoding="utf-8"))
            base = deep_merge(base, incoming) if base else incoming
        if args.patch:
            patch = json.loads(Path(args.patch).read_text(encoding="utf-8"))
            base = deep_merge(base, patch)

        vals_path.write_text(json.dumps(base, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        r = run([
            sys.executable, str(TOOLS / "render_doc.py"),
            "--schema", str(schema),
            "--values", str(vals_path),
            "--out", str(out_md),
        ])
        if r.returncode:
            print(r.stdout or r.stderr, file=sys.stderr)
            return r.returncode or 1
        print(f"wrote {out_md}")

        if not args.skip_lint:
            r = run([
                sys.executable, str(TOOLS / "docs_lint.py"),
                str(docs_root),
                "--package", str(Path(args.package)),
                "--only", code,
            ])
            sys.stdout.write(r.stdout or "")
            if r.stderr:
                sys.stderr.write(r.stderr)
            if r.returncode:
                return r.returncode
        return 0
    finally:
        if args.keep_temp:
            print(f"temp kept: {td}", file=sys.stderr)
        else:
            shutil.rmtree(td, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
