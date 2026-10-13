# 템플릿 — DOC-CONFIG (v2.1)

> **v1 기준본 양식.** 고칠 때는 이 파일과 헌법 §0을 함께 본다.
> **용도:** 헌법 §2의 프로젝트 세팅. DEV 유형이 아니다.
> **경로:** `{docs_root}/DOC-CONFIG.md`
> **가독성:** 표 우선. 산문은 이 양식의 규칙만.

값을 채운 파일은 그 프로젝트의 `{docs_root}/DOC-CONFIG.md` 한 장이다. 이 양식은 `_templates/DOC-CONFIG.md`이고, `demo-docs/_templates/DOC-CONFIG.md`는 이 파일과 같은 바이트로 둔다. 패키지 루트의 `DOC-CONFIG.md`는 별도로 고쳐질 수 있으므로 여기서 그 파일과 바이트가 같다고 하지 않는다.

## 표기

| 기호 | 의미 |
|---|---|
| ＊ | 헌법 §2가 최소 항목으로 둔 키 |
| ○ | 권장 |
| □ | 선택 |

## 이 파일이 정하는 것

이 파일에는 DEV 문서의 `상태`가 없다. `draft`·`active`·`deprecated`는 이 파일이 `statuses`로 나열하는, 다른 DEV 문서의 헤더 값이다. 헌법 §1.5의 이상형은 이 세팅 파일의 생애 단계가 아니다.

| 키 | 사람이 맞출 뜻 | 도구 |
|---|---|---|
| ＊ language | 헌법 §1 원칙 8은 본문·유형명·Mermaid 라벨을 이 키와 같게 하라고 한다. 헌법 §2 표는 파일명 슬러그·유형명 언어라고 적는다 | 키가 빠지면 `config()`가 넣는 값은 `ko`다. 이 키를 코드에서 읽는 곳은 `_tools/ideal_check_min.py`의 `check_dev30`이며, DEV-30 Mermaid에 한글이 있는지를 본다. 값이 `ko`가 아니면 그 항목은 SKIP이다. 본문 언어 전체는 사람 검토다 |
| ＊ docs_root | 문서 루트 폴더명. 헌법 §2의 추천은 `docs`이고, 헌법은 그 이름을 하드코딩하지 않는다 | `config()`는 이 키를 lint의 경로 검사에 쓰지 않는다. 키가 없으면 딕셔너리에 넣지 않는다 |
| ＊ required_profile | `light` 또는 `full` | 없으면 `light`. 그 외 값이면 `config()`가 `ValueError`를 내고, `cli()`가 종료 코드 2와 `error: ValueError; check input paths, UTF-8 and JSON structure`를 낸다. 잘못된 값 자체는 출력하지 않는다 |
| ＊ timezone | 헤더 `마지막 갱신`을 읽는 기준. 헌법 §2 표의 예는 `Asia/Seoul` | lint는 시간대를 읽지 않는다. 날짜는 달력의 `YYYY-MM-DD`인지만 본다. 키가 없으면 `config()`가 기본값을 채우지 않는다 |
| ＊ statuses | DEV 문서 `상태`로 허용할 단어. 헌법 §2의 기본은 `draft`, `active`, `deprecated` | 없으면 문자열 `draft, active, deprecated`. `docs_lint.py`는 쉼표로 나누고 앞뒤 공백을 버린 목록과 헤더 `상태`를 비교한다 |

헌법 §1 원칙 2대로 같은 사실을 복붙하지 않는다. 반복되는 사실은 `_schemas/fact-owners.json`의 id를 쓴다. 주인 문서가 그 사실을 한 번 적고, 다른 문서는 id와 경로만 인용한다. 값이 없는 id `HC-REPO`, `HC-DRIFT-VER`, `HC-HASH`, `HC-PKG`, `HC-LEGAL`, `HC-CHANNEL`은 비워 둔다. `HC-STREAK`의 주인은 DEV-30, `HC-DRIFT-STATE`의 주인은 DEV-50, `HC-FLAG`의 주인은 DEV-52, `HC-MIDNIGHT`의 주인은 DEV-70, `HC-PLATFORM`의 주인은 DEV-10, `TOOL-PY`의 주인은 `README`, `TOOL-EXIT`의 주인은 `_tools/README.md`이다.

## 기계 검사

`_tools/docs_common.py`의 `config()`는 `DOC-CONFIG.md` 전체에서 다음 정규식에 맞는 줄만 읽는다. 코드 펜스 안도 읽는다. 표 칸과 YAML만 있는 키는 읽지 않는다.

```text
^-\s+\*\*(\w+):\*\*\s*(.+)$
```

키는 `\w`만 허용한다. 같은 키가 뒤에 다시 나오면 나중 값이 앞 값을 덮는다. 그래서 실사용 파일에 이 양식의 설명을 붙이면, 설명 안의 `- **키:**` 줄이 펜스 안 값을 바꿀 수 있다. 실사용 파일에는 키 줄과, 필요하면 사람이 읽는 메모만 둔다.

| 호출 | 읽는 키 |
|---|---|
| `docs_lint.py` | `required_profile`, `statuses`. `--profile light` 또는 `--profile full`은 그 호출에서만 `required_profile`을 덮어쓴다 |
| `ideal_check_min.py` | `language`. DEV-30 Mermaid 라벨 힌트에만 쓴다 |
| `docs_lint.py`, `ideal_check_min.py` | 두 도구 모두 `config()`로 `docs_root`와 `timezone`을 딕셔너리에 담을 수 있다. 경로 검사와 날짜 검사는 그 두 키를 쓰지 않는다 |

기본 호출에서 없으면 실패하는 코드는 light가 DEV-10·DEV-30, full이 거기에 DEV-20·DEV-50·DEV-90을 더한 것이다. 이 목록은 `docs_lint.py`의 `required` 집합과 헌법 §3.3이 같다. `--only DEV-90`이면 그 호출의 필수 집합은 DEV-90 하나다. 메모 절의 문장은 파서가 읽지 않는다.

## 복사용 본문

```markdown
# DOC-CONFIG

- **language:** ko
- **docs_root:** docs
- **required_profile:** light
- **timezone:** Asia/Seoul
- **statuses:** draft, active, deprecated

## 메모
- light에서 없으면 실패하는 코드는 DEV-10, DEV-30이다.
- full은 그 둘에 DEV-20, DEV-50, DEV-90을 더한다.
```

## 작성 규칙

- `required_profile`을 `light`와 `full` 이외로 두지 않는다. 도구는 그 값으로 끝난다.
- `timezone`의 `Asia/Seoul`은 헌법 §2 표의 예이다. 다른 IANA 이름을 쓸 수 있다. lint는 그 문자열이 실제 시간대인지를 확인하지 않는다.
- `language`를 `en`으로 두면, 헌법 §3.2 표 다음 문장은 영문 유형명 표를 세팅에 두라고 한다. 이 도구는 그 표가 있는지를 확인하지 않는다. 표를 아직 만들지 않았으면 메모에 그 사실과 다음에 둘 경로를 적는다.
- 키를 표로만 적으면 `config()`가 기본값으로 돌아간다. `language`는 `ko`, `required_profile`은 `light`, `statuses`는 `draft, active, deprecated`가 된다.
