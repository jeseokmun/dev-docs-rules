# 기여 절차
규칙 변경은 관련 문서부터 수정하고, 헌법 변경은 [개정 절차](DEV-CONSTITUTION.md#0-지위와-개정)를 따른다.

| 변경 | 함께 확인 |
|---|---|
| 템플릿 | 같은 DEV 스키마·예제·demo 복사본 |
| 스키마 | 제목·열·최소 행·카탈로그 대응 |
| 도구 | 원본 보존, 오류 종료 코드, UTF-8, 부정 입력 회귀 |
| CLI 옵션 | README와 _skills 호출 예제 |
| 릴리즈 | VERSION과 VERSION-CHANGELOG |

```bash
python _tools/regress_docs_pipeline.py --summary-only
git diff --check
```

새 테스트는 기존 결함이나 사용자 동작을 검증한다. 실패를 숨기려고 검사 강도를 낮추거나 미확인 사실을 예제에 채우지 않는다. 의존성은 Python 표준 라이브러리를 기본으로 한다. CI는 고정된 Action 커밋과 최소 읽기 권한을 사용한다.

품질 평가는 [동일한 기준표](QUALITY-REVIEW.md)를 재사용하고, 자동 통과와 사람이 판단한 점수·잔여 한계를 구분한다. 현재 저장소에는 별도 LICENSE 파일이 없으며, 이 변경에서 새 이용허락 조건을 정하지 않는다.