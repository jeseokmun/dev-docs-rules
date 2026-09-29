# [초안] 템플릿 — DOC-CONFIG (v2)

> 확정본 아님. 권장 경로: `{docs_root}/DOC-CONFIG.md`  
> 패키지에서는 루트 복사본과 `_templates` 보관본이 동일할 수 있음 → **실사용은 docs_root 루트**.

## 문서 성숙도
1. 첫 작성 = **draft 최소(＊) 통과**. 이상 완성 아님.
2. 빈 ＊ → **미결**로 과제화. 假채움·`_…_` 단독 금지.
3. 리뷰는 **보강 요청 목록**을 남긴다. 이상형 미달 ≠ draft 실패.
4. **active**는 핵심 미결 폐쇄 + 검증 가능 후.
5. 코드·사실이 문서를 이기면 갱신하거나 deprecated.

## 최소 기준
| 항목 | 최소 기준 |
|---|---|
| ＊ language | ko/en … — 본문·유형명·Mermaid 라벨 |
| ＊ docs_root | 문서 루트. 기본 추천 docs (변경 가능) |
| ＊ required_profile | light | full |
| ＊ timezone | 예 Asia/Seoul |
| ＊ statuses | draft, active, deprecated |

## 복사용 본문

```markdown
# DOC-CONFIG

- **language:** ko
- **docs_root:** docs
- **required_profile:** light
- **timezone:** Asia/Seoul
- **statuses:** draft, active, deprecated

## 메모
- light 필수: DEV-10, DEV-30
- full 필수: + DEV-20, DEV-50, DEV-90
```

## 작성 규칙
- 헌법은 docs 폴더명을 하드코딩하지 않음 — 항상 이 파일의 docs_root.
