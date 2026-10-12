# HabitCheck 가상 적용
이 폴더는 full 프로필을 적용한 가상 예제이며 실제 제품 SSOT로 사용하지 않는다. 참조 예제는 [전체 예제](../_examples/INDEX.md)에서 확인한다.

| 포함 | 목적 |
|---|---|
| DEV-10·20·30·50·90 | full 필수 문서 |
| DEV-22·35·40·48·70·85 | 다건 경로 및 선택 문서 |
| _templates | 30개 DEV + DOC-CONFIG 복사본 |
| DEV-CONSTITUTION·DOC-CONFIG | 프로젝트 규칙과 설정 |

저장소 루트에서 `python _tools/docs_lint.py demo-docs --summary-only`로 검사한다. DOC-CONFIG의 docs_root는 저장소 기준 `demo-docs`다. `_check`는 포함하지 않는다.