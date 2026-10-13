"""A template must not tell the writer to drop a section because a value is unknown."""
from __future__ import annotations
from pathlib import Path
import sys
import tempfile
import unittest

PKG = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PKG / "_tools"))
import template_unknown_check as unknown


def package_with(name, text):
    root = Path(tempfile.mkdtemp(prefix="양식미지 "))
    templates = root / "_templates"
    templates.mkdir()
    (templates / name).write_text(text, encoding="utf-8")
    return root


class TemplateUnknown(unittest.TestCase):
    def test_package_templates_pass(self):
        self.assertEqual(unknown.check(PKG), [])

    def test_delete_section_when_unknown_fails(self):
        root = package_with("DEV-99.md", "값을 모르면 절을 지운다.\n")
        fails = unknown.check(root)
        self.assertTrue(any("HIDE_UNKNOWN DEV-99.md" in item for item in fails))

    def test_labeled_placeholder_passes(self):
        text = (
            "값을 모르면 그 자리표시 행은 두지 않는다. "
            "미결 내용에 `없는 사실:`과 `다음 행동:`을 적는다.\n"
        )
        self.assertEqual(unknown.check(package_with("DEV-99.md", text)), [])

    def test_lint_warning_about_required_sections_passes(self):
        text = (
            "미결 표의 내용에는 `없는 사실:`과 `다음 행동:`을 적는다. "
            "필수 절을 지우거나 자리표시만 남기면 lint는 실패한다.\n"
        )
        self.assertEqual(unknown.check(package_with("DEV-99.md", text)), [])

    def test_known_absence_passes(self):
        text = "화면 이동이 없으면 이 절을 지운다.\n"
        self.assertEqual(unknown.check(package_with("DEV-99.md", text)), [])

    def test_neighbor_sentence_does_not_bleed(self):
        text = (
            "날짜를 모르면 날짜를 지어 넣지 않고 미결에 적는다. "
            "선언이 없으면 절을 빼거나, 아직 없다는 문장을 적는다.\n"
        )
        self.assertEqual(unknown.check(package_with("DEV-99.md", text)), [])

    def test_generator_note_passes(self):
        text = "생성기는 줄바꿈이 2개 미만이면 구조도 절을 빼고 미결로 보낸다.\n"
        self.assertEqual(unknown.check(package_with("DEV-99.md", text)), [])
