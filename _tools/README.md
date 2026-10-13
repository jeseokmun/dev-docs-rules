# 문서 CLI

실행 환경은 `TOOL-PY`([README](../README.md))다. 명령은 저장소 루트 기준이다. `python`과 `python3`의 구분도 그 문장이다.

## 시작 명령

```bash
# 패키지 전체 검사: 정합·예제·full 데모·파일 링크·사실 주인·미지 절·행동 테스트
python _tools/regress_docs_pipeline.py --summary-only

# 프로젝트 문서 검사
python _tools/docs_lint.py docs --summary-only

# 가상 예제 값으로 새 초안 생성
python _tools/docs_draft_cli.py --docs-root work/my-docs --type DEV-10 --values _tools/_fixtures/habitcheck-dev10.values.json

# 확인된 변경으로 기존 문서 갱신
python _tools/docs_refresh_cli.py --docs-root work/my-docs --type DEV-10 --patch work/confirmed-patch.json
```

실제 프로젝트에는 확인한 사실을 일회 JSON으로 전달한다. 호출자가 준 입력 JSON은 호출자가 삭제하고, CLI 내부 임시 파일은 자동 제거한다.

| 동작 | 규칙 |
|---|---|
| 생성 | DEV-10·30 지원. 기존 파일 전체 교체에만 명시적 `--overwrite` 필요 |
| 갱신 | 지정 섹션만 교체하고 나머지 메모·표·다이어그램·미결 열 유지 |
| 저장 | 후보 검사 후 원자적 교체. 실패하거나 검사 중 원본 변경을 감지하면 반영하지 않음 |
| patch | 객체는 키 병합, 배열은 해당 섹션 전체 교체 |
| 미완성 초안 | `--skip-lint`로 저장 가능. 검사 통과로 보고하지 않음 |
| 문서 검사 | DOC-CONFIG의 light/full을 따름. `--profile`은 덮어쓰기, `--only`는 한 유형만 검사 |

필수 본문·헤더·표 열·최소 행·키·단건/다건 경로와 흔한 비밀 패턴을 검사한다. 빈 필수 항목을 미결 표만으로 대신 통과시키지 않는다. 무변경 갱신은 같은 경로의 BOM·CRLF를 포함한 바이트를 유지한다.

## 보조 도구

여기 없는 인자는 `python _tools/도구명.py --help`가 맡는다. `--json`과 `--summary-only`는 함께 쓸 수 없다.

시작 명령에 코드로 있는 인자는 다음이다.

| 스크립트 | 인자 |
|---|---|
| `regress_docs_pipeline.py` | `--package`, `--json`, `--summary-only` |
| `docs_lint.py` | `docs_root`, `--package`, `--only`, `--profile`, `--skip-schema-sync` |
| `docs_draft_cli.py` | `--docs-root`, `--type`(DEV-10 또는 DEV-30), `--values`, `--from-md`, `--patch`, `--overwrite`, `--skip-lint` |
| `docs_refresh_cli.py` | `--docs-root`, `--type`, `--from-md`, `--patch`, `--skip-lint` |

| 도구 | 용도 |
|---|---|
| [schema_sync_check.py](schema_sync_check.py) | 카탈로그·템플릿·명세 양방향 정합 |
| [sample_schema_check.py](sample_schema_check.py) | 34종 HabitCheck 예제 본문 |
| [check_links.py](check_links.py) | 상대 링크의 대상 파일 존재 |
| [fact_owner_check.py](fact_owner_check.py) | 사실 문장은 주인 파일만. 비주인 재서술, 주인끼리 불일치, 빈 id의 값, 관련 문서에서 빠진 `DEV-NN`·없는 경로를 실패로 본다. `--package`, `--summary-only`, `--json` |
| [template_unknown_check.py](template_unknown_check.py) | 양식이 모르는 값 때문에 절을 지우거나 빼라고 하면 실패한다. 자리표시를 빼고 `없는 사실:`과 `다음 행동:`을 남기는 문장은 통과한다 |
| [ideal_check_min.py](ideal_check_min.py) | DEV-10·30 보강 힌트; 기본 advisory |
| [plant_light_preflight.py](plant_light_preflight.py) | 명시한 대상과 패키지의 읽기 전용 사전 검사 |
| [quality_regress_check.py](quality_regress_check.py) | 통합 회귀의 호환 진입점. 기존 `--write`로 결과 저장 가능 |
| [render_doc.py](render_doc.py) · [extract_values.py](extract_values.py) | DEV-10·30 구조 변환. 사용자 문서 갱신에는 refresh 사용 |

검사는 기본 읽기 전용이다. 명시적 `quality_regress_check.py --write`만 `_check/QUALITY-REGRESS-LAST.md`를 저장한다. `docs_common.py`와 `document_edit.py`는 내부 모듈이다.

`out-DEV-10-empty.md`는 `empty-dev10.values.json`을 `render_doc.py`로 렌더한 결과와 바이트가 같다. 그 파일만 고치면 생성기와 어긋난다. 빈 입력 렌더는 유효한 개요서가 아니다. 필수 칸이 미결로만 옮겨진 실패 형태를 보여 준다.

`out-DEV-10.md`와 `out-DEV-30.md`는 같은 이름의 values JSON으로 렌더한 뒤에, 성공 절차와 실패 단계를 읽어 고친 파일이다.

그 둘을 JSON만으로 다시 렌더하면 고친 문장이 덮인다.

종료 코드: **0** 성공, **1** 검사 실패, **2** 입력·I/O 오류. IDEAL은 기본 FAIL도 0이며 `--strict`일 때 FAIL·파일 누락을 1로 반환한다.

## 검증 한계

Mermaid는 비어 있지 않은 블록의 존재만 검사한다. 전체 문법, 최소 노드 수, 의미, 링크 앵커, 외부 URL, 문서 사실성, 개인정보는 수동 검토한다. 선택(○) 절의 열 이름은 스키마 `column_keys`가 있는 표만 lint가 본다. 미결 표의 열 이름은 lint가 검사하지 않는다. 그 열의 기준은 [_schemas/README.md](../_schemas/README.md)다.

비밀 탐지는 [SECURITY](../SECURITY.md)의 네 패턴이다. 대입은 8자 이상이다. 접두는 `sk-` 뒤 10자다. 인증 헤더는 `Bearer` 뒤 12자다. 개인키 블록은 `BEGIN`과 `PRIVATE KEY`다. 식은 `docs_lint.py`의 `re.I`라 대소문자를 가리지 않는다. 걸리면 `SECRET_LIKE`와 파일 이름만 내고 값은 내지 않는다.

동시 수정 감지는 모든 외부 편집기를 잠그지 않는다. Markdown 표 안의 `|`는 인라인 코드에서도 `\|`로 이스케이프한다. `_schemas`는 범용 JSON Schema가 아닌 자체 문서 명세다.
