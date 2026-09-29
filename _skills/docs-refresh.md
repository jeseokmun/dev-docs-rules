# docs-refresh (1차 · 실행본)

| 항목 | 내용 |
|---|---|
| 종류 | Studio **스킬** (미션 아님) |
| 1차 유형 | `DEV-10` · `DEV-30`만 |
| 입력 | `docs_root`, 유형 1개, **확인된** 변경만 (`--patch`) |
| SSOT | 기존 md. JSON 파일로 저장 금지 |
| CLI | `_tools/docs_refresh_cli.py` → 내부 `docs_draft_cli --from-md` |
| 승인 | docs_root만. 코드·비밀 경로면 막거나 승인 |

## 절차 (단일 CLI)
기존 md 없으면 **docs-draft**로. 있으면:

```bash
# 확인된 변경만 patch JSON (호출 후 삭제). md는 docs_root에서 자동 탐색
python3 _tools/docs_refresh_cli.py \
  --docs-root "{docs_root}" \
  --type DEV-30 \
  --patch /tmp/patch.json \
  --package .

# 경로를 명시할 때
python3 _tools/docs_refresh_cli.py \
  --docs-root "{docs_root}" \
  --type DEV-10 \
  --from-md "{docs_root}/DEV-10-개요서.md" \
  --patch /tmp/patch.json \
  --package .
```

내부: `docs_draft_cli --from-md` → `extract_values` → merge patch → `render_doc` → `docs_lint` → temp 삭제.

수동 extract→render 절차는 **폐기**. 동일 파이프는 draft CLI만.

커밋마다 자동 최신화 **없음**. 호출 시에만.

## 완료 기준
| 통과 | 실패 |
|---|---|
| 변경 사실만 반영된 md | 추측으로 로드맵·모듈 채움 |
| lint PASS 또는 미결만 | values를 영구 JSON으로 보관 |
| 유형 1개 | 코드 트리 무단 스캔 후 문서화 |
| docs_root에 `.json` 없음 | extract/render를 스킬이 직접 호출 |

## 금지
假채움 · JSON SSOT화 · 옛 문서 이관 · 미확인 제품 사실 발명 · draft와 다른 렌더 경로

## 관련 스킬
| 다음 | 스킬 |
|---|---|
| 신규 | `docs-draft` |
| 갱신 | `docs-refresh` |
| draft 게이트 | `docs-lint` |
| advisory | `docs-ideal-min` |
| 패키지 회귀 | `docs-quality-regress` |
| 목록 | `README.md` · `STUDIO-WIRING.md` |

