# dev-docs-rules

AI와 함께 개발할 때 쓰는 문서 헌법, 템플릿, 문서 명세, 검사 도구다. 문서는 마크다운과 Mermaid로 쓰고, 표가 먼저다. 필수 칸은 `＊`다. ★는 쓰지 않는다. 확인하지 않은 내용은 미결에 다음에 할 일로 남긴다.

패키지 버전은 루트 `VERSION` 한 줄이다. 이 파일을 읽을 때 그 줄은 `1.4.4`이다.

## 하는 일과 범위 밖

이 저장소는 프로젝트마다 같은 방식으로 개발 문서를 쓰고 검사하게 하는 패키지다. 기준본은 그 프로젝트 `docs_root` 안의 마크다운이다. 값을 담은 JSON은 문서를 만들 때 넘기는 입력이고, 패키지가 보관하는 원본이 아니다.

| 경로 | 하는 일 |
|---|---|
| `DEV-CONSTITUTION.md` | 문서 헌법 |
| `_templates/` | DEV 34종과 `DOC-CONFIG` 양식 |
| `_schemas/` | 문서 명세 34종과 `fact-owners.json` |
| `_tools/` | 초안·검사 Python CLI |
| `_skills/` | CLI를 부르는 에이전트 레시피 |
| `_examples/` | 가상 HabitCheck 예제. 제품 기준본이 아님 |
| `demo-docs/` | 같은 가상 앱을 full로 배치한 트리. 제품 기준본이 아님 |
| `tests/` | 행동 테스트 |
| `VERSION` | 패키지 버전 한 줄 |

이 패키지에 없는 것은 다음이다.

- HabitCheck 앱의 코드와 `pubspec.lock`. 예제와 데모는 가상 적용이다.
- 범용 JSON Schema. `_schemas`는 이 패키지 도구가 읽는 문서 명세다.
- DEV-10과 DEV-30 이외 유형의 초안 생성, 섹션 갱신, 값 렌더. 그 절차는 [_tools/README.md](_tools/README.md)가 맡는다.
- 특정 앱의 설치 로그, 계정, 승인 명단, 리뷰 도구, 채널 이름. 에이전트 연동으로 들어 있는 것은 CLI 레시피뿐이다.
- 측정하지 않은 완성도 점수.

## light, full, 서른네 유형과 DOC-CONFIG

`required_profile`의 기본은 `light`다. light에서 파일이 없으면 실패하는 문서는 DEV-10 개요서와 DEV-30 구조명세서다. `full`은 그 둘에 DEV-20 요구사항명세서, DEV-50 기술결정기록, DEV-90 릴리즈변경기록을 더한다. DEV-50은 폴더 안 기록이 하나 이상이거나, 「결정 없음」이 적힌 인덱스다. 인덱스로 통과하는 줄은 [_schemas/README.md](_schemas/README.md)에 있다.

나머지 유형은 필요할 때 고른다. 없어도 프로필 검사는 통과한다. 헌법 §3.3은 API가 있으면 DEV-40, 외부 SaaS면 DEV-48, 스토어면 DEV-85를 상황 권장으로 적는다. 카탈로그에 없는 `DEV-숫자`는 만들지 않는다.

DEV 유형은 34개다. 1.4.0의 lint가 적던 30종 뒤에 넣은 유형은 DEV-15 용어집, DEV-64 위험및기술부채목록, DEV-66 장애공지, DEV-86 출시준비목록이다. 코드와 유형명 표는 [DEV-CONSTITUTION.md](DEV-CONSTITUTION.md) §3.1(단건, 루트 파일)과 §3.2(다건, 항상 폴더)다. 이 페이지는 그 표를 다시 적지 않는다. 유형명 문자열은 그 표와 같아야 한다. 용도 한 줄은 같은 문서 §5다.

DOC-CONFIG는 DEV 유형이 아니다. 양식은 [`_templates/DOC-CONFIG.md`](_templates/DOC-CONFIG.md)이고, 채운 파일은 `{docs_root}/DOC-CONFIG.md` 한 장이다. `_tools/docs_common.py`의 `config()`는 `- **키:** 값` 줄만 읽는다. 키를 표나 YAML로만 두면 읽히지 않고, 그때 `language`는 `ko`, `required_profile`은 `light`, `statuses`는 `draft, active, deprecated`다. 키의 의미와 기본값은 헌법 §2다.

## 템플릿을 복사하는 법

1. 프로젝트 안에 문서 폴더를 만든다. 헌법이 추천하는 이름은 `docs`다. 헌법은 그 이름을 하드코딩하지 않는다. `DOC-CONFIG`의 `docs_root`에 적은 폴더를 따른다.
2. 루트 `DEV-CONSTITUTION.md`를 그 폴더에 복사한다.
3. `_templates/DOC-CONFIG.md`의 복사용 본문만 `{docs_root}/DOC-CONFIG.md`로 옮긴다. 양식의 설명을 붙이면 설명 안의 `- **키:**` 줄이 펜스 안 값을 덮을 수 있다. 실사용 파일에는 키 줄과, 필요하면 사람이 읽는 메모만 둔다.
4. 각 DEV 문서도 해당 `_templates/DEV-*.md`의 복사용 본문만 가져온다. 펜스 바깥의 설명과 펜스 표시 자체는 제품 문서에 넣지 않는다.

단건(헌법 §3.1)은 문서 루트의 파일 하나다.

`{docs_root}/DEV-{번호}-{유형명}.md`

예: `docs/DEV-10-개요서.md`

다건(헌법 §3.2)은 항상 폴더다. 루트에 파일 하나로 두지 않는다.

`{docs_root}/DEV-{번호}-{유형명}/DEV-{번호}-{슬러그}.md`

예: `docs/DEV-70-구현작업명세서/DEV-70-1234-로그인.md`

light면 DEV-10과 DEV-30부터 둔다. full이면 DEV-20, DEV-50, DEV-90을 더한다. 첫 초안은 `＊` 절이 검사를 통과하면 된다. 확인하지 않은 문장으로 필수 칸을 채우지 않고, 미결에 다음에 할 일을 적는다. DEV-10과 DEV-30은 CLI로 초안을 만들 수 있다. 생성·갱신·덮어쓰기의 절차는 [_tools/README.md](_tools/README.md)가 맡는다.

## 사실의 주인

반복되는 사실마다 주인이 하나다. 등록부가 그 주인의 파일을 적는다. 파일이 둘로 적혀 있으면 같은 문장을 같이 가지는 공동 주인이고, 두 문장은 같아야 한다. 그 밖의 문서는 id와 경로만 인용한다. 등록부는 [`_schemas/fact-owners.json`](_schemas/fact-owners.json)이다. 읽기 전용 검사는 `_tools/fact_owner_check.py`다.

문장이 있는 id는 다음이다.

| id | 주인 |
|---|---|
| HC-STREAK | `_examples/DEV-30-구조명세서.HabitCheck.md`, `demo-docs/DEV-30-구조명세서.md` |
| HC-DRIFT-STATE | `_examples/DEV-50-로컬DB-drift.HabitCheck.md`, `demo-docs/DEV-50-기술결정기록/DEV-50-로컬DB-drift.md` |
| HC-FLAG | `_examples/DEV-52-기능플래그-주간요약.HabitCheck.md` |
| HC-MIDNIGHT | `_examples/DEV-70-오늘체크.HabitCheck.md`, `demo-docs/DEV-70-구현작업명세서/DEV-70-001-오늘체크-유스케이스.md` |
| HC-PLATFORM | `_examples/DEV-10-개요서.HabitCheck.md`, `demo-docs/DEV-10-개요서.md` |
| HC-C4 | `_examples/DEV-30-구조명세서.HabitCheck.md`, `demo-docs/DEV-30-구조명세서.md` |
| TOOL-PY | `README.md`. `python`과 `python3`의 구분은 아래 검사 절에 한 번 적는다 |
| TOOL-EXIT | `_tools/README.md` |

열린 id는 `sentence`가 null이고 `owners`가 빈 배열이다. 등록부에서도 문서에서도 그 값은 비워 둔다. 문서에 값을 채우면 검사가 실패한다.

| id | 비워 두는 것 |
|---|---|
| HC-REPO | 제품 저장소 주소 |
| HC-DRIFT-VER | drift 버전 번호 |
| HC-HASH | 빌드 해시 |
| HC-PKG | 패키지 이름 |
| HC-LEGAL | SPDX 라이선스 식별자 |
| HC-CHANNEL | 공유·알림 채널 이름 |

코드 펜스 안은 이 검사가 보지 않는다. `_tools/_fixtures`와 `_history`도 보지 않는다. 본문이 다른 `DEV-숫자`를 말하고 그 파일에 관련 문서 표가 있으면, 표에 그 코드와 실제 경로가 있어야 한다. 자기 코드는 표에 없어도 된다.

## 회귀가 실행하는 검사

Python 3.10 이상이면 된다. 추가 패키지 설치는 필요 없다. 아래 블록은 `python3`로 적는다. Windows에서 `python3`가 없으면 그 자리만 `python`으로 바꾼다. 저장소 루트에서 실행한다.

```bash
python3 _tools/regress_docs_pipeline.py --summary-only
python3 _tools/schema_sync_check.py --package . --summary-only
python3 _tools/sample_schema_check.py --package . --summary-only
python3 _tools/docs_lint.py demo-docs --package . --skip-schema-sync --summary-only
python3 _tools/check_links.py --package .
python3 _tools/fact_owner_check.py --package . --summary-only
python3 _tools/template_unknown_check.py --package . --summary-only
python3 -m unittest discover -s tests -v
```

첫 줄이 패키지 회귀다. 파이프라인은 해석기의 실행 파일과 패키지 디렉터리의 절대 경로를 `--package`로 넘겨, 나머지 일곱을 위에서 아래로 한 번씩 실행한다. 기본 `--package`는 `_tools`의 부모, 곧 이 저장소다. 저장소 파일은 고치지 않는다. `--json`과 `--summary-only`는 함께 쓰지 않는다. 아래가 전체 검증 표다.

| 순서 | 이름 | 보는 것 |
|---|---|---|
| 1 | `schema_sync_check.py` | 헌법 §3 표, `_templates`, `_schemas`의 양방향 정합 |
| 2 | `sample_schema_check.py` | `_examples`의 HabitCheck 예제 34종 |
| 3 | `docs_lint.py` | `demo-docs`. 그 `DOC-CONFIG`의 `required_profile`은 `full`. 스키마 정합은 1번이 이미 하므로 `--skip-schema-sync` |
| 4 | `check_links.py` | 상대 링크의 대상 파일. 앵커와 외부 주소는 보지 않는다 |
| 5 | `fact_owner_check.py` | 사실 문장의 주인, 주인끼리의 불일치, 비어 있어야 하는 값, 관련 문서의 코드와 경로 |
| 6 | `template_unknown_check.py` | 양식이 모르는 값 때문에 절을 지우거나 빼라고 하는지. 자리표시를 빼고 `없는 사실:`과 `다음 행동:`을 남기는 문장은 통과한다 |
| 7 | `unittest discover -s tests -v` | `tests/`의 행동 테스트 |

`ideal_check_min.py`와 `plant_light_preflight.py`는 이 표의 행이 아니다. 행동 테스트가 그 도구를 부른다. 같은 회귀 스크립트를 `.github/workflows/quality.yml`도 `--summary-only` 없이 실행한다.

일곱이 끝나면 반환 숫자의 뜻은 `TOOL-EXIT`([_tools/README.md](_tools/README.md))다. 이 문장은 그 문장을 다시 쓰지 않는다.

## 예제와 데모

`_examples`와 `demo-docs`는 둘 다 가상 앱 HabitCheck다. 제품 기준본이 아니다. 앱 코드와 `pubspec.lock`은 없다.

| | `_examples` | `demo-docs` |
|---|---|---|
| 배치 | 평탄한 파일. 이름은 `*.HabitCheck.md`이고 템플릿 파일명과 같지 않다 | full 프로젝트. `docs_root`는 `demo-docs`, `required_profile`은 `full` |
| 범위 | DEV 34종과 DOC-CONFIG 샘플. 색인은 [_examples/INDEX.md](_examples/INDEX.md) | full 필수인 DEV-10, DEV-20, DEV-30, DEV-50, DEV-90과 선택인 DEV-22, DEV-35, DEV-40, DEV-48, DEV-70, DEV-85. 34종을 모두 채워 두지는 않았다. 목록은 [demo-docs/README.md](demo-docs/README.md) |
| 비어 있는 유형 | 예제 파일로 있다 | 그 예제 경로를 인용한다 |
| 검사 | `sample_schema_check.py` | 회귀의 `docs_lint.py` |
| 따라감 | 예제를 고쳐도 데모 본문이 자동으로 바뀌지 않는다 | 데모 본문을 고쳐도 예제가 자동으로 바뀌지 않는다 |

`demo-docs/_templates`의 각 파일은 패키지 `_templates`의 같은 이름과 바이트가 같아야 한다. `demo-docs/DEV-CONSTITUTION.md`도 루트 `DEV-CONSTITUTION.md`와 같아야 한다. `tests/test_documents.py`의 `test_demo_template_copies_match_canonical_sources`가 `_templates/*.md` 35개와 헌법 두 파일을 비교한다. 루트에서 `diff -rq _templates demo-docs/_templates`의 출력이 없으면 두 디렉터리가 같다. 출력이 생기면 패키지 `_templates`를 기준으로 데모 복사본을 맞춘다. 데모 안에 채워 둔 제품 문서는 템플릿과 같을 필요가 없다.

## 도구가 보지 않는 것

[_tools/README.md](_tools/README.md)의 검증 한계와 같다. 비밀 패턴의 식은 [SECURITY.md](SECURITY.md)가 맡으므로 여기 다시 적지 않는다.

- Mermaid는 비어 있지 않은 블록이 있는지만 본다. 전체 문법, 최소 노드 수, 의미는 보지 않는다. 스키마 `min_nodes`는 사람 검토 값이다.
- 링크 앵커, 외부 URL, 문서가 사실인지, 개인정보는 수동으로 본다.
- 선택(○) 절의 열 이름은 스키마에 `column_keys`가 있는 표만 lint가 본다. 미결 표의 열 이름은 보지 않는다. 그 기준은 [_schemas/README.md](_schemas/README.md)다.
- 동시 수정 감지는 모든 외부 편집기를 잠그지 않는다.

기여 순서는 [CONTRIBUTING.md](CONTRIBUTING.md), 확인한 범위는 [QUALITY-REVIEW.md](QUALITY-REVIEW.md), 패키지 경계는 [PACKAGE-NOTES.md](PACKAGE-NOTES.md)다.
