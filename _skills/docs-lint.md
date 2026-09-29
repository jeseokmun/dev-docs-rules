# docs-lint (1차 · 실행본)

| 항목 | 내용 |
|---|---|
| 종류 | Studio **스킬** (미션 아님) |
| 입력 | `docs_root` |
| 승인 | **없음** (읽기 전용) |
| 출력 | 통과 / 미달 표 (콘솔). md 수정 안 함 |

## 명령
```bash
python3 _tools/docs_lint.py "{docs_root}" --package .
python3 _tools/docs_lint.py "{docs_root}" --summary-only
python3 _tools/schema_sync_check.py --package . --summary-only
python3 _tools/regress_docs_pipeline.py --help    # 전체 실행은 인자 없이
```

CLI 표: `_tools/README.md`

## 검사 항목
| 검사 | 내용 |
|---|---|
| ＊ 섹션 | 스키마 required 라벨이 `## ＊ …` 헤딩으로 존재 (미결 문구만으로 통과 불가) |
| 빈 표칸 | 假채움·비밀 휴리스틱 |
| 템플릿 check | 패키지 템플릿과의 대조 |
| schema sync | `schema_sync_check` (required↔템플릿 ＊·○ 1:1) |

## 완료 기준
| 통과 | 실패로 보고 |
|---|---|
| exit 0 | MISSING_SECTION / 假채움 / sync FAIL |
| selection/docs 등 실문서에 재현 | docs_root 밖 몰래 수정 |

회귀가 기대하는 것: full fixture PASS · empty 문서는 ＊ 헤딩 없어 FAIL.

## 다음 (advisory)
lint PASS 뒤 보강 요청만 보려면 `docs-ideal-min` → `_tools/ideal_check_min.py "{docs_root}" --summary-only`.
IDEAL FAIL은 draft 탈락이 **아님**.

## 관련 스킬
| 다음 | 스킬 |
|---|---|
| 신규 | `docs-draft` |
| 갱신 | `docs-refresh` |
| draft 게이트 | `docs-lint` |
| advisory | `docs-ideal-min` |
| 패키지 회귀 | `docs-quality-regress` |
| 목록 | `README.md` · `STUDIO-WIRING.md` |

