# 기여 절차

규칙 변경은 관련 문서부터 수정하고 [헌법 개정 절차](DEV-CONSTITUTION.md#0-지위와-개정)를 따른다. 템플릿을 바꾸면 같은 유형의 스키마·예제·데모 복사본을 함께 확인한다. CLI 옵션 변경은 [_tools/README.md](_tools/README.md)에 반영한다.

```bash
python _tools/regress_docs_pipeline.py --summary-only
git diff --check
```

테스트는 원본 보존과 실제 사용자 동작·결함을 검증한다. 검사를 통과시키려고 미확인 사실을 채우지 않는다. 품질 평가는 [검증 근거와 한계](QUALITY-REVIEW.md)를 함께 기록한다.