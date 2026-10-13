# 문서 명세

`_schemas/DEV-*.schema.json` 30개는 헌법 §3.1·§3.2의 DEV 유형과 `_templates/DEV-*.md` 30개와 1:1이다. `DOC-CONFIG`는 설정 파일이며 이 30개에 들어가지 않는다.

이 JSON은 범용 JSON Schema가 아니다. 그 표준의 검증기에 넣지 않는다. 패키지 도구가 읽는 문서 명세이며, 필드 뜻은 아래 표와 `_tools/docs_lint.py`의 `check_file`, `_tools/schema_sync_check.py`의 `check_pair`가 구현한 동작이다.

| 필드 | 의미 |
|---|---|
| code, title | 등록된 코드와 헌법 표의 유형명. 파일명은 `DEV-코드-유형명.md` |
| single_file, path_pattern | 단건이면 `{docs_root}/DEV-코드-유형명.md`. 다건이면 `{docs_root}/DEV-코드-유형명/DEV-코드-{슬러그}.md` |
| required, optional | `id`, `label`, `type`을 가진 섹션. label은 템플릿 H2와 문자 단위로 같다 |
| columns, keys | 표의 열 이름과 순서, 또는 키-값 표의 허용 키 |
| min, min_rows | 문자열 최소 길이와 표의 최소 행. lint가 본다 |
| min_nodes | Mermaid 노드 수의 사람 검토 값. lint는 보지 않는다. 현재는 DEV-30만 4 |
| meta | 첫 H2 이전 블록에 있어야 하는 헤더 키 |
| open_items | 미결 표의 권장 열. `schema_sync_check`는 이 제목이 스키마에 있으면 템플릿에서 한 번인지만 본다. `docs_lint.py`의 `check_file`도 미결 열 이름은 보지 않는다 |
| rules | 작성 원칙 이름. 별도 규칙 엔진으로 실행되지 않는다 |

허용 type은 `string`, `table`, `kv_rows`, `numbered_rows`, `mermaid`, `table_or_mermaid`뿐이다.

## 프로필과 경로

| 프로필 | 없으면 실패하는 코드 |
|---|---|
| light (기본) | DEV-10, DEV-30 |
| full | light에 DEV-20, DEV-50, DEV-90 |

선택 유형은 파일이 있을 때만 본문을 검사한다. 없어도 프로필 검사는 통과한다.

단건은 루트 파일만, 다건은 유형 폴더 안만 허용한다. 어기면 `DOC_PATH`다. 카탈로그에 없는 `DEV-숫자`는 `UNKNOWN_CODE`다. `archive/`와 이름이 `_`로 시작하는 디렉터리 안의 파일은 이 경로 검사에서 뺀다.

DEV-50은 기록이 없을 수 있다. 폴더의 `INDEX.md`에 다음 중 한 줄이 있으면 누락이 아니다. 줄 끝에 `.` 또는 `!`만 더할 수 있다.

- `결정 없음`
- `- 결정 없음`
- `* 결정 없음`

`결정 없음` 뒤에 다른 단어가 있으면 실패한다. 테스트가 그 경우를 실패로 고정한다.

## lint가 실패시키는 것

명령은 저장소 루트에서 `python3 _tools/docs_lint.py {docs_root} --summary-only`이다.

종료 코드는 `TOOL-EXIT`([_tools/README.md](../_tools/README.md))이다.

요약 한 줄은 `SUMMARY docs_lint status=PASS` 또는 `FAIL`로 시작한다. 그 뒤에 `docs_root`, `profile`, `types`, `fail_n`이 온다.

`--summary-only`를 빼면 실패마다 태그가 한 줄씩 더 나온다.

바로 아래 조건 표는 왜 실패하는지이다.

그다음 태그 표는 그때 출력되는 이름이다. 구현은 `docs_lint.py`의 `check_file`이 맡는다. 이 페이지는 그 이름을 표로 옮긴 것이다.

| 검사 | 실패 조건 |
|---|---|
| 제목 | `^#` 줄에 스키마 `code`가 단어로 없음 |
| 헤더 | 첫 H2 앞의 2열 표 또는 `- **키:** 값`에 meta 키가 없거나 자리표시 |
| 상태 | `draft`, `active`, `deprecated` 이외. DOC-CONFIG `statuses`가 있으면 그 목록 |
| 날짜 | `마지막 갱신`이 달력의 `YYYY-MM-DD`가 아님 |
| 코드 | 헤더 `코드`가 스키마 code와 다름 |
| 필수 H2 | required label이 없거나 같은 label이 두 번 |
| 문자열 | 자리표시이거나 `min` 미만 |
| 표 | 열 이름·순서가 columns와 다름, 행 부족, 칸 개수 불일치, 자리표시, 빈 칸 |
| 키-값 | 열은 `구분`, `내용`. 허용 키 밖의 키. `min_rows`가 키 개수 이상이면 키가 모두 있어야 함 |
| Mermaid | 필수 절에 비어 있지 않은 ` ```mermaid ` 펜스가 없음 |
| 비밀 패턴 | SECURITY에 적은 휴리스틱에 걸림. 찾은 값 자체는 출력하지 않음 |

실패 줄의 태그는 `_tools/docs_lint.py`가 붙이는 이름이다.

| 태그 | 언제 |
|---|---|
| `MISSING` | 파일이 없거나, light/full 필수 코드의 파일이 없음 |
| `DUPLICATE_SECTION` | 같은 H2가 두 번 |
| `SECRET_LIKE` | [SECURITY](../SECURITY.md)의 휴리스틱. 값은 붙지 않음 |
| `META_REQUIRED` | 헤더 키가 없거나 자리표시. 뒤에 `: {키}` |
| `META_CODE` | 헤더 `코드`가 스키마 code와 다름 |
| `TITLE_CODE` | `#` 제목에 스키마 code가 단어로 없음 |
| `META_STATUS` | 상태가 `statuses` 밖 |
| `META_DATE` | `마지막 갱신`이 달력의 `YYYY-MM-DD`가 아님 |
| `MISSING_SECTION` | required label이 없음. 뒤에 `: {label}` |
| `EMPTY_SECTION` | 필수 본문이 자리표시. 뒤에 `: {label}` |
| `MIN_LENGTH` | 문자열이 `min` 미만 |
| `MISSING_MERMAID` | 비어 있지 않은 mermaid 펜스가 없음 |
| `MISSING_TABLE` | 필요한 표가 없음 |
| `TABLE_COLUMNS` | 열 이름이나 순서가 다름 |
| `MIN_ROWS` | 행이 부족 |
| `TABLE_WIDTH` | 칸 개수가 헤더와 다름 |
| `FAKEFILL` | 칸 전체가 자리표시 |
| `UNKNOWN_KEYS` | 키-값 표에 허용 키 밖의 키가 있음 |
| `MISSING_KEYS` | `min_rows`가 키 개수 이상인데 키가 빠짐 |
| `EMPTY_CELL` | 표 칸이 빈 문자열 |
| `UNKNOWN_CODE` | 카탈로그에 없는 `DEV-숫자` |
| `DOC_PATH` | 단건/다건 경로가 스키마와 다름 |
| `SCHEMA_SYNC` | `schema_sync_check.py`가 실패. 요약 줄이 뒤에 붙음 |

헤더 이름이 `비고`이거나 `□`를 포함하면 그 칸의 빈 값·자리표시는 실패가 아니다.

자리표시는 칸 전체(앞뒤 공백과 `` `_* ``를 벗긴 뒤)가 다음일 때다. 빈 문자열, `—`, `–`, `-`, `…`, `...`, `TBD`, `TODO`, `tbd tbd`, `lorem ipsum`, `YYYY-MM-DD`, `{중괄호 한 조각}`. `없음`과 `미결`은 그 목록에 없다. 정말 해당 없거나 아직 모를 때만 쓴다.

## lint가 보지 않는 것

선택(○) 절의 열 이름은 검사하지 않는다. 그래도 복사용 본문은 스키마 columns를 쓴다. 생성·추출과 예제가 그 열을 기준으로 한다.

미결 표의 열 이름도 검사하지 않는다. DEV-10·30 생성기가 만드는 열은 `ID`, `내용`이다. 다른 유형의 스키마 `open_items.columns`가 `ID`, `미결`, `다음에 할 일`이면 복사용 본문도 그 세 열이다.

Mermaid의 문법, 노드 수, 한글 라벨, 링크 앵커, 외부 URL, 본문이 사실인지는 사람이 본다. DEV-30의 `min_nodes` 4는 그 사람 검토 값이지 draft 탈락 조건이 아니다.

빈 필수 절을 미결 문장으로 대신 통과시키지 않는다. 생성기가 비운 필수 절을 미결에 옮겨 적더라도, 저장된 문서에 그 필수 H2가 비어 있으면 lint는 실패한다.

## 템플릿 정합

`python _tools/schema_sync_check.py --summary-only`가 카탈로그·스키마·템플릿을 양방향으로 본다. 템플릿의 `##`는 코드 펜스 안도 세므로, 복사용 본문의 H2가 스키마 label과 정확히 한 번씩 맞아야 한다. `＊`로 시작하는 H2는 required에만, `○`로 시작하는 H2는 optional에만 있을 수 있다. 필수 표의 열은 복사용 본문과 스키마가 같아야 한다.

예제 30종은 `python _tools/sample_schema_check.py --summary-only`로 같은 `check_file`을 적용한다.

새 DEV 코드는 헌법 §0의 개정 절차로 카탈로그에 넣은 뒤에만 스키마와 템플릿을 추가한다.

## 사실 주인

`fact-owners.json`은 반복해서 적으면 안 되는 문장과, 값을 비워 두는 id다. `sentence`는 주인 문서에 있는 문장을 복사한 것이다. 열린 id의 `sentence`는 null이고 `owners`는 빈 배열이다. 읽기 전용 검사는 `python3 _tools/fact_owner_check.py --summary-only`이다. 코드 펜스 안은 보지 않는다. `_tools/_fixtures`와 `_history`는 생성 표본과 과거 기록이라 검사하지 않는다.
