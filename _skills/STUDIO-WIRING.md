# 에이전트 연동
이 저장소는 문서 CLI와 호출 레시피를 제공한다. 초안 명령은 [docs-draft.md](docs-draft.md), 갱신 명령은 [docs-refresh.md](docs-refresh.md), 검사 명령은 [docs-lint.md](docs-lint.md), 보강 명령은 [docs-ideal-min.md](docs-ideal-min.md), 회귀 명령은 [docs-quality-regress.md](docs-quality-regress.md)의 bash 블록이 맡는다.

특정 Studio 앱의 설치 로그, 설정 화면의 값, 연결 계정은 비어 있다. 이 파일이 그 값을 검사하지 않는다.

다음에 할 일은 그 앱의 설정에서 스킬 파일 경로를 확인하는 것이다. 확인한 값을 이 저장소 문서에 복사하지 않는다.

| 단계 | 레시피 | 역할 |
|---|---|---|
| 생성 | [docs-draft](docs-draft.md) | DEV-10·30 신규 |
| 갱신 | [docs-refresh](docs-refresh.md) | 기존 문서 지정 섹션 갱신 |
| 게이트 | [docs-lint](docs-lint.md) | 필수 최소 검사 |
| 보강 | [docs-ideal-min](docs-ideal-min.md) | advisory |
| 회귀 | [docs-quality-regress](docs-quality-regress.md) | 패키지 검사 |

호출 환경은 Python 3.10 이상, 패키지 경로, 사용자가 지정한 docs_root다. 종료 코드 0은 성공, 1은 검사 실패, 2는 입력 오류다. IDEAL의 기본 0은 검사 완료이지 draft 통과가 아니다. 그 구분은 [docs-ideal-min](docs-ideal-min.md)에 있다. JSON과 종료 코드에 없는 수정은 하지 않는다. 앱에 스킬을 올리는 값은 위 문단대로 비어 있고, 이 문단에서 다시 정하지 않는다.

[CLI 옵션](../_tools/README.md), [스킬 목록](README.md), [평가 근거](../QUALITY-REVIEW.md)를 참고한다. 과거 작업일지의 계정·경로·보류 상태를 현재 실행 조건으로 사용하지 않는다.
