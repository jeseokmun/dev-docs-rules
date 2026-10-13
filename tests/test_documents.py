"""Behavioral regressions for data loss, false passes and checkout portability."""
from __future__ import annotations
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

PKG = Path(__file__).resolve().parents[1]
TOOLS = PKG / "_tools"
sys.path.insert(0, str(TOOLS))
from docs_common import atomic_write, cells, load_object, sections, tables
from docs_lint import check_file
from extract_values import extract
from render_doc import render_dev10, render_dev30
from schema_sync_check import catalog_fails, check_pair
from check_links import check_links


class Documents(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="문서 테스트 ")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.docs = self.root / "문서 경로"
        self.docs.mkdir()
        self.v10 = load_object(TOOLS / "_fixtures/habitcheck-dev10.values.json")
        self.v30 = load_object(TOOLS / "_fixtures/habitcheck-dev30.values.json")
        self.s10 = load_object(PKG / "_schemas/DEV-10.schema.json")
        self.s30 = load_object(PKG / "_schemas/DEV-30.schema.json")
        self.p10 = self.docs / "DEV-10-개요서.md"
        self.p30 = self.docs / "DEV-30-구조명세서.md"
        self.p10.write_text(render_dev10(self.s10, self.v10), encoding="utf-8")
        self.p30.write_text(render_dev30(self.s30, self.v30), encoding="utf-8")

    def command(self, tool, *args):
        return subprocess.run([sys.executable, str(TOOLS / tool), *map(str, args)],
                              capture_output=True, text=True, encoding="utf-8",
                              env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1"), timeout=60)

    def value_file(self, value):
        path = self.root / "patch.json"
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        return path

    def refresh(self, code="DEV-10", patch_file=None, *extra):
        args = ["--docs-root", self.docs, "--type", code]
        if patch_file:
            args += ["--patch", patch_file]
        return self.command("docs_refresh_cli.py", *args, *extra)

    def fail_has(self, path, schema, tag):
        self.assertTrue(any(tag in f for f in check_file(path, schema)), tag)

    def test_valid_light(self):
        r = self.command("docs_lint.py", self.docs, "--json")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(json.loads(r.stdout)["ok"])

    def test_required_heading_empty(self):
        text = self.p10.read_text(encoding="utf-8").replace(self.v10["one_liner"], "")
        self.p10.write_text(text, encoding="utf-8")
        self.fail_has(self.p10, self.s10, "EMPTY_SECTION")

    def test_placeholder_variants(self):
        for value in ["…", "_…_", "TBD", "{제품}", "<!-- fill later -->"]:
            with self.subTest(value=value):
                self.p10.write_text(render_dev10(self.s10, dict(self.v10, one_liner=value)), encoding="utf-8")
                self.fail_has(self.p10, self.s10, "EMPTY_SECTION")

    def test_headings_inside_fence_do_not_count(self):
        text = self.p10.read_text(encoding="utf-8")
        self.p10.write_text(text.replace("## ＊ 한 줄 소개", "## 메모") +
                           "\n```markdown\n## ＊ 한 줄 소개\n채움\n```\n", encoding="utf-8")
        self.fail_has(self.p10, self.s10, "MISSING_SECTION")

    def test_downgraded_star_does_not_count(self):
        self.p10.write_text(self.p10.read_text(encoding="utf-8").replace("＊ 한 줄 소개", "○ 한 줄 소개"), encoding="utf-8")
        self.fail_has(self.p10, self.s10, "MISSING_SECTION")

    def test_duplicate_section(self):
        with self.p10.open("a", encoding="utf-8") as f:
            f.write("\n## ＊ 한 줄 소개\n다른 설명\n")
        self.fail_has(self.p10, self.s10, "DUPLICATE_SECTION")

    def test_too_few_rows(self):
        # Preserve the heading with a two-row table to test the checker, not renderer.
        text = render_dev10(self.s10, self.v10)
        text = text.replace("| 3 | " + self.v10["features"][2] + " |\n", "").replace("| 4 | " + self.v10["features"][3] + " |\n", "")
        self.p10.write_text(text, encoding="utf-8")
        self.fail_has(self.p10, self.s10, "MIN_ROWS")

    def test_missing_audience_role(self):
        text = self.p10.read_text(encoding="utf-8").replace("| 비사용자 |", "| 다른 역할 |")
        self.p10.write_text(text, encoding="utf-8")
        self.fail_has(self.p10, self.s10, "MISSING_KEYS")

    def test_metadata_status_and_date(self):
        for field, value, expected in [("상태", "ready", "META_STATUS"), ("마지막 갱신", "2026-02-30", "META_DATE"), ("마지막 갱신", "20261012", "META_DATE")]:
            with self.subTest(field=field):
                values = copy.deepcopy(self.v10)
                values["meta"][field] = value
                self.p10.write_text(render_dev10(self.s10, values), encoding="utf-8")
                self.fail_has(self.p10, self.s10, expected)

    def test_wrong_metadata_code(self):
        self.p10.write_text(self.p10.read_text(encoding="utf-8").replace("| 코드 | DEV-10 |", "| 코드 | DEV-30 |"), encoding="utf-8")
        self.fail_has(self.p10, self.s10, "META_CODE")

    def test_missing_mermaid_fails(self):
        self.p30.write_text(self.p30.read_text(encoding="utf-8").replace("```mermaid", "```text"), encoding="utf-8")
        self.fail_has(self.p30, self.s30, "MISSING_MERMAID")

    def test_round_mermaid_nodes_are_not_rejected(self):
        text = self.p30.read_text(encoding="utf-8")
        for square, rounded in [("A[화면]", "A(화면)"), ("B[유스케이스]", "B(유스케이스)"),
                                ("C[도메인]", "C(도메인)"), ("D[로컬DB]", "D(로컬DB)")]:
            text = text.replace(square, rounded)
        self.p30.write_text(text, encoding="utf-8")
        self.assertEqual(check_file(self.p30, self.s30), [])

    def test_table_width(self):
        self.p10.write_text(self.p10.read_text(encoding="utf-8").replace("| 1 |", "| 1 | extra |"), encoding="utf-8")
        self.fail_has(self.p10, self.s10, "TABLE_WIDTH")

    def test_pipe_roundtrip(self):
        values = copy.deepcopy(self.v10)
        values["features"][0] = "A | B를 선택"
        values["audience"]["사용자"] = "개인 | 팀"
        text = render_dev10(self.s10, values)
        parsed = extract(text, "DEV-10")
        self.assertEqual(parsed["features"][0], values["features"][0])
        self.assertEqual(parsed["audience"], values["audience"])
        self.p10.write_text(text, encoding="utf-8")
        self.assertEqual(check_file(self.p10, self.s10), [])

    def test_secret_is_redacted(self):
        secret = "sk-" + "Z" * 30
        with self.p10.open("a", encoding="utf-8") as f:
            f.write("\n" + secret + "\n")
        r = self.command("docs_lint.py", self.docs, "--json")
        self.assertEqual(r.returncode, 1)
        self.assertIn("SECRET_LIKE", r.stdout)
        self.assertNotIn(secret, r.stdout + r.stderr)

    def test_full_profile_requires_additional_documents(self):
        r = self.command("docs_lint.py", self.docs, "--profile", "full", "--json")
        self.assertEqual(r.returncode, 1)
        fails = json.loads(r.stdout)["fails"]
        for code in ["DEV-20", "DEV-50", "DEV-90"]:
            self.assertIn("MISSING " + code, fails)

    def test_config_selects_full(self):
        (self.docs / "DOC-CONFIG.md").write_text("- **required_profile:** full\n", encoding="utf-8")
        r = self.command("docs_lint.py", self.docs, "--json")
        self.assertEqual(json.loads(r.stdout)["profile"], "full")
        self.assertEqual(r.returncode, 1)

    def test_only_checks_selected_type(self):
        self.p30.unlink()
        r = self.command("docs_lint.py", self.docs, "--only", "DEV-10", "--json")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_unknown_catalog_code(self):
        (self.docs / "DEV-99-임의.md").write_text("# 임의", encoding="utf-8")
        r = self.command("docs_lint.py", self.docs, "--json")
        self.assertIn("UNKNOWN_CODE", r.stdout)
        self.assertEqual(r.returncode, 1)

    def test_multiple_type_cannot_be_root_file(self):
        (self.docs / "DEV-50-결정.md").write_text("# 잘못된 위치", encoding="utf-8")
        r = self.command("docs_lint.py", self.docs, "--json")
        self.assertIn("DOC_PATH", r.stdout)

    def test_archived_documents_excluded(self):
        archive = self.docs / "archive"
        archive.mkdir()
        (archive / "DEV-99-과거.md").write_text("# 보관", encoding="utf-8")
        self.assertEqual(self.command("docs_lint.py", self.docs, "--summary-only").returncode, 0)

    def test_missing_directory_is_usage_error(self):
        self.assertEqual(self.command("docs_lint.py", self.root / "missing").returncode, 2)

    def test_noop_refresh_preserves_exact_bytes(self):
        self.p10.write_bytes(b"\xef\xbb\xbf" + self.p10.read_text(encoding="utf-8").encode("utf-8").replace(b"\n", b"\r\n"))
        before = self.p10.read_bytes()
        r = self.refresh()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.p10.read_bytes(), before)

    def test_patch_preserves_unknown_sections_and_comments(self):
        original = self.p10.read_text(encoding="utf-8") + "\n## 프로젝트 메모\n<!-- 중요 -->\n보존할 근거\n"
        self.p10.write_text(original, encoding="utf-8")
        r = self.refresh(patch_file=self.value_file({"one_liner": "확인된 새 설명"}))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        result = self.p10.read_text(encoding="utf-8")
        self.assertIn("확인된 새 설명", result)
        self.assertIn("## 프로젝트 메모\n<!-- 중요 -->\n보존할 근거\n", result)
        self.assertIn(dict(sections(original))["○ 왜 필요한가"], result)

    def test_refresh_preserves_mixed_table_and_diagram(self):
        example = next((PKG / "_examples").glob("DEV-30-*.HabitCheck.md"))
        self.p30.write_bytes(example.read_bytes())
        before = dict(sections(example.read_text(encoding="utf-8")))["○ 핵심 실행 흐름"]
        r = self.refresh("DEV-30", self.value_file({"summary": "변경한 구조 설명"}))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(before, self.p30.read_text(encoding="utf-8"))

    def test_refresh_preserves_open_item_extra_columns(self):
        example = next((PKG / "_examples").glob("DEV-10-*.HabitCheck.md"))
        self.p10.write_bytes(example.read_bytes())
        before = dict(sections(example.read_text(encoding="utf-8")))["미결"]
        r = self.refresh(patch_file=self.value_file({"one_liner": "확인된 설명"}))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(before, self.p10.read_text(encoding="utf-8"))

    def test_invalid_patch_preserves_original(self):
        before = self.p10.read_bytes()
        r = self.refresh(patch_file=self.value_file({"one_liner": "…"}))
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertEqual(self.p10.read_bytes(), before)

    def test_secret_patch_preserves_original(self):
        before = self.p10.read_bytes()
        secret = "sk-" + "X" * 30
        r = self.refresh(patch_file=self.value_file({"one_liner": secret}))
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.p10.read_bytes(), before)
        self.assertNotIn(secret, r.stdout + r.stderr)

    def test_draft_requires_explicit_overwrite(self):
        before = self.p10.read_bytes()
        r = self.command("docs_draft_cli.py", "--docs-root", self.docs, "--type", "DEV-10",
                         "--values", TOOLS / "_fixtures/habitcheck-dev10.values.json")
        self.assertEqual(r.returncode, 2)
        self.assertEqual(self.p10.read_bytes(), before)

    def test_invalid_new_draft_creates_no_output(self):
        target = self.root / "new"
        r = self.command("docs_draft_cli.py", "--docs-root", target, "--type", "DEV-10", "--values", self.value_file({}))
        self.assertEqual(r.returncode, 1)
        self.assertFalse(target.exists())

    def test_refresh_wrong_type_preserves_original(self):
        before = self.p10.read_bytes()
        r = self.command("docs_draft_cli.py", "--docs-root", self.docs, "--type", "DEV-10", "--from-md", self.p30)
        self.assertEqual(r.returncode, 2)
        self.assertEqual(self.p10.read_bytes(), before)

    def test_bad_json_has_clean_error(self):
        p = self.root / "bad.json"
        p.write_text("{bad json", encoding="utf-8")
        before = self.p10.read_bytes()
        r = self.refresh(patch_file=p)
        self.assertEqual(r.returncode, 2)
        self.assertNotIn("Traceback", r.stderr)
        self.assertEqual(self.p10.read_bytes(), before)

    def test_wrong_types_and_unknown_keys_rejected(self):
        for value in [[], {"features": "wrong"}, {"audience": []}, {"typo_field": "oops"}, {"boundary": ["bad row"]}, {"run": {"typo": "ignored"}}]:
            with self.subTest(value=value):
                r = self.refresh(patch_file=self.value_file(value))
                self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
                self.assertNotIn("Traceback", r.stderr)

    def test_no_temp_json_in_docs(self):
        r = self.refresh(patch_file=self.value_file({"one_liner": "확인된 설명"}))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(list(self.docs.glob("*.json")), [])
        self.assertEqual(sorted(p.name for p in self.docs.iterdir()), sorted([self.p10.name, self.p30.name]))

    def test_atomic_replace_failure_preserves_original(self):
        before = self.p10.read_bytes()
        with patch("docs_common.os.replace", side_effect=OSError("simulated failure")):
            with self.assertRaises(OSError):
                atomic_write(self.p10, "replacement")
        self.assertEqual(self.p10.read_bytes(), before)
        self.assertEqual(len(list(self.docs.iterdir())), 2)

    def test_refuse_symlink_output(self):
        link = self.docs / "DEV-10-개요서.md"
        original = self.root / "original.md"
        link.rename(original)
        before = original.read_bytes()
        try:
            link.symlink_to(original)
        except OSError:
            self.skipTest("OS does not permit creating symlinks")
        r = self.refresh(patch_file=self.value_file({"one_liner": "갱신"}))
        self.assertEqual(r.returncode, 2)
        self.assertEqual(original.read_bytes(), before)

    def test_utf8_bom_values(self):
        p = self.value_file({"one_liner": "한글 BOM 입력"})
        p.write_bytes(b"\xef\xbb\xbf" + p.read_bytes())
        r = self.refresh(patch_file=p)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_metadata_patch_preserves_unrelated_meta(self):
        self.p10.write_text(self.p10.read_text(encoding="utf-8").replace("| 상태 |", "| 담당자 | 홍길동 |\n| 상태 |"), encoding="utf-8")
        r = self.refresh(patch_file=self.value_file({"meta": {"마지막 갱신": "2026-10-12"}}))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("| 담당자 | 홍길동 |", self.p10.read_text(encoding="utf-8"))

    def test_canonical_roundtrip_for_both_types(self):
        for code, path, schema, render in [("DEV-10", self.p10, self.s10, render_dev10), ("DEV-30", self.p30, self.s30, render_dev30)]:
            with self.subTest(code=code):
                text = path.read_text(encoding="utf-8")
                self.assertEqual(render(schema, extract(text, code)), text)

    def test_summary_and_json_are_exclusive(self):
        r = self.command("docs_lint.py", self.docs, "--json", "--summary-only")
        self.assertEqual(r.returncode, 2)

    def test_ideal_strict_missing_documents_fails(self):
        self.p30.unlink()
        r = self.command("ideal_check_min.py", self.docs, "--strict", "--json")
        self.assertEqual(r.returncode, 1)
        self.assertFalse(json.loads(r.stdout)["ok"])

    def test_ideal_advisory_does_not_block(self):
        r = self.command("ideal_check_min.py", self.docs, "--json")
        self.assertEqual(r.returncode, 0)
        self.assertFalse(json.loads(r.stdout)["draft_gate"])

    def test_preflight_valid_target(self):
        shutil.copy(PKG / "DOC-CONFIG.md", self.docs)
        shutil.copy(PKG / "DEV-CONSTITUTION.md", self.docs)
        r = self.command("plant_light_preflight.py", "--docs-root", self.docs, "--json")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(json.loads(r.stdout)["verdict"], "TARGET_READY")

    def test_preflight_invalid_target_fails(self):
        r = self.command("plant_light_preflight.py", "--docs-root", self.root / "missing", "--json")
        self.assertEqual(r.returncode, 1)
        self.assertFalse(json.loads(r.stdout)["ok"])

    def test_schema_empty_package_cannot_pass(self):
        self.assertIn("EMPTY_CATALOG", catalog_fails(self.root))

    def test_schema_orphan_and_duplicate_templates(self):
        (self.root / "_schemas").mkdir()
        templates = self.root / "_templates"
        templates.mkdir()
        (templates / "DEV-10-a.md").touch()
        (templates / "DEV-10-b.md").touch()
        fails = catalog_fails(self.root)
        self.assertIn("MISSING_SCHEMA DEV-10", fails)
        self.assertIn("DUPLICATE_TEMPLATE DEV-10", fails)

    def test_schema_code_mismatch(self):
        path = self.root / "DEV-10.schema.json"
        value = dict(self.s10, code="DEV-30")
        path.write_text(json.dumps(value), encoding="utf-8")
        template = PKG / "_templates/DEV-10-개요서.md"
        self.assertIn("SCHEMA_CODE DEV-10", check_pair(path, template))

    def test_new_template_without_schema_fails_cli(self):
        pkg = self.root / "package"
        shutil.copytree(PKG / "_templates", pkg / "_templates")
        shutil.copytree(PKG / "_schemas", pkg / "_schemas")
        shutil.copy(PKG / "DEV-CONSTITUTION.md", pkg)
        (pkg / "_templates/DEV-99-임의.md").touch()
        r = self.command("schema_sync_check.py", "--package", pkg, "--json")
        self.assertEqual(r.returncode, 1)
        self.assertIn("MISSING_SCHEMA", r.stdout)

    def test_missing_example_fails(self):
        pkg = self.root / "package"
        shutil.copytree(PKG / "_templates", pkg / "_templates")
        shutil.copytree(PKG / "_schemas", pkg / "_schemas")
        shutil.copytree(PKG / "_examples", pkg / "_examples")
        shutil.copy(PKG / "DEV-CONSTITUTION.md", pkg)
        next((pkg / "_examples").glob("DEV-10-*.HabitCheck.md")).unlink()
        r = self.command("sample_schema_check.py", "--package", pkg, "--json")
        self.assertEqual(r.returncode, 1)
        self.assertIn("MISSING", r.stdout)

    def test_links_detect_missing_target(self):
        (self.root / "a.md").write_text("[broken](missing.md)\n[anchor](b.md#nope)", encoding="utf-8")
        (self.root / "b.md").write_text("# Found", encoding="utf-8")
        fails = check_links(self.root)
        self.assertEqual(len(fails), 1)
        self.assertIn("MISSING_LINK", fails[0])

    def test_all_clis_help(self):
        for path in sorted(TOOLS.glob("*.py")):
            if path.name in {"docs_common.py", "document_edit.py"}:
                continue
            with self.subTest(tool=path.name):
                r = self.command(path.name, "--help")
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_concurrent_edit_is_not_clobbered(self):
        import docs_draft_cli
        patch_file = self.value_file({"one_liner": "후보 설명"})
        concurrent = self.p10.read_bytes() + b"\n<!-- concurrent editor -->\n"
        def concurrent_run(command):
            self.p10.write_bytes(concurrent)
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")
        args = ["docs_draft_cli.py", "--docs-root", str(self.docs), "--type", "DEV-10",
                "--from-md", str(self.p10), "--patch", str(patch_file)]
        with patch.object(sys, "argv", args), patch.object(docs_draft_cli, "run", concurrent_run):
            self.assertEqual(docs_draft_cli.main(), 1)
        self.assertEqual(self.p10.read_bytes(), concurrent)

    def test_bullet_metadata_is_supported(self):
        text = self.p10.read_text(encoding="utf-8")
        blocks = sections(text)
        header = "# DEV-10 개요서 — HabitCheck\n\n"
        for key, value in dict(self.v10["meta"], 코드="DEV-10").items():
            header += f"- **{key}:** {value}\n"
        self.p10.write_text(header + "\n" + "".join(raw for _, raw in blocks[1:]), encoding="utf-8")
        self.assertEqual(check_file(self.p10, self.s10), [])
        r = self.refresh(patch_file=self.value_file({"meta": {"마지막 갱신": "2026-10-12"}}))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        result = self.p10.read_text(encoding="utf-8")
        self.assertIn("- **마지막 갱신:** 2026-10-12", result)
        self.assertIn("- **범위:** " + self.v10["meta"]["범위"], result)

    def test_explicit_no_decisions_index_full_profile(self):
        shutil.copytree(PKG / "demo-docs", self.root / "full")
        docs = self.root / "full"
        folder = docs / "DEV-50-기술결정기록"
        for path in folder.iterdir():
            path.unlink()
        index = folder / "INDEX.md"
        index.write_text("# 기술결정기록\n\n결정 없음\n", encoding="utf-8")
        r = self.command("docs_lint.py", docs, "--json")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        index.write_text("# 기술결정기록\n\n결정 없음이라고 입력할 예정\n", encoding="utf-8")
        self.assertEqual(self.command("docs_lint.py", docs, "--json").returncode, 1)

    def test_template_table_columns_are_checked(self):
        template = self.root / "DEV-10-개요서.md"
        template.write_text((PKG / "_templates" / template.name).read_text(encoding="utf-8").replace("| # | 사용자가 하는 일 |", "| # | 다른 열 |"), encoding="utf-8")
        fails = check_pair(PKG / "_schemas/DEV-10.schema.json", template)
        self.assertTrue(any("TEMPLATE_COLUMNS" in value for value in fails))

    def test_existing_file_mode_is_preserved(self):
        before = self.p10.stat().st_mode
        atomic_write(self.p10, self.p10.read_text(encoding="utf-8"))
        self.assertEqual(self.p10.stat().st_mode, before)

    def test_non_korean_ideal_does_not_require_hangul(self):
        (self.docs / "DOC-CONFIG.md").write_text("- **language:** en\n", encoding="utf-8")
        r = self.command("ideal_check_min.py", self.docs, "--json")
        rows = json.loads(r.stdout)["reports"][1]["rows"]
        self.assertEqual(rows[-1]["status"], "SKIP")

    def test_proposed_adr_cannot_claim_acceptance(self):
        src = PKG / "_examples/DEV-50-로컬DB-drift.HabitCheck.md"
        path = self.docs / src.name
        schema = load_object(PKG / "_schemas/DEV-50.schema.json")
        original = src.read_text(encoding="utf-8")
        path.write_text(original, encoding="utf-8")
        self.assertEqual(check_file(path, schema), [])
        path.write_text(original.replace("| 결정 상태 | proposed |", "| 결정 상태 | accepted |", 1), encoding="utf-8")
        self.assertIn("STATUS_CONFLICT DEV-50-로컬DB-drift.HabitCheck.md", check_file(path, schema))
        claimed = original.replace(
            "accepted는 아래 되돌리는 조건의 스파이크가 끝난 뒤에만 올린다.",
            "이 결정은 accepted다.",
            1,
        )
        path.write_text(claimed, encoding="utf-8")
        self.assertIn("STATUS_CONFLICT DEV-50-로컬DB-drift.HabitCheck.md", check_file(path, schema))

    def test_stride_class_rejects_names_outside_the_six(self):
        src = PKG / "_examples/DEV-55-보안명세서.HabitCheck.md"
        path = self.docs / src.name
        schema = load_object(PKG / "_schemas/DEV-55.schema.json")
        path.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        self.assertEqual(check_file(path, schema), [])
        path.write_text(path.read_text(encoding="utf-8").replace("| 정보 노출 |", "| 기타 |", 1), encoding="utf-8")
        self.assertIn("COLUMN_VALUE DEV-55-보안명세서.HabitCheck.md: ○ 위협과 대응", check_file(path, schema))

    def test_demo_template_copies_match_canonical_sources(self):
        sources = list((PKG / "_templates").glob("*.md"))
        self.assertEqual(len(sources), 32)
        for path in sources:
            with self.subTest(template=path.name):
                copy_path = PKG / "demo-docs/_templates" / path.name
                self.assertEqual(path.read_text(encoding="utf-8"), copy_path.read_text(encoding="utf-8"))
        self.assertEqual((PKG / "DEV-CONSTITUTION.md").read_text(encoding="utf-8"),
                         (PKG / "demo-docs/DEV-CONSTITUTION.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
