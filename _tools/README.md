# 문서 CLI
Python 3.10 이상과 표준 라이브러리만 사용한다. 아래 명령은 저장소 루트 기준이며 Windows에서는 `python`, macOS/Linux에서는 환경에 따라 `python3`를 쓴다.

| 도구 | 역할 | 주요 옵션 |
|---|---|---|
| [docs_draft_cli.py](docs_draft_cli.py) | DEV-10·30 초안 생성, 검사 후 원자적 저장 | `--values`, `--from-md`, `--patch`, `--overwrite`, `--skip-lint` |
| [docs_refresh_cli.py](docs_refresh_cli.py) | 기존 DEV-10·30에서 지정한 섹션만 갱신 | `--docs-root`, `--type`, `--patch`, `--from-md` |
| [docs_lint.py](docs_lint.py) | 프로필 존재 및 작성된 문서 전체 검사 | `--profile light/full`, `--only DEV-XX`, `--json`, `--summary-only` |
| [schema_sync_check.py](schema_sync_check.py) | 헌법 카탈로그·템플릿·스키마 양방향 검사 | `--package`, `--json`, `--summary-only` |
| [sample_schema_check.py](sample_schema_check.py) | 30종 HabitCheck 예제 본문 검사 | `--package`, `--json`, `--summary-only` |
| [render_doc.py](render_doc.py) | DEV-10·30 값 객체를 md로 렌더 | `--schema`, `--values`, `--out` |
| [extract_values.py](extract_values.py) | DEV-10·30 md에서 알려진 값 추출 | `--md`, `--out`, `--stdout` |
| [ideal_check_min.py](ideal_check_min.py) | DEV-10·30 보강 힌트, 기본 advisory | `--strict`, `--json`, `--summary-only`, `--print-boundary` |
| [plant_light_preflight.py](plant_light_preflight.py) | 패키지·명시한 대상의 읽기 전용 사전 검사 | `--docs-root`, `--json`, `--summary-only` |
| [regress_docs_pipeline.py](regress_docs_pipeline.py) | 예제·데모·링크·테스트 통합 회귀 | `--package`, `--json`, `--summary-only` |
| [quality_regress_check.py](quality_regress_check.py) | 통합 회귀와 선택적 결과 저장 | `--write`, `--no-write`, `--json`, `--summary-only` |
| [check_links.py](check_links.py) | 상대 Markdown 파일 링크·앵커 검사 | `--package` |

`docs_common.py`와 `document_edit.py`는 내부 공통 모듈이다. 도구별 상세 인자는 `python _tools/도구명.py --help`로 확인한다.

## 재현 가능한 검증
```bash
python _tools/regress_docs_pipeline.py --summary-only
python _tools/quality_regress_check.py --json
python -m unittest discover -s tests -v
python _tools/docs_lint.py demo-docs --profile full --summary-only
```

기본 검사는 저장소 파일을 수정하지 않는다. `quality_regress_check.py --write`만 `_check/QUALITY-REGRESS-LAST.md`를 생성하며, 생성 결과는 Git에서 제외한다. `--json`과 `--summary-only`는 함께 쓸 수 없다.

## 생성과 갱신
```bash
python _tools/docs_draft_cli.py --docs-root work/my-docs --type DEV-10 --values _tools/_fixtures/habitcheck-dev10.values.json
python _tools/docs_refresh_cli.py --docs-root work/my-docs --type DEV-10 --patch work/confirmed-patch.json
```

첫 명령의 값은 가상 예제다. 실제 프로젝트에는 확인한 사실을 임시 JSON으로 전달한다. 예제의 날짜·제품·실행 명령을 그대로 제품 사실로 쓰지 않는다. CLI가 만드는 중간 파일은 임시 디렉터리에만 있으며 종료 시 제거한다. 호출자가 제공한 입력 JSON은 호출자가 삭제한다.

| 동작 | 보장과 경계 |
|---|---|
| 신규 생성 | 기존 파일이 있으면 실패. 명시적 전체 교체만 `--overwrite` 사용 |
| 갱신 | patch가 지정한 섹션만 교체. 나머지 메모·표·Mermaid·미결 열 유지 |
| 검사 실패 | 대상 원본과 신규 대상 경로에 쓰지 않음 |
| 저장 | 대상 옆 임시 파일 작성 후 동일 파일시스템에서 원자적 교체 |
| 동시 수정 | 검사 전후 원본 바이트를 비교하고 변경 감지 시 중단. 모든 외부 편집기를 잠그지는 않음 |
| 무변경 갱신 | 같은 경로이면 BOM·CRLF를 포함한 바이트 유지 |
| `--skip-lint` | 미완성 초안 저장을 명시적으로 허용. 통과 판정을 뜻하지 않음 |
| 저수준 render/extract | 구조 변환용. 임의 사용자 섹션을 전부 표현하지 않으므로 실제 갱신은 refresh 사용 |

필수 섹션을 비우거나 미결 표만 남기면 lint는 실패한다. 모르는 사실은 미결에 다음 행동과 함께 기록하고 문서는 draft로 유지한다. `features`, `boundary` 등의 배열 patch는 해당 섹션 전체를 대체하고 객체 patch는 키를 병합한다.

## 검사 범위
| 검사 | 자동 확인 |
|---|---|
| 프로필 | light=10·30, full=10·20·30·50·90. DOC-CONFIG를 읽고 `--profile`로 덮어쓸 수 있음 |
| 작성된 선택 문서 | 카탈로그 코드·단건/다건 경로·필수 본문을 함께 검사 |
| 필수 본문 | 실제 H2, 중복, 빈칸·자리표시자, 열·행 최소, 필수 역할 키 |
| 헤더 | 상태·코드·실제 달력 날짜·범위·비범위 |
| 구조도 | DEV-30 Mermaid 블록과 명시된 사각 노드 수 |
| 비밀 | 흔한 키·토큰·개인키 패턴. 일치한 값을 출력하지 않음 |
| 미결 | 필수 본문 부족을 대신 통과시키지 않음. 내용의 사실성은 사람 리뷰 |
| 언어 | IDEAL에서 ko 라벨 힌트 제공. 다른 언어는 수동 확인으로 SKIP |

전체 Mermaid 문법, 사실성, 외부 URL 응답, 개인정보 탐지는 자동 검증 범위 밖이다. Markdown 표의 셀 내부 `|`는 인라인 코드에서도 `\|`로 이스케이프한다. `_schemas`는 일반 JSON Schema가 아니라 이 도구의 문서 명세 형식이다.

| 종료 코드 | 의미 |
|---|---|
| 0 | 검사 통과 또는 실행 성공 |
| 1 | 문서·회귀 검사 실패 |
| 2 | 잘못된 인자·입력·I/O 오류 |
| IDEAL 예외 | 기본은 advisory여서 FAIL도 0. `--strict`는 FAIL 또는 필수 파일 누락이면 1 |