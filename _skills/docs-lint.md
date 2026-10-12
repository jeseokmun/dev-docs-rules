# docs-lint
지정한 docs_root를 읽고 수정 없이 결과를 보고한다.

```bash
python _tools/docs_lint.py "{docs_root}" --package . --summary-only
python _tools/docs_lint.py "{docs_root}" --package . --json
```

| 검사 | 범위 |
|---|---|
| 필수 존재 | DOC-CONFIG light/full; --profile으로 명시적 변경 |
| 작성된 문서 | 30종 카탈로그의 코드·단건/다건 경로 |
| 본문 | 실제 필수 H2·중복·내용·자리표시자·표 열·최소 행·키 |
| 헤더 | 상태·코드·날짜·범위·비범위 |
| 구조도 | DEV-30의 비어 있지 않은 Mermaid 블록; 문법·노드 수는 수동 검토 |
| 보안 | 흔한 비밀 패턴; 실제 값 미출력 |
| 패키지 | 템플릿↔스키마 양방향 정합 |

exit 0=통과, 1=검사 실패, 2=입력/실행 오류. 미결 표만으로 필수 내용을 대신하지 않는다. 실패 항목은 구체적인 보강 과제로 보고한다. `--only DEV-XX`는 선택한 한 유형만 검사하므로 전체 프로필 통과로 보고하지 않는다.

[IDEAL](docs-ideal-min.md)은 보강 힌트이며 draft 게이트와 분리한다. [검사 한계](../_tools/README.md)를 함께 따른다.