#!/usr/bin/env python3
"""Read-only check that each fact is stated only by its owner files."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
from urllib.parse import unquote

from docs_common import body, cli, read_text, sections, tables

OPEN_IDS = (
    "HC-REPO",
    "HC-DRIFT-VER",
    "HC-HASH",
    "HC-PKG",
    "HC-LEGAL",
    "HC-CHANNEL",
)

# Patterns recognize a fact typed differently from the copied sentence.
# They are not extra facts; the sentence in fact-owners.json is the wording.
RESTATE = {
    "HC-STREAK": re.compile(
        r"CheckIn\.localDate만 센다|하루가 비면|과거로 이어진|weeklyGoal은 세지 않는다|"
        r"가장 최근 날이 어제|빈 날 없이 이어진|오늘만 해제하면|주당 목표와 더하지"
    ),
    "HC-DRIFT-STATE": re.compile(
        r"drift\s+proposed|proposed이며\s*accepted|accepted가\s*아니다|accepted는\s*아님|"
        r"accepted가\s*되면|accepted로\s*올릴|결정 상태는 proposed|"
        r"DB는 drift proposed|로컬 DB는 drift proposed|상태는 proposed"
    ),
    "HC-FLAG": re.compile(
        r"weekly_summary.{0,80}(?:\bon\b|기본)|(?:\bon\b|기본).{0,80}weekly_summary",
        re.I | re.S,
    ),
    "HC-MIDNIGHT": re.compile(
        r"기기\s*로컬\s*자정|로컬\s*자정|자정을\s*기기\s*로컬|자정(?:은|을|이).{0,24}추측"
    ),
    "HC-PLATFORM": re.compile(r"Android\s*8\.0|Flutter\s*3\.22|Dart\s*3\.4", re.I),
    "TOOL-PY": re.compile(
        r"python3`?가 없으면|`python`이 없으면|없으면.{0,40}python3|python3.{0,24}없으면|"
        r"python`?\s*대신\s*`?python3|python3`?\s*대신\s*`?python|Windows에서 `python3`"
    ),
}

OPEN_VALUE = {
    "HC-REPO": re.compile(
        r"git\s+clone\s+(?!HC-REPO\b|<repo-url\b)(?:https?://|git@|ssh://)\S+"
        r"|https?://(?!github\.com/jeseokmun/dev-docs-rules(?:/|[)>\"'.,`]|\s|$))[A-Za-z0-9][^\s<>)`]*"
        r"|git@[A-Za-z0-9][\w.-]*:",
        re.I,
    ),
    "HC-DRIFT-VER": re.compile(r"drift[^0-9\n]{0,16}\d+\.\d+", re.I),
    "HC-HASH": re.compile(r"\b[a-fA-F0-9]{40}\b|\b[a-fA-F0-9]{64}\b|sha256:[A-Za-z0-9+/=]{16,}", re.I),
    "HC-PKG": re.compile(
        r"applicationId\s*[:=]\s*['\"]?[A-Za-z][\w.]*|\bcom\.[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+\b"
    ),
    "HC-LEGAL": re.compile(
        r"\b(?:MIT|Apache-2\.0|BSD-2-Clause|BSD-3-Clause|GPL-2\.0|GPL-3\.0|"
        r"LGPL-2\.1|LGPL-3\.0|MPL-2\.0|ISC|Unlicense|AGPL-3\.0)\b"
    ),
    "HC-CHANNEL": re.compile(
        r"https?://(?:discord\.gg|slack\.com|t\.me)/\S+|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|(?<!\w)#[a-z][a-z0-9_-]{2,}",
        re.I,
    ),
}


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


def visible(text):
    return re.sub(r"^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$", "", text, flags=re.M | re.S)


def ignored(rel):
    parts = Path(rel).parts
    if any(part.startswith(".") for part in parts):
        return True
    if "_history" in parts:
        return True
    return len(parts) >= 2 and parts[0] == "_tools" and parts[1] == "_fixtures"


def sentence_list(fact):
    value = fact.get("sentence", None)
    if value is None:
        return []
    if isinstance(value, str) and value.strip():
        return [value]
    if isinstance(value, list) and value and all(isinstance(item, str) and item.strip() for item in value):
        return value
    raise ValueError("sentence must be a non-empty string, a list of strings, or null")


def load_facts(package):
    path = Path(package) / "_schemas" / "fact-owners.json"
    data = json.loads(read_text(path))
    facts = data.get("facts")
    if not isinstance(facts, list) or not facts:
        raise ValueError("facts must be a non-empty list")
    seen = set()
    for fact in facts:
        if not isinstance(fact, dict) or not isinstance(fact.get("id"), str):
            raise ValueError("each fact needs an id")
        if fact["id"] in seen:
            raise ValueError("duplicate fact id")
        seen.add(fact["id"])
        owners = fact.get("owners", [])
        if not isinstance(owners, list) or not all(isinstance(owner, str) for owner in owners):
            raise ValueError("owners must be a list of paths")
        sentence_list(fact)
        if fact["id"] in OPEN_IDS and (fact.get("sentence") is not None or owners):
            raise ValueError("open fact must keep a null sentence and no owners")
        if fact["id"] not in OPEN_IDS and (not owners or not sentence_list(fact)):
            raise ValueError("owned fact needs owners and a sentence")
    missing = [item for item in OPEN_IDS if item not in seen]
    if missing:
        raise ValueError("open fact id missing")
    return facts


def contains(text, sentence):
    return norm(sentence) in norm(text)


def exit_restated(text):
    for match in re.finditer(r"종료\s*코드|\bexit\b", text, re.I):
        chunk = text[match.start():match.start() + 500]
        ordered = re.search(
            r"(?<![\d.])0(?![\d.]).{0,160}(?<![\d.])1(?![\d.]).{0,160}(?<![\d.])2(?![\d.])",
            chunk,
            re.S,
        )
        if ordered and re.search(r"성공|통과|실패|입력|오류|완료", chunk):
            return True
    return False


def restates(fact_id, text, sentences):
    if any(contains(text, sentence) for sentence in sentences):
        return True
    pattern = RESTATE.get(fact_id)
    if pattern and pattern.search(text):
        return True
    return fact_id == "TOOL-EXIT" and exit_restated(text)


def distinctive_phrases(sentence):
    phrases = []
    for part in re.split(r"[。．.·|]", sentence):
        part = norm(part.strip(" `*"))
        if len(part) >= 8:
            phrases.append(part)
    return phrases


def cell_restate_fails(docs, facts):
    indexed, fails, seen = [], [], set()
    for fact in facts:
        if fact["id"] in OPEN_IDS:
            continue
        phrases = []
        for sentence in sentence_list(fact):
            phrases.extend(distinctive_phrases(sentence))
        if phrases:
            indexed.append((fact["id"], set(fact.get("owners") or []), phrases))
    for rel, _path, _raw, text in docs:
        for _headers, rows in tables(text):
            for row in rows:
                for cell in row:
                    folded = norm(cell)
                    for fact_id, owners, phrases in indexed:
                        if rel in owners or fact_id not in cell:
                            continue
                        key = (fact_id, rel)
                        if key in seen:
                            continue
                        if any(phrase in folded for phrase in phrases):
                            seen.add(key)
                            fails.append(f"CELL_RESTATE {fact_id} {rel}")
    return fails


def cell_paths(cell):
    found = []
    for target in re.findall(r"\[[^\]\n]*\]\(([^)\s]+)\)", cell):
        found.append(target)
    for tick in re.findall(r"`([^`]+)`", cell):
        match = re.search(r"\S+\.md", tick)
        if match:
            found.append(match.group(0))
    if ".md" in cell and "`" not in cell and "](" not in cell:
        match = re.search(r"\S+\.md", cell)
        if match:
            found.append(match.group(0))
    paths = []
    for raw in found:
        cleaned = unquote(raw.strip().strip("<>")).split("#", 1)[0].split("?", 1)[0].strip()
        if cleaned.endswith(".md") and "{" not in cleaned and "…" not in cleaned and "..." not in cleaned:
            paths.append(cleaned)
    return paths


def own_codes(text, path):
    codes = set(re.findall(r"^#\s+(DEV-\d+)\b", text, re.M))
    codes.update(re.findall(r"^\|\s*코드\s*\|\s*`?(DEV-\d+)`?\s*\|", text, re.M))
    match = re.search(r"(DEV-\d+)", path.name)
    if match:
        codes.add(match.group(1))
    return codes


def related_fails(path, text):
    plain = visible(text)
    listed, cited, body_parts, has_related = set(), [], [], False
    for label, block in sections(plain):
        if label and "관련" in label:
            has_related = True
            for _headers, rows in tables(body(block)):
                for row in rows:
                    for cell in row:
                        listed.update(re.findall(r"DEV-\d+", cell))
                        cited.extend(cell_paths(cell))
        else:
            body_parts.append(block)
    fails = []
    if has_related:
        mentions = set(re.findall(r"DEV-\d+", "".join(body_parts))) - own_codes(text, path)
        for code in sorted(mentions - listed):
            fails.append(("RELATED_OMIT", code))
        seen = set()
        for cited_path in cited:
            if cited_path in seen:
                continue
            seen.add(cited_path)
            if not (path.parent / cited_path).resolve().is_file():
                fails.append(("RELATED_MISSING", cited_path))
    return fails


def check(package):
    package = Path(package)
    facts = load_facts(package)
    docs = []
    for path in sorted(package.rglob("*.md")):
        rel = path.relative_to(package).as_posix()
        if ignored(rel):
            continue
        raw = read_text(path)
        docs.append((rel, path, raw, visible(raw)))
    fails = []
    for fact in facts:
        fact_id = fact["id"]
        sentences = sentence_list(fact)
        owners = set(fact.get("owners") or [])
        if fact_id in OPEN_IDS:
            pattern = OPEN_VALUE[fact_id]
            for rel, _path, _raw, text in docs:
                if pattern.search(text):
                    fails.append(f"OPEN_VALUE {fact_id} {rel}")
            continue
        for owner in sorted(owners):
            owner_path = package / owner
            if not owner_path.is_file():
                fails.append(f"OWNER_MISSING {fact_id} {owner}")
                continue
            text = visible(read_text(owner_path))
            if not all(contains(text, sentence) for sentence in sentences):
                fails.append(f"OWNER_DISAGREE {fact_id} {owner}")
        for rel, _path, _raw, text in docs:
            if rel in owners:
                continue
            if restates(fact_id, text, sentences):
                fails.append(f"RESTATE {fact_id} {rel}")
    fails.extend(cell_restate_fails(docs, facts))
    for rel, path, raw, _text in docs:
        for kind, detail in related_fails(path, raw):
            fails.append(f"{kind} {rel} {detail}")
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
    if not (package / "_schemas" / "fact-owners.json").is_file():
        ap.error("fact-owners.json is missing")
    fails = check(package)
    ok = not fails
    summary = f"SUMMARY fact_owner_check status={'PASS' if ok else 'FAIL'} fail_n={len(fails)}"
    if args.json:
        print(json.dumps(
            dict(tool="fact_owner_check", ok=ok, fail_n=len(fails), fails=fails, summary=summary),
            ensure_ascii=False,
        ))
    else:
        print(summary)
        if not args.summary_only:
            print("\n".join(fails))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(cli(main))
