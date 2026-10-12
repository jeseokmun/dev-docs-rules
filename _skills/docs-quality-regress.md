# docs-quality-regress
패키지의 재현 가능한 검사를 실행한다. 외부 제품에 문서를 생성하거나 인증 상태를 추정하지 않는다.

```bash
python _tools/quality_regress_check.py --summary-only
python _tools/quality_regress_check.py --json
python _tools/quality_regress_check.py --write --summary-only
```

| 항목 | 처리 |
|---|---|
| 기본 | 읽기 전용; 30종 정합·예제·full 데모·링크·테스트 실행 |
| --write | _check/QUALITY-REGRESS-LAST.md 생성, Git에서는 제외 |
| 결과 | exit 0/1/2와 ok·rows·summary 확인 |
| 점수 | 자동으로 올리지 않음; [평가 근거](../QUALITY-REVIEW.md)에서 판단 |

검사 실패를 PASS나 SKIP으로 숨기지 않는다. IDEAL은 실행·JSON 계약만 회귀 검사하고 의미적 FAIL은 draft 실패로 승격하지 않는다.