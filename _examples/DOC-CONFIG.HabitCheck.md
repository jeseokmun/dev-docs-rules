# DOC-CONFIG

- **language:** ko
- **docs_root:** docs
- **required_profile:** full
- **timezone:** Asia/Seoul
- **statuses:** draft, active, deprecated

## 메모

HabitCheck 가상 프로젝트용 샘플이다. `_tools/docs_common.py`의 `config`는 `- **키:** 값` 줄만 읽는다. 표로 쓴 키는 무시되고, `required_profile`이 없으면 light가 된다.

`docs_root` 값 `docs`는 새 프로젝트에 권하는 폴더명이다. 이 저장소에서 실제로 lint하는 가상 루트는 `demo-docs/DOC-CONFIG.md`이며, 그 파일의 `docs_root`는 `demo-docs`다.

`timezone`의 `Asia/Seoul`은 헤더 `마지막 갱신`을 사람이 읽을 때의 기준이다. 패키지 루트 `DOC-CONFIG.md`가 말하듯 lint는 이 값으로 시간대를 검사하지 않는다. 앱이 저장하는 날짜의 경계도 이 키가 아니다. DEV-35. 그 값은 `HC-MIDNIGHT` (`_examples/DEV-70-오늘체크.HabitCheck.md`).
