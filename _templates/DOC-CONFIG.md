# 템플릿 — DOC-CONFIG (v2.1)

> **v1 기준본 양식**. 개정 시 템플릿·헌법 §0을 함께.  
> **가독성:** 표 우선. 산문은 요약만.  
> **경로:** `{docs_root}/DOC-CONFIG.md` (실사용 루트)

## 표기
| 기호 | 의미 |
|---|---|
| ＊ | 필수 |
| ○ | 권장 |
| □ | 선택 |

## 문서 성숙도
| 규칙 | 내용 |
|---|---|
| draft | ＊ 최소. 假채움 금지 → 미결 |
| 리뷰 | 보강 요청 목록 |
| active | 핵심 미결 폐쇄 + 검증 가능 |
| 이상형 | draft 실패 조건 아님 |

## 최소 기준
| 항목 | 최소 기준 |
|---|---|
| ＊ language | ko/en … |
| ＊ docs_root | 기본 추천 docs |
| ＊ required_profile | light|full |
| ＊ timezone | 예 Asia/Seoul |
| ＊ statuses | draft, active, deprecated |

## 복사용 본문

```markdown
# DOC-CONFIG

| 필드 | 값 |
|---|---|
| language | ko |
| docs_root | docs |
| required_profile | light |
| timezone | Asia/Seoul |
| statuses | draft, active, deprecated |

## 메모
| 항목 | 내용 |
|---|---|
| light 필수 | DEV-10, DEV-30 |
| full 필수 | + DEV-20, DEV-50, DEV-90 |

```
