# 문서 명세
헌법 카탈로그의 DEV 30종과 템플릿이 1:1로 대응한다. DOC-CONFIG는 설정 템플릿이며 DEV 스키마 수에 포함하지 않는다.

이 파일들은 범용 JSON Schema 표준의 검증기가 읽는 스키마가 아니다. 문서 섹션·메타데이터·표 열·최소 행을 정의하는 패키지 고유 JSON 형식이다. 초안 값 렌더링은 DEV-10·30만 지원하고, 문서 lint와 예제 검사는 30종을 지원한다.

| 필드 | 의미 |
|---|---|
| code, title | 등록된 유형 코드·정확한 유형명 |
| single_file, path_pattern | 단건/다건 저장 경로 |
| required, optional | id·label·type을 갖는 섹션 배열 |
| columns, keys | 표 열 또는 키-값 표의 역할 키 |
| min, min_rows, min_nodes | 문자열·행·DEV-30 구조 노드 최소 |
| meta | 문서 공통 헤더의 필수 키 |
| open_items | 미결 표 형식 |
| rules | 작성 원칙 식별자; 별도 자동 실행 규칙 언어가 아님 |

저장소 루트에서 실행한다.

```bash
python _tools/schema_sync_check.py --summary-only
python _tools/sample_schema_check.py --summary-only
```

카탈로그에 등록되지 않은 유형, 누락·중복 템플릿, 빈 카탈로그, 필수 제목·표 열 불일치는 실패한다. 새 DEV 유형은 [헌법 개정 절차](../DEV-CONSTITUTION.md#0-지위와-개정)를 먼저 따른다.