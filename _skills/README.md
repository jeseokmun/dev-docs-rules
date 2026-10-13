# 이 저장소의 문서 스킬

| 스킬 | 파일 | CLI |
|---|---|---|
| docs-draft | `docs-draft.md` | `docs_draft_cli.py` |
| docs-refresh | `docs-refresh.md` | `docs_refresh_cli.py` |
| docs-lint | `docs-lint.md` | `docs_lint.py` |
| docs-ideal-min | `docs-ideal-min.md` | `ideal_check_min.py` |
| docs-quality-regress | `docs-quality-regress.md` | `quality_regress_check.py` |

연동 순서는 [STUDIO-WIRING.md](STUDIO-WIRING.md)다. 패키지 버전은 루트 `VERSION` 한 줄이다.

절차는 스킬 파일이 맡는다. 초안은 [docs-draft.md](docs-draft.md), 갱신은 [docs-refresh.md](docs-refresh.md), 검사는 [docs-lint.md](docs-lint.md), 보강은 [docs-ideal-min.md](docs-ideal-min.md), 회귀는 [docs-quality-regress.md](docs-quality-regress.md)이다.

종료 코드는 [_tools/README.md](../_tools/README.md)와 같다. 0은 성공이다. 1은 검사 실패다. 2는 입력·I/O 오류다.

IDEAL만 기본 종료 코드가 다르다. 그 차이는 [docs-ideal-min.md](docs-ideal-min.md)가 맡는다.

회귀 `regress_docs_pipeline.py`의 `collect()`가 부르는 다섯은 이 순서다.

1. `schema_sync_check.py`
2. `sample_schema_check.py` — HabitCheck 예제 30종
3. `docs_lint.py` — 대상은 `demo-docs`
4. `check_links.py`
5. `tests/`의 unittest
