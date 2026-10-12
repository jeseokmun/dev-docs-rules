#!/usr/bin/env python3
"""Check relative Markdown file targets; no network or anchor interpretation."""
from __future__ import annotations
import argparse
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from docs_common import cli, read_text


def check_links(package):
    fails = []
    for path in sorted(package.rglob("*.md")):
        if any(p.startswith(".") for p in path.relative_to(package).parts):
            continue
        text = read_text(path)
        # Skip fenced code examples, including shell snippets with Markdown strings.
        text = re.sub(r"^`{3,}[^\n]*\n.*?^`{3,}\s*$", "", text, flags=re.M | re.S)
        for value in re.findall(r"\[[^\]\n]+\]\((<[^>]+>|[^\s)]+)\)", text):
            value = value.strip("<>")
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc:
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path.resolve()
            if not target.exists():
                fails.append(f"MISSING_LINK {path.relative_to(package).as_posix()}: {value}")
    return fails


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--package", type=Path, default=Path(__file__).resolve().parents[1])
    args = ap.parse_args()
    if not args.package.is_dir():
        ap.error("package must be a directory")
    fails = check_links(args.package.resolve())
    print(f"SUMMARY check_links status={'FAIL' if fails else 'PASS'} fail_n={len(fails)}")
    for fail in fails:
        print(fail)
    return int(bool(fails))


if __name__ == "__main__":
    raise SystemExit(cli(main))
