#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract ephemeral values JSON from DEV-10/30 markdown SSOT. Does not invent facts.

md is SSOT; JSON is temporary for docs-refresh / render. Unknown / extra H2 sections
are ignored (not invented into schema). Em-dash placeholders (—) and empty cells
become empty strings / omitted kv keys.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

SEP = re.compile(r"^\|[-:| ]+\|\s*$")
H1 = re.compile(r"^#\s+DEV-(10|30)\s+[^\n—\-]*[—\-]\s*(.+?)\s*$")
H2 = re.compile(r"^##\s+(.+?)\s*$")


def is_blank(s: str) -> bool:
    return s is None or str(s).strip() in ("", "—", "–", "-", "…", "...")


def clean(s: str) -> str:
    s = (s or "").strip()
    if is_blank(s):
        return ""
    return s


def parse_tables_and_blocks(md: str):
    """Return list of (heading|None, kind, payload). kind: meta_table|kv|table|string|mermaid|none."""
    lines = md.splitlines()
    i = 0
    product = None
    # H1
    while i < len(lines) and not lines[i].startswith("# "):
        i += 1
    if i < len(lines):
        m = H1.match(lines[i])
        if m:
            product = m.group(2).strip()
        i += 1

    sections: list[tuple[str | None, str, object]] = []
    cur_h: str | None = None
    buf: list[str] = []

    def flush():
        nonlocal buf, cur_h
        if cur_h is None and not buf:
            return
        text = "\n".join(buf).strip()
        buf = []
        if not text and cur_h is None:
            return
        # try parse as table(s)
        tlines = [ln for ln in text.splitlines() if ln.strip()]
        if not tlines:
            sections.append((cur_h, "none", None))
            return
        # mermaid fence
        if "```mermaid" in text:
            m = re.search(r"```mermaid\s*\n(.*?)```", text, re.S)
            sections.append((cur_h, "mermaid", (m.group(1).strip() if m else "")))
            return
        # single table?
        if tlines[0].startswith("|"):
            rows = parse_md_table(tlines)
            if not rows:
                sections.append((cur_h, "string", text))
                return
            headers = rows[0]
            body = rows[1:]
            if headers == ["필드", "값"] or (len(headers) == 2 and headers[0] == "필드"):
                meta = {r[0]: clean(r[1]) for r in body if len(r) >= 2 and not is_blank(r[0])}
                sections.append((cur_h, "meta_table", meta))
            elif headers == ["구분", "내용"]:
                kv = {r[0]: clean(r[1]) for r in body if len(r) >= 2 and not is_blank(r[0]) and not is_blank(r[1])}
                sections.append((cur_h, "kv", kv))
            else:
                dicts = []
                for r in body:
                    d = {}
                    for hi, h in enumerate(headers):
                        d[h] = clean(r[hi]) if hi < len(r) else ""
                    # skip fully empty
                    if any(v for v in d.values()):
                        dicts.append(d)
                sections.append((cur_h, "table", {"columns": headers, "rows": dicts}))
            return
        # plain string under heading
        sections.append((cur_h, "string", text.strip()))

    while i < len(lines):
        ln = lines[i]
        hm = H2.match(ln)
        if hm:
            flush()
            cur_h = hm.group(1).strip()
            i += 1
            continue
        # leading meta table before any H2
        buf.append(ln)
        i += 1
    flush()
    return product, sections


def parse_md_table(tlines: list[str]) -> list[list[str]]:
    rows = []
    for ln in tlines:
        if not ln.strip().startswith("|"):
            break
        if SEP.match(ln.strip()):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        rows.append(cells)
    return rows


def map_dev10(product, sections) -> dict:
    values: dict = {"product": product or "", "meta": {}, "open": []}
    label_map = {
        "＊ 한 줄 소개": ("one_liner", "string"),
        "○ 왜 필요한가": ("why", "kv"),
        "＊ 누구를 위한가": ("audience", "kv"),
        "＊ 핵심 기능": ("features", "features"),
        "＊ 실행·설치": ("run", "kv"),
        "＊ 시스템 경계": ("boundary", "boundary"),
        "○ 성공·검증": ("success", "table"),
        "○ 관련 문서": ("related", "table"),
        "미결": ("open", "open"),
    }
    for h, kind, payload in sections:
        if h is None and kind == "meta_table":
            meta = dict(payload)
            meta.pop("코드", None)
            values["meta"] = {k: v for k, v in meta.items() if v}
            continue
        if h is None:
            continue
        # normalize heading: allow lock sections etc. only if in map
        key = None
        mode = None
        for lab, (k, m) in label_map.items():
            if h == lab or h.startswith(lab):
                key, mode = k, m
                break
        if key is None:
            continue  # extra H2 ignored — not invented
        if mode == "string" and kind in ("string", "none"):
            if kind == "string" and payload:
                values[key] = clean(payload.splitlines()[0]) if payload else ""
        elif mode == "kv" and kind == "kv":
            values[key] = payload
        elif mode == "features" and kind == "table":
            feats = []
            for r in payload["rows"]:
                text = r.get("사용자가 하는 일") or r.get("내용") or ""
                if text:
                    feats.append(text)
            values[key] = feats
        elif mode == "boundary" and kind == "table":
            # tolerate alt column names from real docs
            rows = []
            cols = payload["columns"]
            for r in payload["rows"]:
                item = r.get("하지 않는 것") or r.get("하지 않는 것 / 현재 상태") or (r.get(cols[0]) if cols else "")
                reason = r.get("이유") or r.get("설명") or (r.get(cols[1]) if len(cols) > 1 else "")
                if item or reason:
                    rows.append({"하지 않는 것": item, "이유": reason})
            values[key] = rows
        elif mode == "table" and kind == "table":
            values[key] = payload["rows"]
        elif mode == "open" and kind == "table":
            opens = []
            for r in payload["rows"]:
                iid, content = r.get("ID", ""), r.get("내용", "")
                if is_blank(content) or content == "없음" or iid == "—":
                    continue
                opens.append({"ID": iid or str(len(opens) + 1), "내용": content})
            values[key] = opens
    return values


def map_dev30(product, sections) -> dict:
    values: dict = {"product": product or "", "meta": {}, "open": []}
    label_map = {
        "＊ 한 줄 구조 요약": ("summary", "string"),
        "＊ 모듈/레이어": ("modules", "table"),
        "＊ 구조도 (Mermaid)": ("mermaid", "mermaid"),
        "＊ 의존 규칙": ("deps", "table"),
        "＊ 건드리기 위험 구역": ("danger", "table"),
        "○ 핵심 실행 흐름": ("flow", "table"),
        "○ 데이터 위치": ("data", "table"),
        "○ 관련 문서": ("related", "table"),
        "미결": ("open", "open"),
    }
    for h, kind, payload in sections:
        if h is None and kind == "meta_table":
            meta = dict(payload)
            meta.pop("코드", None)
            values["meta"] = {k: v for k, v in meta.items() if v}
            continue
        if h is None:
            continue
        key = mode = None
        for lab, (k, m) in label_map.items():
            if h == lab or h.startswith(lab):
                key, mode = k, m
                break
        if key is None:
            continue
        if mode == "string" and kind == "string":
            values[key] = clean(payload.splitlines()[0]) if payload else ""
        elif mode == "mermaid" and kind == "mermaid":
            values[key] = payload or ""
        elif mode == "table" and kind == "table":
            values[key] = payload["rows"]
        elif mode == "open" and kind == "table":
            opens = []
            for r in payload["rows"]:
                iid, content = r.get("ID", ""), r.get("내용", "")
                if is_blank(content) or content == "없음" or iid == "—":
                    continue
                opens.append({"ID": iid or str(len(opens) + 1), "내용": content})
            values[key] = opens
    return values


def detect_code(md: str, schema_hint: str | None) -> str:
    if schema_hint:
        return schema_hint
    m = re.search(r"^#\s+DEV-(10|30)\b", md, re.M)
    if m:
        return f"DEV-{m.group(1)}"
    raise SystemExit("cannot detect DEV-10/30; pass --code")


def extract(md: str, code: str) -> dict:
    product, sections = parse_tables_and_blocks(md)
    if code == "DEV-10":
        return map_dev10(product, sections)
    if code == "DEV-30":
        return map_dev30(product, sections)
    raise SystemExit(f"unsupported {code}")


def main() -> int:
    ap = argparse.ArgumentParser(description="md SSOT → ephemeral values JSON (DEV-10/30)")
    ap.add_argument("--md", required=True, help="path to DEV-10/30 markdown")
    ap.add_argument("--out", required=True, help="write values JSON here (ephemeral)")
    ap.add_argument("--code", choices=["DEV-10", "DEV-30"], help="override detection")
    ap.add_argument("--stdout", action="store_true", help="also print JSON")
    args = ap.parse_args()
    path = Path(args.md)
    md = path.read_text(encoding="utf-8")
    code = detect_code(md, args.code)
    values = extract(md, code)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(values, ensure_ascii=False, indent=2) + "\n"
    out.write_text(text, encoding="utf-8")
    print(str(out))
    if args.stdout:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
