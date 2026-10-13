# DOC-CONFIG

- **language:** ko
- **docs_root:** demo-docs
- **required_profile:** full
- **timezone:** Asia/Seoul
- **statuses:** draft, active, deprecated

## 메모
- HabitCheck 가상 적용의 세팅이다. 양식 설명은 패키지 `_templates/DOC-CONFIG.md`에 둔다. 이 파일은 값이다.
- 기계가 읽는 줄은 위 다섯 키뿐이다. 키는 표로 쓰지 않고 `- **키:** 값` 한 줄로 둔다. `_tools/docs_common.py`의 `config`는 그 줄만 읽고, 메모 절은 읽지 않는다.
- `full`이면 light의 `DEV-10-개요서.md`·`DEV-30-구조명세서.md`에 더해 `DEV-20-요구사항명세서.md`, `DEV-50-기술결정기록/`의 기록 1건, `DEV-90-릴리즈변경기록/`의 기록 1건이 있어야 한다. 그 세 가지가 없으면 full 검사가 실패한다. 선택 문서가 없어도 그 검사는 통과한다. 선택 문서의 파일명은 `README.md` 표에 있다.
- `timezone`은 헤더 `마지막 갱신`을 읽는 달력이다. 날짜 값은 각 문서 헤더에 둔다.
- 헤더 상태는 `draft`, `active`, `deprecated`만 쓴다.
- README가 적는 제품 `DEV-*.md`의 상태 필드는 `draft`다. 그 문장에서 빼는 파일은 `_templates`와 `DEV-CONSTITUTION.md`다. `active`는 그 문서의 미결이 닫힌 뒤에 쓴다.
- lint는 `required_profile`을 이 파일에서 읽는다. 호출에 `--profile`이 있으면 그 한 번만 이 값을 덮어쓴다.
