#!/usr/bin/env python3
"""Fail when a template says to drop a section because a value is unknown."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

from docs_common import cli, read_text

# Unknown value, not a known absence such as "이동이 없으면".
UNKNOWN = re.compile(
    r"모르면|정하기\s*전|합의\s*전|확인\s*전|확정되기\s*전|아직\s*쓰지\s*않|아직\s*모르"
)
# Drop or skip the section. Placeholder rows ("자리표시 행은 두지 않는다") do not match.
OMIT = re.compile(
    r"절을\s*지(?:운다|우고|워라)|절을\s*빼(?!도)|절을\s*두지\s*않|절을\s*만들지\s*않|"
    r"행이나\s*절을\s*지우"
)
def visible(text):
    return re.sub(r"^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$", "", text, flags=re.M | re.S)


def sentences(text):
    parts = re.split(r"(?<=[다요]\.)\s+|\n+", visible(text))
    return [part.strip() for part in parts if part.strip()]


def hides_unknown(text):
    hits = []
    for sentence in sentences(text):
        if not OMIT.search(sentence) or not UNKNOWN.search(sentence):
            continue
        if "없는 사실" in sentence and "다음 행동" in sentence:
            continue
        hits.append(re.sub(r"\s+", " ", sentence))
    return hits


def check(package):
    package = Path(package)
    root = package / "_templates"
    if not root.is_dir():
        raise ValueError("templates directory is missing")
    fails = []
    for path in sorted(root.glob("*.md")):
        for hit in hides_unknown(read_text(path)):
            fails.append(f"HIDE_UNKNOWN {path.name}: {hit}")
    return fails


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--package", type=Path, default=Path(__file__).resolve().parents[1])
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--summary-only", action="store_true")
    group.add_argument("--json", action="store_true")
    args = ap.parse_args()
    package = args.package.resolve()
    if not package.is_dir():
        ap.error("package must be a directory")
    fails = check(package)
    ok = not fails
    summary = f"SUMMARY template_unknown_check status={'PASS' if ok else 'FAIL'} fail_n={len(fails)}"
    if args.json:
        print(json.dumps(
            dict(tool="template_unknown_check", ok=ok, fail_n=len(fails), fails=fails, summary=summary),
            ensure_ascii=False,
        ))
    else:
        print(summary)
        if not args.summary_only:
            print("\n".join(fails))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(cli(main))
