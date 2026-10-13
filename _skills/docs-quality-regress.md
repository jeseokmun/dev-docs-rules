# docs-quality-regress

기존 호출을 위한 호환 진입점이다. 내부에서는 통합 회귀와 같은 검사를 한 번 실행한다.

```bash
python _tools/quality_regress_check.py --summary-only
python _tools/quality_regress_check.py --json
```

명령 이름의 구분은 `TOOL-PY`([README](../README.md))가 맡는다. `--json`과 `--summary-only`는 함께 쓰지 않는다.

기본은 읽기 전용이다. 기존 `--write`는 선택적으로 `_check/QUALITY-REGRESS-LAST.md`를 저장한다. 결과는 종료 코드와 `ok`, `rows`, `summary`로 본다. 종료 코드는 `TOOL-EXIT`([_tools/README.md](../_tools/README.md))이다.

요약 한 줄의 접두는 `SUMMARY quality_regress`다. 이 이름은 스크립트 파일 이름이 아니다. `regress_docs_pipeline.main`이 이 진입점에 붙인다.

그 뒤에 `PASS` 또는 `FAIL`, `checks=7`, `fail=`, `plant=no`, `fails=`가 온다. `fails=-`는 실패한 검사 이름이 없다는 뜻이다.

이 페이지는 그 형식만 적는다. 명령을 지금 실행한 결과는 적지 않는다. 실행 결과의 자리는 `regress_docs_pipeline.py`의 표준 출력이다. 일곱 검사의 스크립트 이름은 [README.md](../README.md)의 전체 검증 표가 맡는다.

일곱 검사는 스키마 정합, HabitCheck 예제 34종, `demo-docs` full lint, 상대 파일 링크, 사실 주인, 양식의 미지 절 지시, `tests/` 행동 테스트다. 점수는 만들지 않는다. 검증의 한계는 [평가 근거](../QUALITY-REVIEW.md)에 있다.
