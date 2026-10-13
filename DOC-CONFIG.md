# 템플릿 — DOC-CONFIG (v2.1)

> **v1 기준본 양식**. 개정 시 템플릿·헌법 §0을 함께.
> **가독성:** 표 우선. 산문은 요약만.
> **경로:** `{docs_root}/DOC-CONFIG.md` (그 프로젝트의 문서 루트)

문서를 만드는 사람은 아래 복사용 본문만 가져간다. 키는 `language`, `docs_root`, `required_profile`, `timezone`, `statuses`다.

그 다섯 줄은 `_templates/DOC-CONFIG.md`와 `demo-docs/_templates/DOC-CONFIG.md`의 복사용 본문과 같다.

기계 검사 표는 이 패키지 설명이다. 그 표의 문장까지 두 템플릿 사본과 바이트가 같지는 않다.

값을 채운 예는 `demo-docs/DOC-CONFIG.md`와 `_examples/DOC-CONFIG.HabitCheck.md`이다. `demo-docs` 예는 `docs_root`가 `demo-docs`이고 프로필이 full이다.

## 표기
| 기호 | 의미 |
|---|---|
| ＊ | 필수 |
| ○ | 권장 |
| □ | 선택 |

## 문서 성숙도
| 규칙 | 내용 |
|---|---|
| draft | ＊ 최소. 확인하지 않은 채움(假채움) 금지 → 미결 |
| 리뷰 | 보강 요청 목록 |
| active | 핵심 미결 폐쇄 + 검증 가능 |
| 이상형 | draft 실패 조건 아님 |

## 사람 검토
| 항목 | 최소 기준 |
|---|---|
| ＊ language | `ko` 또는 `en`. 본문·유형명·Mermaid 라벨의 언어 |
| ＊ docs_root | 문서 루트 폴더명. 추천 기본은 `docs`. 헌법이 폴더명을 고정하지 않음 |
| ＊ required_profile | `light` 또는 `full`만 |
| ＊ timezone | 헤더 날짜의 기준. 예: `Asia/Seoul` |
| ＊ statuses | 쉼표로 구분. 기본 `draft, active, deprecated` |

## 기계 검사

`_tools/docs_common.py`의 `config`는 이 파일에서 `^- **키:** 값` 줄만 읽는다. 코드 펜스 안이어도 읽는다. 표로 쓴 키는 무시된다.

| 키 | 빠지거나 잘못되면 |
|---|---|
| language | 기본 `ko`. `_tools/ideal_check_min.py`의 `check_dev30`이 `config()`로 이 값을 읽는다. 그 함수는 DEV-30 Mermaid 라벨에 한글이 있는지만 본다. `ko`가 아니면 그 항목은 SKIP이다 |
| required_profile | 기본 `light`. `light`·`full` 외의 값이면 도구가 오류로 끝난다 |
| statuses | 기본 `draft, active, deprecated` |

`docs_root`와 `timezone`은 사람·경로 규칙용이다. lint가 폴더명과 시간대를 이 값으로 검증하지는 않는다. 프로필은 lint가 읽으며, `--profile`을 주면 그 호출에서만 이 값을 덮어쓴다.

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
- full 필수: light + DEV-20, DEV-50, DEV-90
```

## 작성 규칙
- 실사용 파일은 `{docs_root}/DOC-CONFIG.md` 한 장이다. 양식 설명을 그 파일에 붙이지 않는다.
- 표 형식의 키는 파서가 읽지 못하므로 복사용 본문으로 쓰지 않는다.
