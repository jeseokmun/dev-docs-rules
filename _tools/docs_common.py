"""Shared UTF-8 I/O, Markdown parsing and CLI error handling (stdlib only)."""
from __future__ import annotations
import json
import os
from pathlib import Path
import re
import subprocess
import stat
import sys
import tempfile

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")


def cli(main):
    try:
        return main()
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print(f"error: {type(exc).__name__}; check input paths, UTF-8 and JSON structure", file=sys.stderr)
        return 2


def read_text(path):
    return Path(path).read_text(encoding="utf-8-sig")


def load_object(path):
    value = json.loads(read_text(path))
    if not isinstance(value, dict):
        raise ValueError("JSON object required")
    return value


def escape_cell(value):
    text = str(value).replace("\r", " ").replace("\n", " ").replace("|", "\\|").strip() if value is not None else ""
    return text or "—"


def run(command):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    return subprocess.run(command, capture_output=True, text=True,
                          encoding="utf-8", env=env, timeout=60)


def atomic_write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="",
                                         dir=path.parent, delete=False) as stream:
            temp = Path(stream.name)
            stream.write(text)
        if path.exists():
            os.chmod(temp, stat.S_IMODE(path.stat().st_mode))
        os.replace(temp, path)
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)


def sections(text):
    """Return (H2 label or None, raw block); ignore headings inside fences."""
    blocks, label, buf, fence, length = [], None, [], None, 0
    for line in text.splitlines(keepends=True):
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line.rstrip())
        if match:
            marker = match[1]
            if fence is None:
                fence, length = marker[0], len(marker)
            elif marker[0] == fence and len(marker) >= length and not match[2].strip():
                fence = None
        heading = re.match(r"^##\s+(.+?)\s*$", line) if fence is None else None
        if heading:
            blocks.append((label, "".join(buf)))
            label, buf = heading[1], []
        buf.append(line)
    blocks.append((label, "".join(buf)))
    return blocks


def body(block):
    return block.split("\n", 1)[1] if block.startswith("## ") and "\n" in block else block


def cells(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"):
        line = line[:-1]
    return [part.strip().replace(r"\|", "|") for part in re.split(r"(?<!\\)\|", line)]


def tables(text):
    """Yield (headers, rows); escape cell pipes as \\|, also in inline code."""
    lines, i, fence = text.splitlines(), 0, None
    while i < len(lines):
        line = lines[i].strip()
        marker = re.match(r"^(`{3,}|~{3,})", line)
        if marker:
            fence = None if fence == marker[1][0] else marker[1][0]
        if fence is None and line.startswith("|") and i + 1 < len(lines):
            separator = cells(lines[i + 1])
            if separator and all(re.fullmatch(r":?-{3,}:?", c) for c in separator):
                headers, rows = cells(line), []
                i += 2
                while i < len(lines) and lines[i].strip().startswith("|"):
                    rows.append(cells(lines[i]))
                    i += 1
                yield headers, rows
                continue
        i += 1


def placeholder(value):
    value = str(value).strip().strip("`_*").strip()
    return (not value or value.casefold() in {"—", "–", "-", "…", "...", "tbd", "todo",
            "tbd tbd", "lorem ipsum", "yyyy-mm-dd"} or
            bool(re.fullmatch(r"\{[^{}]+\}", value)))


def config(root):
    path = Path(root) / "DOC-CONFIG.md"
    result = {"language": "ko", "required_profile": "light", "statuses": "draft, active, deprecated"}
    if path.is_file():
        for key, value in re.findall(r"^-\s+\*\*(\w+):\*\*\s*(.+)$", read_text(path), re.M):
            result[key] = value.strip()
    if result["required_profile"] not in {"light", "full"}:
        raise ValueError("unknown required_profile")
    return result
