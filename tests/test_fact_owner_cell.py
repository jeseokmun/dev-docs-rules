"""A non-owner table cell must not cite a fact id and repeat the owner's phrase."""
from __future__ import annotations
import json
from pathlib import Path
import sys
import tempfile
import unittest

PKG = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PKG / "_tools"))
import fact_owner_check as owners

OPEN = ("HC-REPO", "HC-DRIFT-VER", "HC-HASH", "HC-PKG", "HC-LEGAL", "HC-CHANNEL")
SENTENCE = "알파 규칙은 베타만 센다."


def package(owner_cell, other_cell):
    root = Path(tempfile.mkdtemp(prefix="사실칸 "))
    schema = root / "_schemas"
    schema.mkdir()
    facts = [{"id": item, "owners": [], "sentence": None} for item in OPEN]
    facts.append({"id": "HC-ALPHA", "owners": ["owner.md"], "sentence": SENTENCE})
    (schema / "fact-owners.json").write_text(
        json.dumps({"facts": facts}, ensure_ascii=False),
        encoding="utf-8",
    )
    (root / "owner.md").write_text(
        "| 칸 | 값 |\n|---|---|\n| 규칙 | " + owner_cell + " |\n",
        encoding="utf-8",
    )
    (root / "other.md").write_text(
        "| ID | 내용 |\n|---|---|\n| 1 | " + other_cell + " |\n",
        encoding="utf-8",
    )
    return root


class FactOwnerCell(unittest.TestCase):
    def test_package_has_no_cell_restate(self):
        self.assertEqual([item for item in owners.check(PKG) if item.startswith("CELL_RESTATE")], [])

    def test_owner_cell_may_keep_the_phrase(self):
        root = package(f"HC-ALPHA. {SENTENCE}", "HC-ALPHA (`owner.md`)")
        self.assertEqual(owners.cell_restate_fails(
            [(rel, root / rel, "", (root / rel).read_text(encoding="utf-8"))
             for rel in ("owner.md", "other.md")],
            owners.load_facts(root),
        ), [])

    def test_non_owner_cell_with_id_and_phrase_fails(self):
        root = package(SENTENCE, f"HC-ALPHA. {SENTENCE}")
        fails = owners.check(root)
        self.assertIn("CELL_RESTATE HC-ALPHA other.md", fails)
        self.assertFalse(any(item.endswith(" owner.md") and item.startswith("CELL_RESTATE") for item in fails))

    def test_id_without_the_phrase_passes(self):
        root = package(SENTENCE, "HC-ALPHA (`owner.md`)")
        self.assertEqual([item for item in owners.check(root) if item.startswith("CELL_RESTATE")], [])
