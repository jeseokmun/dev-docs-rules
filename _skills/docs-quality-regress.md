# docs-quality-regress

기존 호출을 위한 호환 진입점이다. 내부에서는 통합 회귀와 같은 검사를 한 번 실행한다.

```bash
python _tools/quality_regress_check.py --summary-only
python _tools/quality_regress_check.py --json
```

기본은 읽기 전용이다. 기존 `--write`는 선택적으로 `_check/QUALITY-REGRESS-LAST.md`를 저장한다. 종료 코드와 `ok`, `rows`, `summary`로 실행 결과를 확인한다. 점수는 자동으로 산정하지 않는다. [평가 근거](../QUALITY-REVIEW.md)를 참고한다.