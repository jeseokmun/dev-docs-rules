"""Lossless section edits for the supported DEV-10/30 value fields."""
from __future__ import annotations
import re
from docs_common import cells, escape_cell as esc, sections

FIELDS = {
    "DEV-10": {"one_liner": "＊ 한 줄 소개", "why": "○ 왜 필요한가", "audience": "＊ 누구를 위한가",
               "features": "＊ 핵심 기능", "run": "＊ 실행·설치", "boundary": "＊ 시스템 경계",
               "success": "○ 성공·검증", "related": "○ 관련 문서", "open": "미결"},
    "DEV-30": {"summary": "＊ 한 줄 구조 요약", "modules": "＊ 모듈/레이어", "mermaid": "＊ 구조도 (Mermaid)",
               "deps": "＊ 의존 규칙", "danger": "＊ 건드리기 위험 구역", "flow": "○ 핵심 실행 흐름",
               "data": "○ 데이터 위치", "related": "○ 관련 문서", "open": "미결"},
}


def validate_values(code, values, strict=True):
    if not isinstance(values, dict):
        raise ValueError("values must be an object")
    if set(values) - (set(FIELDS[code]) | {"product", "meta"}):
        raise ValueError("unsupported value fields")
    for key, value in values.items():
        if key in {"product", "one_liner", "summary", "mermaid"}:
            if not isinstance(value, str):
                raise ValueError("string required")
        elif key in {"meta", "why", "audience", "run"}:
            if not isinstance(value, dict) or any(not isinstance(v, str) for v in value.values()):
                raise ValueError("string mapping required")
            known = {"why": {"문제", "접근"}, "audience": {"사용자", "비사용자"},
                     "run": {"개발", "사용자", "환경"}}
            if strict and key in known and set(value) - known[key]:
                raise ValueError("unsupported mapping keys")
        else:
            if not isinstance(value, list):
                raise ValueError("row array required")
            for row in value:
                if key == "features" and isinstance(row, str):
                    continue
                if not isinstance(row, dict) or any(not isinstance(v, (str, int, float)) for v in row.values()):
                    raise ValueError("row objects required")


def refresh_text(original, rendered, code, patch):
    """Replace only explicitly patched sections; keep all other bytes as text."""
    blocks = sections(original)
    labels = [label for label, _ in blocks if label is not None]
    if len(labels) != len(set(labels)):
        raise ValueError("ambiguous duplicate sections")
    replacements = dict(sections(rendered))
    wanted = {FIELDS[code][k] for k in patch if k in FIELDS[code]}
    newline = "\r\n" if "\r\n" in original else "\n"
    out, seen = [], set()
    for label, raw in blocks:
        if label is None:
            if "product" in patch:
                title = f"# {code} {'개요서' if code == 'DEV-10' else '구조명세서'} — {esc(patch['product'])}"
                raw = re.sub(r"^# DEV-\d+ [^\r\n]*", lambda _: title, raw, count=1, flags=re.M)
            if "meta" in patch:
                pending = dict(patch["meta"])
                lines = []
                for line in raw.splitlines(keepends=True):
                    if line.strip().startswith("|"):
                        row = cells(line)
                        if len(row) == 2 and row[0] in pending:
                            line = "| " + esc(row[0]) + " | " + esc(pending.pop(row[0])) + " |" + newline
                    else:
                        bullet = re.match(r"^(-\s+\*\*([^:*]+):?\*\*:?\s*).+", line)
                        if bullet and bullet[2] in pending:
                            value = pending.pop(bullet[2]).replace("\r", " ").replace("\n", " ")
                            line = bullet[1] + value + newline
                    lines.append(line)
                if pending:
                    raise ValueError("cannot add unknown metadata keys during refresh")
                raw = "".join(lines)
        elif label in wanted:
            seen.add(label)
            replacement = replacements.get(label)
            if replacement is None:
                raise ValueError("patch removes required content; use explicit manual edit")
            raw = replacement.rstrip().replace("\n", newline) + newline * 2
        out.append(raw)
    for label in sorted(wanted - seen):
        if label not in replacements:
            raise ValueError("patch content cannot be rendered")
        out.append(newline + replacements[label].rstrip().replace("\n", newline) + newline)
    return "".join(out)
