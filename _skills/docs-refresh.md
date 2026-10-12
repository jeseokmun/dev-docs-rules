# docs-refresh
기존 DEV-10·30 md에 확인된 변경을 반영한다. 파일이 없으면 [docs-draft](docs-draft.md)를 사용한다.

```bash
python _tools/docs_refresh_cli.py --docs-root "{docs_root}" --type DEV-30 --patch "{temporary-patch.json}" --package .
```

| 규칙 | 처리 |
|---|---|
| 변경 범위 | patch에 지정한 섹션만 교체 |
| 보존 | 나머지 메모·혼합 표/다이어그램·미결 추가 열 유지 |
| 입력 | 객체는 키 병합, 배열은 해당 섹션 전체 교체 |
| 저장 | 임시 후보 검사 후 원자적 교체; 실패 시 원본 유지 |
| 충돌 | 검사 중 대상 변경을 감지하면 실패하고 현재 md에서 다시 시작 |
| 완료 | lint 성공, 수정 사실 확인, 호출자 입력 JSON 제거 |

빈 필수 본문을 미결 문구로 대신 통과시키지 않는다. `--skip-lint`를 썼으면 미검증 초안이라고 명시한다. 수동 extract→render로 사용자 문서를 덮어쓰지 않는다. [CLI 세부 동작](../_tools/README.md)을 따른다.