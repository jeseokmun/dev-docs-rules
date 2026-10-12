#!/usr/bin/env python3
"""Stage, validate and atomically write a DEV-10/30 document."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
import tempfile

from docs_common import atomic_write, cli, load_object, run
from document_edit import refresh_text, validate_values
from extract_values import detect_code, extract
from render_doc import render_dev10, render_dev30

TOOLS = Path(__file__).resolve().parent
PKG = TOOLS.parent
OUT_NAME = {"DEV-10": "DEV-10-개요서.md", "DEV-30": "DEV-30-구조명세서.md"}


def deep_merge(base, patch):
    out = dict(base)
    for key, value in patch.items():
        out[key] = deep_merge(out[key], value) if isinstance(value, dict) and isinstance(out.get(key), dict) else value
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--docs-root", required=True, type=Path)
    ap.add_argument("--type", required=True, choices=list(OUT_NAME))
    ap.add_argument("--values", type=Path)
    ap.add_argument("--from-md", type=Path)
    ap.add_argument("--patch", type=Path)
    ap.add_argument("--package", default=PKG, type=Path)
    ap.add_argument("--skip-lint", action="store_true", help="explicitly allow unvalidated drafts")
    ap.add_argument("--overwrite", action="store_true", help="replace existing output for a new draft")
    args = ap.parse_args()
    if not args.values and not args.from_md:
        ap.error("need --values and/or --from-md")
    if args.docs_root.is_symlink():
        ap.error("docs_root must not be a symlink")
    target = args.docs_root / OUT_NAME[args.type]
    if target.is_symlink():
        ap.error("output must not be a symlink")
    old_bytes = target.read_bytes() if target.exists() else None
    if old_bytes is not None and not args.from_md and not args.overwrite:
        ap.error("output exists; use --from-md for refresh or --overwrite for replacement")
    schema = load_object(args.package / "_schemas" / f"{args.type}.schema.json")
    base, changes, original = {}, {}, None
    if args.from_md:
        original = args.from_md.read_bytes().decode("utf-8-sig")
        if detect_code(original, None) != args.type:
            ap.error("--from-md code differs from --type")
        base = extract(original, args.type)
    for path in (args.values, args.patch):
        if path:
            incoming = load_object(path)
            validate_values(args.type, incoming)
            changes = deep_merge(changes, incoming)
    base = deep_merge(base, changes)
    validate_values(args.type, base, strict=False)
    renderer = render_dev10 if args.type == "DEV-10" else render_dev30
    rendered = renderer(schema, base)
    candidate = refresh_text(original, rendered, args.type, changes) if original is not None else rendered
    # No product path is modified until all validation succeeds.
    with tempfile.TemporaryDirectory(prefix="docs-draft-") as td:
        stage = Path(td)
        atomic_write(stage / target.name, candidate)
        settings = args.docs_root / "DOC-CONFIG.md"
        if settings.is_file():
            (stage / settings.name).write_bytes(settings.read_bytes())
        if not args.skip_lint:
            result = run([sys.executable, str(TOOLS / "docs_lint.py"), str(stage),
                          "--package", str(args.package), "--only", args.type])
            sys.stdout.write(result.stdout)
            sys.stderr.write(result.stderr)
            if result.returncode:
                return result.returncode
    if target.is_symlink() or (target.read_bytes() if target.exists() else None) != old_bytes:
        print("error: output changed during validation; retry from the current document", file=sys.stderr)
        return 1
    # Preserve exact original bytes for a no-op in-place refresh (including BOM/CRLF).
    if original is not None and not changes and args.from_md.resolve() == target.resolve():
        print(f"unchanged {target}")
        return 0
    atomic_write(target, candidate)
    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(cli(main))
