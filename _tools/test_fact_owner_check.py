"""Fixture checks for fact ownership. Does not run the package regression."""
from __future__ import annotations
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parent
PKG = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import fact_owner_check as owners

PLATFORM = "Android 8.0+ · Flutter 3.22+ · Dart 3.4+"
OPENS = ("HC-REPO", "HC-DRIFT-VER", "HC-HASH", "HC-PKG", "HC-LEGAL", "HC-CHANNEL")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class FactOwners(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="사실주인 ")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        write(self.root / "owner-a.md", f"환경은 {PLATFORM} 이다.\n")
        write(self.root / "owner-b.md", f"같은 문장 {PLATFORM} 을 적는다.\n")
        write(self.root / "cited.md", "있다\n")
        write(self.root / "other.md", "\n".join([
            "# DEV-20 요구",
            "",
            "하한은 `HC-PLATFORM` (`owner-a.md`)이다.",
            "",
            "## ○ 관련 문서",
            "| 코드 | 경로 |",
            "|---|---|",
            "| DEV-10 | `cited.md` |",
            "",
        ]))
        self.registry(self.platform_fact())

    def registry(self, *extra):
        facts = [{"id": item, "owners": [], "sentence": None} for item in OPENS]
        facts.extend(extra)
        write(self.root / "_schemas" / "fact-owners.json",
              json.dumps({"facts": facts}, ensure_ascii=False, indent=2))

    def platform_fact(self):
        return {"id": "HC-PLATFORM", "owners": ["owner-a.md", "owner-b.md"], "sentence": PLATFORM}

    def codes(self):
        return [item.split()[0] for item in owners.check(self.root)]

    def test_citation_without_the_sentence_passes(self):
        self.assertEqual(owners.check(self.root), [])

    def test_exact_sentence_outside_owner_fails(self):
        write(self.root / "other.md", self.root.joinpath("other.md").read_text(encoding="utf-8") + PLATFORM)
        self.assertIn("RESTATE HC-PLATFORM other.md", owners.check(self.root))

    def test_different_typing_fails(self):
        write(self.root / "other.md", "하한은 Android 8.0+, Flutter 3.22+, Dart 3.4+다.\n")
        self.assertIn("RESTATE HC-PLATFORM other.md", owners.check(self.root))

    def test_owners_that_differ_fail(self):
        write(self.root / "owner-b.md", "하한은 Android 8.0+, Flutter 3.22+, Dart 3.4+다.\n")
        self.assertIn("OWNER_DISAGREE HC-PLATFORM owner-b.md", owners.check(self.root))

    def test_missing_owner_file_fails(self):
        self.registry({"id": "HC-PLATFORM", "owners": ["owner-a.md", "없는.md"], "sentence": PLATFORM})
        self.assertIn("OWNER_MISSING HC-PLATFORM 없는.md", owners.check(self.root))

    def test_streak_paraphrase_fails(self):
        sentence = "streak는 한 습관의 CheckIn.localDate만 센다. 하루가 비면 그 앞에서 끊긴다."
        self.registry({"id": "HC-STREAK", "owners": ["owner-a.md"], "sentence": sentence})
        write(self.root / "owner-a.md", sentence + "\n")
        write(self.root / "other.md", "계산은 하루가 비면 끊긴다.\n")
        self.assertIn("RESTATE HC-STREAK other.md", owners.check(self.root))

    def test_drift_words_outside_owner_fail(self):
        sentence = "| 결정 상태 | proposed |"
        self.registry({"id": "HC-DRIFT-STATE", "owners": ["owner-a.md"], "sentence": sentence})
        write(self.root / "owner-a.md", sentence + "\n")
        write(self.root / "other.md", "로컬 DB는 drift proposed이지 accepted가 아니다.\n")
        fails = owners.check(self.root)
        self.assertIn("RESTATE HC-DRIFT-STATE other.md", fails)

    def test_flag_default_fails_and_name_alone_passes(self):
        sentence = "| weekly_summary | on | 전체 사용자 | 제거 |"
        self.registry({"id": "HC-FLAG", "owners": ["owner-a.md"], "sentence": sentence})
        write(self.root / "owner-a.md", sentence + "\n")
        write(self.root / "other.md", "플래그 이름은 weekly_summary 이다.\n")
        self.assertEqual(owners.check(self.root), [])
        write(self.root / "other.md", "weekly_summary 기본은 on이다.\n")
        self.assertIn("RESTATE HC-FLAG other.md", owners.check(self.root))

    def test_midnight_guess_outside_owner_fails(self):
        sentence = "날짜를 자르는 시각은 기기 로컬 자정으로 둔다."
        self.registry({"id": "HC-MIDNIGHT", "owners": ["owner-a.md"], "sentence": sentence})
        write(self.root / "owner-a.md", sentence + "\n")
        write(self.root / "other.md", "기준은 `HC-MIDNIGHT` (`owner-a.md`)이다.\n")
        self.assertEqual(owners.check(self.root), [])
        write(self.root / "other.md", "날짜 경계는 일단 기기 로컬 자정이다.\n")
        self.assertIn("RESTATE HC-MIDNIGHT other.md", owners.check(self.root))

    def test_python_rule_and_exit_codes(self):
        self.registry(
            {"id": "TOOL-PY", "owners": ["README.md"],
             "sentence": "Windows에서 `python3`가 없으면 그 자리만 `python`으로 바꾼다."},
            {"id": "TOOL-EXIT", "owners": ["_tools/README.md"],
             "sentence": "종료 코드: **0** 성공, **1** 검사 실패, **2** 입력·I/O 오류."},
        )
        write(self.root / "README.md", "Windows에서 `python3`가 없으면 그 자리만 `python`으로 바꾼다.\n")
        write(self.root / "_tools/README.md", "종료 코드: **0** 성공, **1** 검사 실패, **2** 입력·I/O 오류.\n")
        write(self.root / "other.md", "명령 이름의 구분은 `TOOL-PY` (`README.md`)가 맡는다.\n")
        self.assertEqual(owners.check(self.root), [])
        write(self.root / "other.md", "환경에 따라 `python` 대신 `python3`를 쓴다.\n")
        self.assertIn("RESTATE TOOL-PY other.md", owners.check(self.root))
        write(self.root / "other.md", "exit 0은 통과, 1은 검사 실패, 2는 입력 오류다.\n")
        self.assertIn("RESTATE TOOL-EXIT other.md", owners.check(self.root))

    def test_open_value_detected_and_placeholder_allowed(self):
        cases = {
            "HC-REPO": "git clone https://github.com/acme/habit.git\n",
            "HC-DRIFT-VER": "핀은 drift 2.18.0 이다.\n",
            "HC-HASH": "sha256:" + "ab" * 20 + "\n",
            "HC-PKG": "applicationId=com.habit.check\n",
            "HC-LEGAL": "라이선스 칸은 MIT 이다.\n",
            "HC-CHANNEL": "알림은 https://discord.gg/habit 이다.\n",
        }
        for fact_id, text in cases.items():
            with self.subTest(fact=fact_id):
                write(self.root / "other.md", text)
                self.assertIn(f"OPEN_VALUE {fact_id} other.md", owners.check(self.root))
        write(self.root / "other.md", "\n".join([
            "git clone HC-REPO",
            "git clone <repo-url>",
            "목록은 https://github.com/jeseokmun/dev-docs-rules/actions 이다.",
            "drift 버전은 없다.",
            "applicationId는 확인 전에 적지 않는다.",
            "식별자는 미확인이다.",
            "채널 이름은 비어 있다.",
        ]) + "\n")
        self.assertEqual([item for item in owners.check(self.root) if item.startswith("OPEN_VALUE")], [])

    def test_filled_open_sentence_is_rejected(self):
        facts = json.loads((self.root / "_schemas" / "fact-owners.json").read_text(encoding="utf-8"))
        facts["facts"][0]["sentence"] = "https://github.com/acme/habit"
        write(self.root / "_schemas" / "fact-owners.json", json.dumps(facts))
        with self.assertRaises(ValueError):
            owners.check(self.root)

    def test_related_table_omission_and_missing_path(self):
        write(self.root / "other.md", "\n".join([
            "# DEV-20 요구",
            "",
            "화면은 DEV-25, 저장은 DEV-35.",
            "",
            "## ○ 관련 문서",
            "| 코드 | 경로 |",
            "|---|---|",
            "| DEV-25 | `cited.md` |",
            "| DEV-40 | `없는.md` |",
            "",
        ]))
        fails = owners.check(self.root)
        self.assertIn("RELATED_OMIT other.md DEV-35", fails)
        self.assertIn("RELATED_MISSING other.md 없는.md", fails)
        self.assertNotIn("RELATED_OMIT other.md DEV-20", fails)
        self.assertNotIn("RELATED_OMIT other.md DEV-25", fails)

    def test_fenced_copy_history_and_fixtures_are_not_statements(self):
        write(self.root / "other.md", f"설명에 `https://` 만 있다.\n```markdown\n{PLATFORM}\n```\n")
        write(self.root / "_history" / "과거.md", PLATFORM + "\n")
        write(self.root / "_tools" / "_fixtures" / "out.md", PLATFORM + "\n")
        self.assertEqual(owners.check(self.root), [])

    def test_template_prose_restatement_fails(self):
        write(self.root / "_templates" / "양식.md", f"{PLATFORM}\n")
        self.assertIn("RESTATE HC-PLATFORM _templates/양식.md", owners.check(self.root))

    def test_cli_exit_codes(self):
        command = [sys.executable, str(TOOLS / "fact_owner_check.py"), "--package", str(self.root), "--summary-only"]
        passed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                                env=dict(os.environ, PYTHONUTF8="1"))
        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
        self.assertIn("SUMMARY fact_owner_check status=PASS fail_n=0", passed.stdout)
        write(self.root / "other.md", PLATFORM + "\n")
        failed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                                env=dict(os.environ, PYTHONUTF8="1"))
        self.assertEqual(failed.returncode, 1)
        self.assertIn("status=FAIL", failed.stdout)
        missing = subprocess.run(
            [sys.executable, str(TOOLS / "fact_owner_check.py"), "--package", str(self.root / "없는")],
            capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(missing.returncode, 2)

    def test_registered_sentences_are_copied_from_current_docs(self):
        data = json.loads((PKG / "_schemas" / "fact-owners.json").read_text(encoding="utf-8"))
        ids = [fact["id"] for fact in data["facts"]]
        self.assertEqual(ids, [
            "HC-STREAK", "HC-DRIFT-STATE", "HC-FLAG", "HC-MIDNIGHT", "HC-PLATFORM",
            *OPENS, "TOOL-PY", "TOOL-EXIT",
        ])
        for fact in data["facts"]:
            if fact["id"] in OPENS:
                self.assertIsNone(fact["sentence"])
                self.assertEqual(fact["owners"], [])
                continue
            items = fact["sentence"] if isinstance(fact["sentence"], list) else [fact["sentence"]]
            for sentence in items:
                hits = [owner for owner in fact["owners"]
                        if sentence in (PKG / owner).read_text(encoding="utf-8")]
                self.assertTrue(hits, fact["id"])


if __name__ == "__main__":
    unittest.main()
