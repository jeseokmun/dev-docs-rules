# 기여 절차

규칙 변경은 관련 문서부터 수정하고 [헌법 개정 절차](DEV-CONSTITUTION.md#0-지위와-개정)를 따른다. Python 3.10 이상이 필요하다. 추가 패키지는 없다.

| 고친 파일 | 같이 볼 파일 |
|---|---|
| `_templates/DEV-*.md`의 H2·필수 표 열 | 같은 코드의 `_schemas/DEV-*.schema.json`, `_examples/DEV-*-*.HabitCheck.md` |
| `_templates/*.md` 또는 루트 `DEV-CONSTITUTION.md` | `demo-docs/_templates/`의 같은 이름, `demo-docs/DEV-CONSTITUTION.md`. 테스트가 바이트 일치를 본다 |
| CLI 옵션·종료 코드·검사 범위 | [_tools/README.md](_tools/README.md), 해당 [_skills](_skills/README.md) |
| 새 DEV 코드 | 헌법 §3 표가 먼저. 그 다음에 스키마·템플릿 |

```bash
python _tools/regress_docs_pipeline.py --summary-only
git diff --check
```

위 블록의 `python`은 `.github/workflows/quality.yml`이 setup-python 뒤에 쓰는 명령 이름이다.

CI 단계는 `--summary-only` 없이 같은 스크립트를 실행한다.

명령 이름의 구분은 `TOOL-PY`([README](README.md))가 맡는다.

회귀가 한 번씩 부르는 것은 `schema_sync_check.py`, `sample_schema_check.py`, `docs_lint.py`(대상은 `demo-docs`), `check_links.py`, `fact_owner_check.py`, `python -m unittest discover -s tests`다. 저장소 파일은 수정하지 않는다.

여섯이 모두 끝나면 종료 코드는 `TOOL-EXIT`([_tools/README.md](_tools/README.md))이다.

`git diff --check`는 변경에 들어온 충돌 표시와 공백 오류를 경고한다. 이 저장소는 `core.whitespace`를 두지 않아 Git 기본을 쓴다. 기본으로 잡히는 것은 줄 끝 공백, 들여쓰기에서 스페이스 바로 뒤의 탭, `<<<<<<<` 같은 충돌 표시다.

테스트를 통과시키려고 확인하지 않은 사실을 채우지 않는다. 품질 문장은 [검증 근거와 한계](QUALITY-REVIEW.md)에 적고, 측정하지 않은 완성도 점수를 쓰지 않는다.
