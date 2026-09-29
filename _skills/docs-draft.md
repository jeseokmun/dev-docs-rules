# docs-draft (1차 · 실행본)

| 항목 | 내용 |
|---|---|
| 종류 | Studio **스킬** (미션 아님) |
| 1차 유형 | `DEV-10` · `DEV-30`만 |
| 입력 | `docs_root`, 유형 1개, **확인된** 사실만 |
| 출력 | `{docs_root}` 아래 md (**SSOT**) |
| 중간 | 값 JSON — **디스크에 남기지 않음** (`docs_draft_cli` temp) |
| CLI | `_tools/docs_draft_cli.py` |

## 값 객체 (스키마 키)
| 공통 | 내용 |
|---|---|
| `product` | 제품명 문자열 |
| `meta` | `상태`/`마지막 갱신`/`범위`/`비범위` |
| `open` | 미결 행 `[{ID, 내용}, …]` |

| DEV-10 required | 키 |
|---|---|
| ＊ 한 줄 소개 | `one_liner` |
| ＊ 누구를 위한가 | `audience` |
| ＊ 핵심 기능 | `features` |
| ＊ 실행·설치 | `run` |
| ＊ 시스템 경계 | `boundary` |

| DEV-30 required | 키 |
|---|---|
| ＊ 한 줄 구조 요약 | `summary` |
| ＊ 모듈/레이어 | `modules` |
| ＊ 구조도 | `mermaid` |
| ＊ 의존 규칙 | `deps` |
| ＊ 건드리기 위험 구역 | `danger` |

## 절차 (CLI)
```bash
# A) 신규: 확인된 values만 (temp 입력 파일은 CLI 밖 temp에 두고 호출 후 삭제)
python3 _tools/docs_draft_cli.py \
  --docs-root "{docs_root}" \
  --type DEV-10 \
  --values /tmp/vals.json \
  --package .

# B) 기존 md 기반 갱신형 draft: extract + patch (JSON은 docs_root에 안 남김)
python3 _tools/docs_draft_cli.py \
  --docs-root "{docs_root}" \
  --type DEV-10 \
  --from-md "{docs_root}/DEV-10-개요서.md" \
  --patch /tmp/patch.json \
  --package .
```
내부: `extract_values` → merge → `render_doc` → `docs_lint` → temp 삭제.

## 완료 기준
| 통과 | 실패 |
|---|---|
| md 존재 + lint(또는 미결만) | 템플릿 전문 재작성 |
| docs_root에 `.json` values 없음 | 31종 일괄·假채움 |

## 금지
| 금지 | 이유 |
|---|---|
| 템플릿 전문을 모델이 다시 쓰기 | 토큰·형식 붕괴 |
| values를 docs_root에 저장 | SSOT=md |
| 假채움 | 헌법 |

## 관련 스킬
| 다음 | 스킬 |
|---|---|
| 신규 | `docs-draft` |
| 갱신 | `docs-refresh` |
| draft 게이트 | `docs-lint` |
| advisory | `docs-ideal-min` |
| 패키지 회귀 | `docs-quality-regress` |
| 목록 | `README.md` · `STUDIO-WIRING.md` |

