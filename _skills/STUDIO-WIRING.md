# Studio 연동 체크리스트 (확인된 것만 · 2026-09-10 · 패키지측 잔여)

추측·로드맵 금지. 미확인은 `확인 필요`.

## 패키지 진입점
| 문서 | 용도 |
|---|---|
| `../README.md` | 패키지 루트 진입 |
| `../VERSION` · `../VERSION-CHANGELOG.md` | 현재 태그·이력 |
| `README.md` (이 폴더) | 스킬 목록 |
| `../_tools/README.md` | CLI 플래그 표 |
| `../_check/DAY-SUMMARY-DRAFT.md` | 하루 중간/마감 요약 |

## 확정 (house docs / 스킬)
| # | 항목 | 상태 | 근거 |
|---|---|---|---|
| 1 | 스킬 이름 | docs-draft / docs-refresh / docs-lint / **docs-ideal-min**(advisory) | 잠금: 미션 아님. 앞 3=생애주기, ideal=보강 요청 |
| 2 | 1차 유형 | DEV-10 · DEV-30만 | light 프로필 |
| 3 | SSOT | `docs_root` md | JSON은 호출 중 temp만 |
| 4 | 렌더 | `_tools/render_doc.py` + 스키마 | 모델이 템플릿 전문 재작성 금지 |
| 4a | draft/refresh CLI | `docs_draft_cli` / `docs_refresh_cli` | refresh=`draft --from-md`; JSON temp만 |
| 5 | lint | `_tools/docs_lint.py` 읽기·무승인 | ＊는 ## 헤딩만 인정 |
| 6 | 켜기 | Studio 설정 UI **한 번** | 스킬이 트리/켜기 담당 아님 |
| 7 | 호출 | 슬래시 또는 Commander | |
| 8 | 카탈로그 | 트리=필수 10·30 + 선택 카탈로그 | 옛 문서 이관·요약 금지 |
| 9 | 폐기/트리 위치 | UI 담당 | 스킬 본문 밖 |
| 10 | package 스킬 초안 | `_skills/docs-*.md` | Studio 앱 내 설치 여부는 별도 |

## 확인 필요 (앱/제품 — 여기서 발명 금지)
| # | 항목 | 비고 |
|---|---|---|
| A | 기본 프로필 light vs 켤 때 질문 | **홀드** (문제석 스킵·재질문 금지 · 2026-09-10) |
| B | 문서 트리: 사이드바 vs 미션 패널 | **홀드** (스킵·재질문 금지) |
| C | Studio에 이 package 경로/`_skills` 자동 로드 여부 | **홀드** (스킵·재질문 금지) |
| D | GatewAI docs_root·심기 | **스킵 유지**. 상세 `GATEWAI-LIGHT-PLANT-CHECK.md` |

## 패키지측 완료도 (앱 UI 제외)
| 항목 | 상태 |
|---|---|
| CLI 전종 README | 됨 (`_tools` 11) |
| 스킬 실행본 5 | 됨 |
| regress ← sample_schema | 됨 |
| 진입점 README/WIRING | 됨 |
| Studio A/B/C 잠금 | **홀드** (재질문 금지) → F=5 대기 |

## 패키지 쪽 완료 신호
| 신호 | 명령/경로 |
|---|---|
| 회귀 PASS | `python3 _tools/regress_docs_pipeline.py` [`--summary-only`|`--json`] |
| 스킬 실행본 | `_skills/docs-draft.md` · `docs-refresh.md` · `docs-lint.md` · `docs-ideal-min.md` · `docs-quality-regress.md` |
| 이 체크리스트 | `_skills/STUDIO-WIRING.md` |
| GatewAI light 사전점검 | `python3 _tools/plant_light_preflight.py` [`--summary-only`\|`--json`] |
| IDEAL 최소(advisory) | `python3 _tools/ideal_check_min.py {docs_root}` [`--summary-only`\|`--json`] · 경계 `IDEAL-MACHINE-BOUNDARY.md` |
| docs-ideal-min 스킬 | `_skills/docs-ideal-min.md` (draft 게이트 아님) |
| QUALITY×회귀 CLI | `quality_regress_check.py` [`--summary-only`\|`--json`] → LAST + SUMMARY/JSON |
| docs-quality-regress | 패키지 QUALITY×회귀 원샷 | `_skills/docs-quality-regress.md` |
| CLI 표 | `_tools` 한 줄 플래그 표 | `_tools/README.md` |
| lint/sync 요약 | `docs_lint`/`schema_sync` `--summary-only`/`--json` | Studio 원샷 |
| regress 요약 | `regress_docs_pipeline` `--summary-only`/`--json` | Studio 원샷 |
| HabitCheck↔스키마 | `sample_schema_check.py` [`--summary-only`\|`--json`] | 전유형 30 |
| values↔md | `extract_values.py` / `render_doc.py` | regress round-trip |
| schema↔템플릿 | `schema_sync_check.py` [`--summary-only`\|`--json`] | 전유형 30 |
