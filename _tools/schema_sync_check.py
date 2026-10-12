#!/usr/bin/env python3
"""Check catalog/schema/template coverage in both directions."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

from docs_common import body, cli, load_object, read_text, sections, tables


def headings(path):
    # Templates intentionally wrap the copyable body in a markdown fence.
    return re.findall(r"^##\s+(.+?)\s*$", read_text(path), re.M)


def section_labels(schema):
    fields = schema.get("required", []) + schema.get("optional", [])
    if schema.get("open_items"):
        fields += [schema["open_items"]]
    return [f["label"] for f in fields]


def check_pair(schema_path, template_path):
    schema = load_object(schema_path)
    code = schema_path.name.removesuffix(".schema.json")
    if not template_path.is_file():
        return [f"MISSING_TEMPLATE {code}"]
    fails = []
    if schema.get("code") != code:
        fails.append(f"SCHEMA_CODE {code}")
    if template_path.name != f"{code}-{schema.get('title')}.md":
        fails.append(f"TEMPLATE_NAME {code}")
    expected_path = "{docs_root}/" + f"{code}-{schema.get('title')}"
    expected_path += ".md" if schema.get("single_file") else f"/{code}-{{슬러그}}.md"
    if schema.get("path_pattern") != expected_path:
        fails.append(f"SCHEMA_PATH {code}")
    fields = schema.get("required", []) + schema.get("optional", [])
    ids, labels = [f["id"] for f in fields], section_labels(schema)
    if len(ids) != len(set(ids)) or len(labels) != len(set(labels)):
        fails.append(f"DUPLICATE_SCHEMA_FIELD {code}")
    if not schema.get("required") or not isinstance(schema.get("single_file"), bool):
        fails.append(f"INVALID_SCHEMA {code}")
    for f in fields:
        if f["type"] not in {"string", "table", "kv_rows", "numbered_rows", "mermaid", "table_or_mermaid"}:
            fails.append(f"UNKNOWN_FIELD_TYPE {code}: {f['id']}")
    hs = headings(template_path)
    for label in labels:
        if hs.count(label) != 1:
            fails.append(f"SCHEMA_NOT_IN_TEMPLATE_ONCE {code}: {label}")
    req = {f["label"] for f in schema.get("required", [])}
    opt = {f["label"] for f in schema.get("optional", [])}
    for h in hs:
        if h.startswith("＊") and h not in req:
            fails.append(f"TEMPLATE_STAR_NOT_IN_SCHEMA_REQUIRED {code}: {h}")
        if h.startswith("○") and h not in opt:
            fails.append(f"TEMPLATE_OPT_NOT_IN_SCHEMA {code}: {h}")
    template = read_text(template_path)
    # Unwrap the copyable Markdown body before using the fence-aware parser.
    match = re.search(r"```markdown\s*\n(.*?)\n```", template, re.S)
    if not match:
        fails.append(f"MISSING_COPY_BODY {code}")
    else:
        blocks = {label: body(raw) for label, raw in sections(match[1])}
        for field in schema.get("required", []):
            if field["type"] in {"table", "numbered_rows", "kv_rows"}:
                found = list(tables(blocks.get(field["label"], "")))
                expected = ["구분", "내용"] if field["type"] == "kv_rows" else field["columns"]
                if not found or found[0][0] != expected:
                    fails.append(f"TEMPLATE_COLUMNS {code}: {field['label']}")
    return fails


def discover_pairs(pkg):
    return [(p, next(iter(sorted((pkg / "_templates").glob(p.name.removesuffix(".schema.json") + "-*.md"))),
                     pkg / "_templates" / (p.stem + "-MISSING.md")))
            for p in sorted((pkg / "_schemas").glob("DEV-*.schema.json"))]


def catalog_fails(pkg):
    schemas = {p.name.removesuffix(".schema.json") for p in (pkg / "_schemas").glob("DEV-*.schema.json")}
    templates = {}
    fails = []
    for path in (pkg / "_templates").glob("DEV-*.md"):
        match = re.match(r"^(DEV-\d+)-", path.name)
        if match:
            templates.setdefault(match[1], []).append(path)
    if not schemas or not templates:
        fails.append("EMPTY_CATALOG")
    for code in sorted(set(templates) - schemas):
        fails.append(f"MISSING_SCHEMA {code}")
    for code, paths in templates.items():
        if len(paths) != 1:
            fails.append(f"DUPLICATE_TEMPLATE {code}")
    constitution = pkg / "DEV-CONSTITUTION.md"
    if not constitution.is_file():
        fails.append("MISSING_CONSTITUTION")
    else:
        # Only catalog rows in §3.1/3.2, not examples or prose.
        registered = set(re.findall(r"^\| (DEV-\d+) \|", read_text(constitution), re.M))
        for code in sorted(registered - schemas):
            fails.append(f"CATALOG_MISSING_SCHEMA {code}")
        for code in sorted(schemas - registered):
            fails.append(f"UNREGISTERED_SCHEMA {code}")
    return fails


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--package", type=Path, default=Path(__file__).resolve().parents[1])
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--json", action="store_true")
    group.add_argument("--summary-only", action="store_true")
    args = ap.parse_args()
    pairs = discover_pairs(args.package)
    fails = catalog_fails(args.package)
    for schema, template in pairs:
        fails.extend(check_pair(schema, template))
    ok = not fails
    summary = f"SUMMARY schema_sync status={'PASS' if ok else 'FAIL'} pairs={len(pairs)} fail_n={len(fails)}"
    if args.json:
        print(json.dumps(dict(tool="schema_sync_check", ok=ok, pairs=len(pairs), fail_n=len(fails), fails=fails, summary=summary), ensure_ascii=False))
    else:
        print(summary)
        if not args.summary_only:
            print("\n".join(fails))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(cli(main))
