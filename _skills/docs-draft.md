# docs-draft
확인된 사실로 DEV-10·30의 새 초안을 만든다. 출력 md가 기준본이며 값 JSON은 일회 입력이다.

| 입력 | 내용 |
|---|---|
| docs_root | 사용자가 지정한 문서 루트 |
| type | DEV-10 또는 DEV-30 |
| values | 확인된 사실 객체; 입력 파일은 호출 후 호출자가 제거 |

```bash
python _tools/docs_draft_cli.py --docs-root "{docs_root}" --type DEV-10 --values "{temporary-values.json}" --package .
```

필수 키 목록은 [_schemas/DEV-10](../_schemas/DEV-10.schema.json), [_schemas/DEV-30](../_schemas/DEV-30.schema.json)을 확인한다. 제품·날짜·범위는 실제 근거로 채운다. 모르는 항목은 미결과 다음 행동으로 남기고, 미완성 저장이 필요한 경우에만 명시적 `--skip-lint`를 쓴다. 이 경우 lint 통과로 보고하지 않는다.

| 동작 | 처리 |
|---|---|
| 기존 파일 존재 | 자동 교체 금지. 갱신은 [docs-refresh](docs-refresh.md), 전체 교체는 명시적 --overwrite |
| 검증 실패 | 대상에 쓰지 않고 실패 이유 보고 |
| 임시 파일 | 내부 중간 파일 자동 제거; docs_root에 JSON을 만들지 않음 |
| 완료 | md 저장과 lint 성공을 확인하고 실제 결과만 보고 |

코드·제품 사실을 추정하거나 카탈로그 밖 유형을 만들지 않는다. [CLI 세부 동작](../_tools/README.md)을 따른다.