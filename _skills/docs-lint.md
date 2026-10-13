# docs-lint
지정한 docs_root를 읽고 수정 없이 결과를 보고한다.

```bash
python _tools/docs_lint.py "{docs_root}" --package . --summary-only
python _tools/docs_lint.py "{docs_root}" --package . --json
```

이 블록의 `python`은 CI가 쓰는 이름이다. 그 이름이 없으면 [README](../README.md)의 `python3`로 같은 스크립트를 실행한다. `--json`과 `--summary-only`는 함께 쓰지 않는다.

| 검사 | 범위 |
|---|---|
| 필수 존재 | DOC-CONFIG light/full; --profile으로 명시적 변경 |
| 작성된 문서 | 30종 카탈로그의 코드·단건/다건 경로 |
| 본문 | 필수 H2·중복·내용·자리표시·필수 표 열·최소 행·키. 선택 절과 미결 열 이름은 검사하지 않음 |
| 헤더 | 상태·코드·날짜·범위·비범위 |
| 구조도 | DEV-30의 비어 있지 않은 Mermaid 블록; 문법·노드 수는 수동 검토 |
| 보안 | 흔한 비밀 패턴; 실제 값 미출력 |
| 패키지 | 템플릿↔스키마 양방향 정합 |

exit 0은 통과, 1은 검사 실패, 2는 입력이나 실행 오류다. 미결 표만으로 필수 내용을 대신하지 않는다. 실패 항목은 보강 과제로 보고한다.

`--summary-only`를 빼면 실패마다 한 줄이 더 나온다.

`META_DATE {파일명}`은 `마지막 갱신`이 달력의 `YYYY-MM-DD`가 아닐 때다. `EMPTY_SECTION {파일명}: {필수 제목}`은 그 필수 본문이 자리표시일 때다.

나머지 태그 이름은 [_schemas/README.md](../_schemas/README.md)에 있다.

`--only DEV-XX`는 선택한 한 유형만 검사한다. 그 결과를 전체 프로필 통과로 보고하지 않는다.

[IDEAL](docs-ideal-min.md)은 보강 힌트이며 draft 게이트와 분리한다. [검사 한계](../_tools/README.md)를 함께 따른다.
