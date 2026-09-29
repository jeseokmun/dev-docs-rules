# docs-ideal-min (1차 · 실행본 · advisory)

| 항목 | 내용 |
|---|---|
| 종류 | Studio **스킬** (미션 아님). 생애주기 4번째 = **advisory** |
| 순서 | `docs-lint`(draft 게이트) → 본 스킬 → (선택) 사람 `IDEAL-DEV-*` |
| 대상 | `DEV-10` · `DEV-30`만 |
| 입력 | `docs_root` (읽기) |
| 출력 | 콘솔 표 PASS/FAIL/SKIP. md **수정 안 함** |
| 승인 | 없음 (읽기 전용) |
| draft | **실패 조건 아님** (헌법·DOC-MATURITY). `docs_lint` ＊만 draft 게이트 |
| SSOT 경계 | `_check/IDEAL-MACHINE-BOUNDARY.md` |

## 명령
```bash
# 기본 보고 (표)
python3 _tools/ideal_check_min.py "{docs_root}"

# 한 줄 요약만 (보드/채팅용)
python3 _tools/ideal_check_min.py "{docs_root}" --summary-only
# 예: SUMMARY … PASS=7 FAIL=0 SKIP=6 missing=- draft_gate=no

# 기계 JSON (Studio 원샷; --summary-only와 동시 불가)
python3 _tools/ideal_check_min.py "{docs_root}" --json

# 표 + SUMMARY
python3 _tools/ideal_check_min.py "{docs_root}" --summary

# 기계|사람 경계표만
python3 _tools/ideal_check_min.py --print-boundary

# FAIL>0이면 exit 1 — 그래도 draft 탈락으로 쓰지 말 것
python3 _tools/ideal_check_min.py "{docs_root}" --strict

# 고정 샘플 리포트 재생성 (패키지)
python3 _tools/ideal_check_min.py _check/habitcheck-light > _check/IDEAL-HABITCHECK-AUTO.md
python3 _tools/ideal_check_min.py _check/habitcheck-fixtures-docs > _check/IDEAL-HABITCHECK-FIXTURES-AUTO.md
```

## exit 코드
| code | 의미 | draft 영향 |
|---|---|---|
| 0 | 검사 실행됨 (FAIL 있어도 기본) | 없음 |
| 1 | `--strict`이고 FAIL>0 | **여전히 draft 탈락 아님** |
| 2 | 사용법/docs_root 없음 | 도구 오류 |

## 절차
1. `docs_lint.py "{docs_root}"` 먼저 (draft 게이트). FAIL이면 IDEAL 전에 ＊부터.
2. `ideal_check_min.py "{docs_root}" --summary` 실행 → 표·SUMMARY 읽기.
3. FAIL = **보강 요청 후보** (假채움 금지). SKIP = 사람 채점 (`IDEAL-DEV-10/30`).
4. 결과를 채팅/보드에 짧게: `SUMMARY` 한 줄 · 주요 FAIL 한 줄 · draft 아님 명시.
5. (선택) 패키지 회귀: `quality_regress_check.py` 또는 `regress_docs_pipeline.py`.

## 결과 읽는 법
| 결과 | 의미 | 다음 |
|---|---|---|
| PASS | 기계 휴리스틱 통과 | 사람 SKIP 항목만 보면 됨 |
| FAIL | 토큰/헤딩/링크 힌트 부족 | 보강 요청 목록. draft 유지 OK |
| SKIP | 기계 불가 | `IDEAL-DEV-*` 사람 칸 |
| missing=DEV-10/30 | 파일 없음 | light면 draft 먼저 |

## 고정 리포트 (패키지)
| 파일 | 내용 |
|---|---|
| `IDEAL-HABITCHECK-REPORT.md` | HabitCheck 집계·재생성 명령 |
| `IDEAL-HABITCHECK-AUTO.md` | light 샘플 실행 결과 |
| `IDEAL-SELECTION-AUTO.md` | Selection 참고 실행 결과 |
| `IDEAL-MACHINE-BOUNDARY.md` | SKIP 잠금 |

## 완료 기준
| 통과 | 실패로 보고 |
|---|---|
| 명령이 표 또는 SUMMARY를 출력 | docs를 IDEAL FAIL로 덮어씀 |
| draft 게이트로 사용 안 함 | SKIP을 PASS로 假채움 |
| light만 (10·30) | 31종 IDEAL 일괄 확대 |
| GatewAI 사실 발명으로 FAIL 해소 | G1–G3 대기인데 심기 |

## 금지
| 금지 | 이유 |
|---|---|
| IDEAL FAIL → draft 탈락 | 헌법 |
| 새 제품 md 심기 (지금) | G1–G3·Studio 확인 대기 |
| 템플릿/스키마 없이 이상형만 채움 | SSOT 붕괴 |
| regress를 IDEAL FAIL로 깨기 | regress는 advisory smoke만 |

## 관련 스킬
| 다음 | 스킬 |
|---|---|
| 신규 | `docs-draft` |
| 갱신 | `docs-refresh` |
| draft 게이트 | `docs-lint` |
| advisory | `docs-ideal-min` |
| 패키지 회귀 | `docs-quality-regress` |
| 목록 | `README.md` · `STUDIO-WIRING.md` |

