# docs-quality-regress (1차 · 실행본)

| 항목 | 내용 |
|---|---|
| 종류 | Studio **스킬** (미션 아님) · 패키지 건강 점검 |
| 입력 | 없음 (패키지 `_tools` / `_check` 기준) |
| 출력 | 콘솔 + `_check/QUALITY-REGRESS-LAST.md` · 선택 `--json` / `--summary-only` |
| 승인 | 없음 (읽기·리포트 쓰기만) |
| 심기 | **안 함** — GatewAI **오늘 스킵** · md 심기 금지 |

## 명령
```bash
python3 _tools/quality_regress_check.py
# 보드/채팅용 한 줄
python3 _tools/quality_regress_check.py --summary-only
# Studio/기계 파싱
python3 _tools/quality_regress_check.py --json
# 표 원본: _check/QUALITY-REGRESS.md
# 통합 회귀: python3 _tools/regress_docs_pipeline.py --summary-only
```

## SUMMARY 예
`SUMMARY quality_regress PASS PASS=5 FAIL=0 checks=5 plant=no A-F=see_QUALITY.md fails=-`

## 생애주기 위치
| 순서 | 스킬 | 역할 |
|---|---|---|
| 1 | `docs-draft` | 신규 md |
| 2 | `docs-refresh` | 기존 md 패치 |
| 3 | `docs-lint` | draft 게이트(＊) |
| 4 | `docs-ideal-min` | advisory IDEAL |
| 5 | `docs-quality-regress` | 패키지 회귀 원샷 |

## 완료 기준
| 통과 | 실패 |
|---|---|
| LAST 리포트 PASS · GatewAI BLOCKED 허용 | package tools 깨짐 |
| A–F 점수를 5로 올리지 않음 | 심기·사실 발명 |
| `--json`에 `ok`/`summary`/`rows` | draft 게이트로 오용 |

## 관련
| 도구 | |
|---|---|
| `sample_schema_check.py` | HabitCheck↔전유형 스키마 (regress에 포함) |
