#!/usr/bin/env python3
"""Validate document bodies and profile presence using the bundled catalog."""
from __future__ import annotations
import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys

from docs_common import body, cli, config, load_object, placeholder, read_text, run, sections, tables

SECRET = re.compile(r"""(?:api[_-]?key|password|secret|token)\s*[:=]\s*["']?[^\s"'|]{8,}|sk-[A-Za-z0-9_-]{10,}|Bearer\s+[A-Za-z0-9._-]{12,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----""", re.I)
PKG = Path(__file__).resolve().parents[1]
# A proposed ADR may mention acceptance only as something still in the future.
NOT_YET_ACCEPTED = re.compile(r"아니다|아님|아직|뒤에만|올린다|올리기|두지\s*않|후보")


def decision_sentences(text):
    return [part.strip() for part in re.split(r"[.\n]+", text) if part.strip()]


def claims_accepted_now(text):
    for sent in decision_sentences(text):
        if re.search(r"(?<![A-Za-z])accepted(?![A-Za-z])", sent, re.I) or "채택" in sent:
            if NOT_YET_ACCEPTED.search(sent):
                continue
            return True
    return False


def claims_still_proposed(text):
    for sent in decision_sentences(text):
        if re.search(r"accepted(?:가|는)\s*아니다", sent):
            return True
        if re.search(r"결정 상태는 proposed", sent):
            return True
        if re.search(r"아직\s*proposed|proposed로\s*둔다", sent):
            return True
    return False


def longest_common_end(left, right):
    best = end_left = end_right = 0
    prev = [0] * (len(right) + 1)
    for i, ca in enumerate(left, 1):
        cur = [0] * (len(right) + 1)
        for j, cb in enumerate(right, 1):
            if ca == cb:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best, end_left, end_right = cur[j], i, j
        prev = cur
    return best, end_left, end_right


def fact_guess_cue(text, end):
    window = text[max(0, end - 2):end + 8]
    if re.search(r"아니|없|않|못", window):
        return "neg"
    if re.search(r"있|이다|된다", window):
        return "pos"
    return None


QUANTITY = re.compile(r"\d+(?:\.\d+)?\s*(?:초|ms|밀리초|%|건|MB|KB)")


def quantity_tokens(text):
    return {re.sub(r"\s+", "", token) for token in QUANTITY.findall(text)}


def goal_copy(goal_text, scenario_text):
    """A scenario measure must not repeat a number from the goal column."""
    found = list(tables(goal_text))
    if not found or "목표" not in found[0][0]:
        return False
    index = found[0][0].index("목표")
    goals = set()
    for row in found[0][1]:
        if index < len(row):
            goals.update(quantity_tokens(row[index]))
    if not goals:
        return False
    scenario = list(tables(scenario_text))
    if not scenario or "측정" not in scenario[0][0]:
        return False
    measure = scenario[0][0].index("측정")
    for row in scenario[0][1]:
        if measure < len(row) and quantity_tokens(row[measure]) & goals:
            return True
    return False


def fact_guess_conflict(fact, guess):
    """Same span of 4+ characters, then opposite polarity or a different number."""
    length, end_fact, end_guess = longest_common_end(fact, guess)
    if length < 4:
        return False
    fact_num = re.match(r"\s*(\d+)", fact[end_fact:])
    guess_num = re.match(r"\s*(\d+)", guess[end_guess:])
    if fact_num and guess_num and fact_num.group(1) != guess_num.group(1):
        return True
    fact_cue = fact_guess_cue(fact, end_fact)
    guess_cue = fact_guess_cue(guess, end_guess)
    return bool(fact_cue and guess_cue and fact_cue != guess_cue)


def check_file(path, schema, settings=None):
    path = Path(path)
    if not path.is_file():
        return [f"MISSING {path.name}"]
    settings = settings or {"statuses": "draft, active, deprecated"}
    text = read_text(path)
    blocks = sections(text)
    labels = [label for label, _ in blocks if label is not None]
    fails = []
    for label in set(labels):
        if labels.count(label) > 1:
            fails.append(f"DUPLICATE_SECTION {path.name}")
    contents = {label: body(raw).strip() for label, raw in blocks if label is not None}
    if SECRET.search(text):
        fails.append(f"SECRET_LIKE {path.name}")
    meta_tables = list(tables(blocks[0][1]))
    meta = dict(meta_tables[0][1]) if meta_tables and all(len(r) == 2 for r in meta_tables[0][1]) else {}
    # Constitution §4 also permits a bullet header.
    meta.update(dict(re.findall(r"^-\s+\*\*([^:*]+):?\*\*:?\s*(.+?)\s*$", blocks[0][1], re.M)))
    for key in schema.get("meta", []):
        if key not in meta or placeholder(meta[key]):
            fails.append(f"META_REQUIRED {path.name}: {key}")
    if meta.get("코드") != schema["code"]:
        fails.append(f"META_CODE {path.name}")
    if not re.search(r"^#\s+" + re.escape(schema["code"]) + r"\b", text, re.M):
        fails.append(f"TITLE_CODE {path.name}")
    if meta.get("상태") not in [s.strip() for s in settings["statuses"].split(",")]:
        fails.append(f"META_STATUS {path.name}")
    try:
        value = meta.get("마지막 갱신", "")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError("expected YYYY-MM-DD")
        date.fromisoformat(value)
    except ValueError:
        fails.append(f"META_DATE {path.name}")
    for field in schema.get("required", []):
        label = field["label"]
        if label not in contents:
            fails.append(f"MISSING_SECTION {path.name}: {label}")
            continue
        content = re.sub(r"<!--.*?-->", "", contents[label], flags=re.S).strip()
        if placeholder(content):
            fails.append(f"EMPTY_SECTION {path.name}: {label}")
            continue
        kind = field["type"]
        if kind == "string":
            if len(content) < field.get("min", 1):
                fails.append(f"MIN_LENGTH {path.name}: {label}")
        elif kind == "mermaid":
            match = re.search(r"```mermaid\s*\n(.*?)```", content, re.S)
            # Node syntax/count and diagram meaning require a Mermaid renderer or review.
            if not match or placeholder(match[1]):
                fails.append(f"MISSING_MERMAID {path.name}: {label}")
        else:
            found = list(tables(content))
            if not found:
                fails.append(f"MISSING_TABLE {path.name}: {label}")
                continue
            headers, rows = found[0]
            expected = ["구분", "내용"] if kind == "kv_rows" else field.get("columns", [])
            if headers != expected:
                fails.append(f"TABLE_COLUMNS {path.name}: {label}")
            if len(rows) < field.get("min_rows", 1):
                fails.append(f"MIN_ROWS {path.name}: {label}")
            for row in rows:
                if len(row) != len(headers):
                    fails.append(f"TABLE_WIDTH {path.name}: {label}")
                elif any(placeholder(c) for h, c in zip(headers, row) if h != "비고" and "□" not in h):
                    fails.append(f"FAKEFILL {path.name}: {label}")
            if kind == "kv_rows":
                keys = {r[0] for r in rows if r}
                if keys - set(field.get("keys", [])):
                    fails.append(f"UNKNOWN_KEYS {path.name}: {label}")
                if field.get("min_rows", 1) >= len(field.get("keys", [])):
                    if not set(field.get("keys", [])) <= keys:
                        fails.append(f"MISSING_KEYS {path.name}: {label}")
            if headers == expected:
                for name, words in (field.get("column_keys") or {}).items():
                    if name not in headers:
                        continue
                    index = headers.index(name)
                    for row in rows:
                        if index < len(row) and row[index] not in words:
                            fails.append(f"COLUMN_VALUE {path.name}: {label}")
    if schema.get("code") == "DEV-50":
        claim = "\n".join(contents.get(label, "") for label in ("＊ 제목", "＊ 결정"))
        state = meta.get("결정 상태", "").strip()
        if state == "proposed" and claims_accepted_now(claim):
            fails.append(f"STATUS_CONFLICT {path.name}")
        if state == "accepted" and claims_still_proposed(claim):
            fails.append(f"STATUS_CONFLICT {path.name}")
    if schema.get("code") == "DEV-62":
        facts, guesses = [], []
        found = list(tables(contents.get("＊ 사실 / 추측", "")))
        if found and found[0][0][:2] == ["종류", "내용"]:
            for row in found[0][1]:
                if len(row) < 2:
                    continue
                if row[0].strip() == "사실":
                    facts.append(row[1])
                elif row[0].strip() == "추측":
                    guesses.append(row[1])
        case = list(tables(contents.get("＊ 사례", "")))
        if case and "원인" in case[0][0]:
            index = case[0][0].index("원인")
            for row in case[0][1]:
                if index >= len(row):
                    continue
                cause = row[index].strip()
                if cause.startswith("추측:") or cause.startswith("추측："):
                    guesses.append(cause)
                else:
                    facts.append(cause)
        if any(fact_guess_conflict(fact, guess) for fact in facts for guess in guesses):
            fails.append(f"FACT_GUESS {path.name}")
    if schema.get("code") == "DEV-68" and goal_copy(contents.get("＊ 목표 지표", ""), contents.get("○ 품질 시나리오", "")):
        fails.append(f"GOAL_COPY {path.name}")
    for field in schema.get("optional", []):
        allowed = field.get("column_keys")
        if not allowed or field["label"] not in contents:
            continue
        found = list(tables(contents[field["label"]]))
        if not found:
            fails.append(f"MISSING_TABLE {path.name}: {field['label']}")
            continue
        headers, rows = found[0]
        expected = field.get("columns", [])
        if headers != expected:
            fails.append(f"TABLE_COLUMNS {path.name}: {field['label']}")
            continue
        for name, words in allowed.items():
            if name not in headers:
                fails.append(f"TABLE_COLUMNS {path.name}: {field['label']}")
                continue
            index = headers.index(name)
            for row in rows:
                if index >= len(row) or row[index] not in words:
                    fails.append(f"COLUMN_VALUE {path.name}: {field['label']}")
    for headers, rows in tables(text):
        for row in rows:
            if len(row) != len(headers):
                fails.append(f"TABLE_WIDTH {path.name}")
            elif any(not c for h, c in zip(headers, row) if h != "비고" and "□" not in h):
                fails.append(f"EMPTY_CELL {path.name}")
    return list(dict.fromkeys(fails))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("docs_root", type=Path)
    ap.add_argument("--package", type=Path, default=PKG)
    ap.add_argument("--skip-schema-sync", action="store_true")
    ap.add_argument("--only", help="check one catalog code; skip presence of other types")
    ap.add_argument("--profile", choices=["light", "full"], help="override DOC-CONFIG profile")
    output = ap.add_mutually_exclusive_group()
    output.add_argument("--json", action="store_true")
    output.add_argument("--summary-only", action="store_true")
    args = ap.parse_args()
    if not args.docs_root.is_dir():
        ap.error("docs_root must be an existing directory")
    schemas = {p.stem.split(".")[0]: load_object(p) for p in (args.package / "_schemas").glob("DEV-*.schema.json")}
    if not schemas:
        ap.error("package has no schemas")
    if args.only and args.only not in schemas:
        ap.error("--only must name a catalog code")
    settings = config(args.docs_root)
    profile = args.profile or settings["required_profile"]
    required = {args.only} if args.only else {"DEV-10", "DEV-30"}
    if not args.only and profile == "full":
        required |= {"DEV-20", "DEV-50", "DEV-90"}
    fails, checked = [], []
    for code, schema in sorted(schemas.items()):
        if args.only and code != args.only:
            continue
        title = schema["title"]
        folder = args.docs_root / f"{code}-{title}"
        files = [args.docs_root / f"{code}-{title}.md"] if schema["single_file"] else sorted(folder.glob(f"{code}-*.md"))
        files = [p for p in files if p.is_file()]
        if files:
            checked.append(code)
            for path in files:
                fails.extend(check_file(path, schema, settings))
        elif code in required:
            index = folder / "INDEX.md"
            if code == "DEV-50" and index.is_file() and re.search(r"^(?:[-*]\s+)?결정 없음[.!]?$", read_text(index), re.M):
                checked.append(code)
            else:
                fails.append(f"MISSING {code}")
    if not args.only:
        for path in args.docs_root.rglob("DEV-*.md"):
            rel = path.relative_to(args.docs_root)
            if any(p.startswith("_") or p == "archive" for p in rel.parts[:-1]) or path.name.startswith("DEV-CONSTITUTION"):
                continue
            match = re.match(r"^(DEV-\d+)-", path.name)
            code = match[1] if match else ""
            schema = schemas.get(code)
            if not schema:
                fails.append(f"UNKNOWN_CODE {rel.as_posix()}")
            elif (schema["single_file"] and rel.as_posix() != f"{code}-{schema['title']}.md") or (not schema["single_file"] and (len(rel.parts) != 2 or rel.parts[0] != f"{code}-{schema['title']}")):
                fails.append(f"DOC_PATH {rel.as_posix()}")
    sync_line = ""
    if not args.skip_schema_sync:
        r = run([sys.executable, str(Path(__file__).with_name("schema_sync_check.py")), "--package", str(args.package), "--summary-only"])
        sync_line = r.stdout.strip()
        if r.returncode:
            fails.append("SCHEMA_SYNC " + sync_line)
    ok = not fails
    summary = f"SUMMARY docs_lint status={'PASS' if ok else 'FAIL'} docs_root={args.docs_root} profile={profile} types={','.join(checked)} fail_n={len(fails)}"
    payload = dict(tool="docs_lint", ok=ok, docs_root=str(args.docs_root), profile=profile, types=checked, fail_n=len(fails), fails=fails, schema_sync=sync_line, summary=summary)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(summary)
        if not args.summary_only:
            for fail in fails:
                print(fail)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(cli(main))
