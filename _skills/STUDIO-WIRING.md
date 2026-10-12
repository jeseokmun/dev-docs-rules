# 에이전트 연동
이 저장소는 문서 CLI와 호출 레시피를 제공한다. 특정 Studio 앱의 자동 설치·설정 UI·연결 상태는 검증하지 않는다.

| 단계 | 레시피 | 역할 |
|---|---|---|
| 생성 | [docs-draft](docs-draft.md) | DEV-10·30 신규 |
| 갱신 | [docs-refresh](docs-refresh.md) | 기존 문서 지정 섹션 갱신 |
| 게이트 | [docs-lint](docs-lint.md) | 필수 최소 검사 |
| 보강 | [docs-ideal-min](docs-ideal-min.md) | advisory |
| 회귀 | [docs-quality-regress](docs-quality-regress.md) | 패키지 검사 |

호출 환경은 Python 3.10 이상, 패키지 경로, 사용자가 지정한 docs_root를 전달한다. 종료 코드와 JSON 결과를 읽고 실제 실행 결과만 보고한다. 앱 측 스킬 로딩 방법은 해당 앱의 설정에서 별도로 확인한다.

[CLI 옵션](../_tools/README.md), [스킬 목록](README.md), [평가 근거](../QUALITY-REVIEW.md)를 참고한다. 과거 작업일지의 계정·경로·보류 상태를 현재 실행 조건으로 사용하지 않는다.