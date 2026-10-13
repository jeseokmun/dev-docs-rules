# docs-refresh
기존 DEV-10·30 md에 확인된 변경을 반영한다. 파일이 없으면 [docs-draft](docs-draft.md)를 사용한다.

```bash
python _tools/docs_refresh_cli.py --docs-root "{docs_root}" --type DEV-30 --patch "{temporary-patch.json}" --package .
```

명령 이름의 구분은 `TOOL-PY`([README](../README.md))가 맡는다.

패치 JSON은 값 객체의 일부다. 객체 키는 그 섹션만 합치고, 배열 키는 그 섹션을 통째로 바꾼다.

```json
{"one_liner": "확인된 한 문장"}
```

위 `one_liner` 값은 키 모양만 보여 준다. 키 이름 전체는 [docs-draft.md](docs-draft.md)의 표가 맡는다. 제품 문서에는 확인된 문장을 넣고, 이 예문 자체를 복사하지 않는다.

```json
{"flow": [{"단계": "1", "행위자": "사용자", "행동": "확인된 행동"}]}
```

`flow`는 배열이라 `○ 핵심 실행 흐름` 전체가 이 배열로 바뀐다.

| 규칙 | 처리 |
|---|---|
| 변경 범위 | patch에 지정한 섹션만 교체 |
| 보존 | 나머지 메모·혼합 표/다이어그램·미결 추가 열 유지 |
| 입력 | 객체는 키 병합, 배열은 해당 섹션 전체 교체 |
| 저장 | 임시 후보 검사 후 원자적 교체; 실패 시 원본 유지 |
| 충돌 | 검사 중 대상 변경을 감지하면 실패하고 현재 md에서 다시 시작 |
| 완료 | lint 성공, 수정 사실 확인, 호출자 입력 JSON 제거 |

빈 필수 본문을 미결 문구로 대신 통과시키지 않는다. `--skip-lint`를 썼으면 미검증 초안이라고 명시한다.

수동 extract에서 render로 사용자 문서를 덮어쓰지 않는다.

종료 코드는 `TOOL-EXIT`([_tools/README.md](../_tools/README.md))이다. 검사에 실패하거나 충돌을 감지하면 원본을 유지한다.

세부 동작은 [CLI 설명](../_tools/README.md)이 맡는다.
