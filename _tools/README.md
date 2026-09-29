# _tools CLI 표 (Studio 한 줄용 · 2026-09-10 · 패키지측 완료)

심기·제품 로드맵 없음. JSON은 호출 중 temp만. SSOT=`docs_root` md.

| 도구 | 한 줄 역할 | Studio 요약 플래그 |
|---|---|---|
| `sample_schema_check.py` | HabitCheck 예↔전유형 스키마 ＊·빈칸 | `--summary-only` · `--json` |
| `schema_sync_check.py` | 스키마↔템플릿 ＊·○ 1:1 | `--summary-only` · `--json` |
| `docs_lint.py` | docs_root ＊헤딩·빈칸·假채움 (+ schema_sync) | `--summary-only` · `--json` · `--only` |
| `render_doc.py` | values JSON → md | (없음) |
| `extract_values.py` | md → 임시 values JSON | `--stdout` |
| `docs_draft_cli.py` | draft (values 또는 `--from-md`) | `--skip-lint` |
| `docs_refresh_cli.py` | refresh = draft `--from-md` thin | `--skip-lint` |
| `ideal_check_min.py` | IDEAL DEV-10/30 advisory | `--summary-only` · `--json` · `--print-boundary` |
| `quality_regress_check.py` | QUALITY×회귀 + LAST | `--summary-only` · `--json` |
| `regress_docs_pipeline.py` | 파이프라인 통합 회귀 | `--summary-only` · `--json` |
| `plant_light_preflight.py` | light 심기 사전 (발명 금지) | `--summary-only` · `--json` |
| `check_docs.py` (`_check/`) | 템플릿 기계 최소 | (없음) |

## 예시 (Selection)

```bash
python3 _tools/schema_sync_check.py --summary-only
python3 _tools/sample_schema_check.py --summary-only
python3 _tools/docs_lint.py /workspace/selection/docs --summary-only
python3 _tools/ideal_check_min.py /workspace/selection/docs --summary-only
python3 _tools/ideal_check_min.py /workspace/selection/docs --json
python3 _tools/quality_regress_check.py --summary-only
python3 _tools/regress_docs_pipeline.py --summary-only
python3 _tools/regress_docs_pipeline.py --json
```

## 규칙

| 규칙 | |
|---|---|
| draft 게이트 | `docs_lint` ＊ 최소. IDEAL·QUALITY는 advisory/회귀 |
| GatewAI plant | `plant_light_preflight` BLOCKED면 심기 안 함 |
| 새 DEV 유형 | 카탈로그 확장 금지 (이 표에 안 넣음) |

패키지 루트 README: `../README.md` · VERSION: `../VERSION` · 스킬: `../_skills/README.md`.

## 상태
| 항목 | |
|---|---|
| 패키지측 CLI 표 완료 | 예 (11도구) |
| Studio UI 잠금 | 문제석 카드 |
