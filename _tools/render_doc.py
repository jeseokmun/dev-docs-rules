#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render ephemeral values JSON + schema → markdown. Does not invent facts."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

def esc(s):
    s = str(s).replace("\n", " ").strip() if s is not None else ""
    return s if s else "—"

def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        if isinstance(r, dict):
            cells = [esc(r.get(h, "")) for h in headers]
        elif isinstance(r, (list, tuple)):
            cells = [esc(r[i] if i < len(r) else "") for i, _ in enumerate(headers)]
        else:
            cells = [esc("") for _ in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)

def kv_rows(keys, data: dict):
    rows = []
    for k in keys:
        v = data.get(k, "")
        if v == "" or v is None:
            continue
        rows.append({"구분": k, "내용": v})
    if not rows:
        return None
    return table(["구분", "내용"], rows)

def render_dev10(schema, values):
    meta = values.get("meta", {})
    open_items = list(values.get("open", []) or [])
    parts = [f"# DEV-10 개요서 — {esc(values.get('product', '{제품}'))}", ""]
    parts.append(table(["필드", "값"], [
        {"필드": "상태", "값": meta.get("상태", "draft")},
        {"필드": "코드", "값": "DEV-10"},
        {"필드": "마지막 갱신", "값": meta.get("마지막 갱신", "YYYY-MM-DD")},
        {"필드": "범위", "값": meta.get("범위", "…")},
        {"필드": "비범위", "값": meta.get("비범위", "…")},
    ]))
    # required
    def need(field_id, label, block):
        nonlocal open_items
        if block:
            parts.extend(["", f"## {label}", block])
        else:
            open_items.append({"ID": str(len(open_items)+1), "내용": f"{label} 미기입"})

    one = values.get("one_liner")
    need("one_liner", "＊ 한 줄 소개", esc(one) if one else None)

    why = values.get("why")
    if why:
        b = kv_rows(["문제", "접근"], why)
        if b:
            parts.extend(["", "## ○ 왜 필요한가", b])

    aud = values.get("audience") or {}
    need("audience", "＊ 누구를 위한가", kv_rows(["사용자", "비사용자"], aud))

    feats = values.get("features") or []
    if len(feats) >= 3:
        rows = []
        for i, f in enumerate(feats, 1):
            if isinstance(f, dict):
                rows.append({"#": str(f.get("#", i)), "사용자가 하는 일": f.get("사용자가 하는 일", f.get("text", ""))})
            else:
                rows.append({"#": str(i), "사용자가 하는 일": f})
        need("features", "＊ 핵심 기능", table(["#", "사용자가 하는 일"], rows))
    else:
        need("features", "＊ 핵심 기능", None)

    run = values.get("run") or {}
    need("run", "＊ 실행·설치", kv_rows(["개발", "사용자", "환경"], run) if any(run.get(k) for k in ["개발","사용자","환경"]) else None)

    bound = values.get("boundary") or []
    if len(bound) >= 2:
        rows = [{"하지 않는 것": b.get("하지 않는 것", b.get("item","")), "이유": b.get("이유", b.get("reason",""))} for b in bound]
        need("boundary", "＊ 시스템 경계", table(["하지 않는 것", "이유"], rows))
    else:
        need("boundary", "＊ 시스템 경계", None)

    succ = values.get("success") or []
    if succ:
        rows = [{"성공 모습": s.get("성공 모습",""), "검증 방법": s.get("검증 방법","")} for s in succ]
        parts.extend(["", "## ○ 성공·검증", table(["성공 모습", "검증 방법"], rows)])

    rel = values.get("related") or []
    if rel:
        rows = [{"코드": r.get("코드",""), "경로": r.get("경로","")} for r in rel]
        parts.extend(["", "## ○ 관련 문서", table(["코드", "경로"], rows)])

    parts.extend(["", "## 미결", table(["ID", "내용"], open_items or [{"ID": "—", "내용": "없음"}])])
    return "\n".join(parts) + "\n"

def render_dev30(schema, values):
    meta = values.get("meta", {})
    open_items = list(values.get("open", []) or [])
    parts = [f"# DEV-30 구조명세서 — {esc(values.get('product', '{제품}'))}", ""]
    parts.append(table(["필드", "값"], [
        {"필드": "상태", "값": meta.get("상태", "draft")},
        {"필드": "코드", "값": "DEV-30"},
        {"필드": "마지막 갱신", "값": meta.get("마지막 갱신", "YYYY-MM-DD")},
        {"필드": "범위", "값": meta.get("범위", "…")},
        {"필드": "비범위", "값": meta.get("비범위", "…")},
    ]))
    def need(label, block):
        nonlocal open_items
        if block:
            parts.extend(["", f"## {label}", block])
        else:
            open_items.append({"ID": str(len(open_items)+1), "내용": f"{label} 미기입"})

    need("＊ 한 줄 구조 요약", esc(values["summary"]) if values.get("summary") else None)

    mods = values.get("modules") or []
    if len(mods) >= 3:
        rows = [{"모듈": m.get("모듈",""), "책임": m.get("책임",""), "비고": m.get("비고","")} for m in mods]
        need("＊ 모듈/레이어", table(["모듈", "책임", "비고"], rows))
    else:
        need("＊ 모듈/레이어", None)

    mm = values.get("mermaid")
    if mm and mm.count("\n") >= 2:
        need("＊ 구조도 (Mermaid)", "```mermaid\n" + mm.strip() + "\n```")
    else:
        need("＊ 구조도 (Mermaid)", None)

    deps = values.get("deps") or []
    if len(deps) >= 2:
        rows = [{"방향": d.get("방향",""), "허용?": d.get("허용?",""), "설명": d.get("설명","")} for d in deps]
        need("＊ 의존 규칙", table(["방향", "허용?", "설명"], rows))
    else:
        need("＊ 의존 규칙", None)

    dang = values.get("danger") or []
    if dang:
        rows = [{"모듈": d.get("모듈",""), "이유": d.get("이유",""), "경로(□)": d.get("경로(□)", d.get("경로",""))} for d in dang]
        need("＊ 건드리기 위험 구역", table(["모듈", "이유", "경로(□)"], rows))
    else:
        need("＊ 건드리기 위험 구역", None)

    flow = values.get("flow") or []
    if flow:
        rows = [{"단계": f.get("단계",""), "행위자": f.get("행위자",""), "행동": f.get("행동","")} for f in flow]
        parts.extend(["", "## ○ 핵심 실행 흐름", table(["단계", "행위자", "행동"], rows)])

    data = values.get("data") or []
    if data:
        rows = [{"데이터": d.get("데이터",""), "위치": d.get("위치","")} for d in data]
        parts.extend(["", "## ○ 데이터 위치", table(["데이터", "위치"], rows)])

    rel = values.get("related") or []
    if rel:
        rows = [{"코드": r.get("코드",""), "경로": r.get("경로","")} for r in rel]
        parts.extend(["", "## ○ 관련 문서", table(["코드", "경로"], rows)])

    parts.extend(["", "## 미결", table(["ID", "내용"], open_items or [{"ID": "—", "내용": "없음"}])])
    return "\n".join(parts) + "\n"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True)
    ap.add_argument("--values", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
    values = json.loads(Path(args.values).read_text(encoding="utf-8"))
    code = schema.get("code")
    if code == "DEV-10":
        md = render_dev10(schema, values)
    elif code == "DEV-30":
        md = render_dev30(schema, values)
    else:
        print("unsupported", code, file=sys.stderr)
        return 2
    Path(args.out).write_text(md, encoding="utf-8")
    print(args.out)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
