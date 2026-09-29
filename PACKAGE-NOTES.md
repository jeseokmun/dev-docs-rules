# 개발론 문서 패키지

> **v1 기준본 + 표 우선**. 프로젝트 `docs_root`에 light(DEV-10·30)부터.  
> 오늘 도구망 태그: 루트 `VERSION` · 이력 `VERSION-CHANGELOG.md`.

## 진입점 (어디부터)
| 보고 싶은 것 | 경로 |
|---|---|
| **지금 VERSION** | `VERSION` |
| VERSION 이력 | `VERSION-CHANGELOG.md` |
| Studio 연동·스킬 | `_skills/STUDIO-WIRING.md` · `_skills/README.md` |
| CLI 한 줄 표 | `_tools/README.md` |
| 품질·회귀 | `_check/QUALITY.md` · `python3 _tools/quality_regress_check.py --summary-only` |
| 하루 요약(중간) | `_check/DAY-SUMMARY-DRAFT.md` |
| 야간 사이클 로그 | `_check/NIGHT-CYCLE-LOG.md` |
| Studio 채택 초안 | `_check/STUDIO-ADOPT-DRAFT.md` |
| Studio 루프 레시피 | `_check/STUDIO-LOOP-RECIPE.md` |
| D·F 언락 조건 | `_check/UNBLOCK-DF.md` |
| 헌법 | `DEV-CONSTITUTION.md` |
| 세팅 양식 | `DOC-CONFIG.md` |

## 포함
| 경로 | 내용 |
|---|---|
| `DEV-CONSTITUTION.md` | 헌법 (표 우선) |
| `DOC-CONFIG.md` | 프로젝트 세팅 양식 |
| `_templates/` | 전 유형 템플릿 v2.1 |
| `_schemas/` | DEV-* **30/30** JSON (템플릿 1:1) |
| `_tools/` | render/extract/draft/refresh/lint/ideal/regress… |
| `_skills/` | Studio 스킬 실행본 |
| `_check/` | 점검·QUALITY·IDEAL·CYCLE·STATUS |
| `_examples/` · `demo-docs/` | HabitCheck 샘플 (SSOT 아님) |

## 자주 쓰는 명령
```bash
python3 _tools/docs_lint.py "{docs_root}" --summary-only
python3 _tools/ideal_check_min.py "{docs_root}" --summary-only
python3 _tools/quality_regress_check.py --summary-only
python3 _tools/regress_docs_pipeline.py --summary-only
python3 _tools/sample_schema_check.py --summary-only
```

## 프로젝트에 심기 (light)
| 단계 | 할 일 |
|---|---|
| 1 | `docs_root` 생성 + 헌법·DOC-CONFIG |
| 2 | 필요 시 `_templates`/`_check`/`_tools` 참조 |
| 3 | DEV-10·30 draft ＊ (`docs_draft_cli` 또는 수동) |
| 4 | `docs_lint` PASS. 假채움 금지 → 미결 |
| 5 | GatewAI 등 **미확인 레포는** `plant_light_preflight` PASS 전 심기 금지 |

## 버전 규칙
| 파일 | 역할 |
|---|---|
| `VERSION` | 현재 한 줄 태그 (SSOT) |
| `VERSION-CHANGELOG.md` | 당일 태그 표 |
| README 본문 숫자 | **쓰지 않음** — `VERSION`을 보라 |

## 오늘 마감 (2026-09-09)
| 시각 | |
|---|---|
| ~20:30 | DAY-SUMMARY 확정 잠금 ✓ (20:50 · 1.2.26) |
| 21:00 | 하루 요약 승격 · 루틴 종료 |
상세: `_check/DAY-SUMMARY-DRAFT.md` · `VERSION-CHANGELOG.md`.
