# 품질 재평가

2026-10-12 · 대상: 문서 규칙·템플릿·Python 도구 · 패키지 버전 `VERSION`의 1.4.1.

2026-10-13에 유형을 더하면서 `VERSION`은 1.4.2가 되었다. 같은 날 DEV-66을 넣으며 1.4.3이 되었다. 위 문장은 2026-10-12 재평가 당시의 버전이다.

이전의 약 8/10과 9.85는 차원별 평균이 아니다. 둘 다 이 페이지의 통과 기준이 아니다. 확인했다고 적는 범위는 아래 표의 명령과 파일뿐이다.

| 항목 | 판단 | 근거·남은 일 |
|---|---|---|
| 규칙·예제 정합 | 명령으로 확인 | `schema_sync_check.py`, `sample_schema_check.py`, `docs_lint.py`(대상 `demo-docs`), `check_links.py`, `fact_owner_check.py`. 진입은 `python3 _tools/regress_docs_pipeline.py --summary-only` |
| 핵심 도구 | 테스트로 확인 | `tests/test_documents.py`의 네 함수. 이름과 보는 것은 표 아래 |
| 유지보수성 | 코드에서 확인 | `quality_regress_check.py`는 `regress_docs_pipeline.main`을 호출한다. CI 조합은 `.github/workflows/quality.yml` include 3행 |
| 실제 사용 | 이 저장소 밖 | 외부 프로젝트의 편집 로그 경로는 비어 있다. 로그가 생기면 그 경로를 이 칸에 적는다. 그 전에는 위 명령이 본 범위만 확인된 것이다 |

네 함수는 다음이다.

- `test_noop_refresh_preserves_exact_bytes`는 무변경 바이트를 본다.
- `test_invalid_patch_preserves_original`은 잘못된 패치일 때 원본을 본다.
- `test_metadata_patch_preserves_unrelated_meta`는 지정 밖 메타가 유지되는지 본다.
- `test_bad_json_has_clean_error`는 잘못된 JSON의 오류를 본다.

## 이번에 덜어낸 것

| 변경 | 이유 |
|---|---|
| 소수점 배점·목표 달성 선언 삭제 | 객관적인 측정 근거가 없음 |
| 통합 검사 8개 → 5개, 이후 사실 주인 | 그때 남긴 다섯은 스키마 정합, HabitCheck 예제, full 데모 lint, 상대 파일 링크, 행동 테스트다. 사전 검사·IDEAL은 행동 테스트에서도 실행하며 schema_sync 중복 실행은 제거했다. 지금 회귀는 사실 주인을 더해 여섯이다 |
| CI 5개 → 3개 조합 | `.github/workflows/quality.yml`의 include 3행: ubuntu + Python 3.10, windows + Python 3.14, macos + Python 3.14. 3.14를 최신 파이썬이라고 부르지는 않는다 |
| 품질 CLI를 회귀 CLI의 호환 진입점으로 통합 | 같은 실행·JSON·요약 구현을 두 번 관리할 필요가 없음 |
| 자체 Mermaid 노드 수·링크 앵커 판정 제거 | 일부 문법만 해석하면서 정상 문서를 실패시키는 문제 방지 |

목록형 헤더를 lint에서 허용하면서 refresh에서 갱신하지 못하던 오류도 수정했다. 메타데이터를 수정해도 다른 헤더와 본문은 유지한다.

## 확인 범위

```bash
python3 _tools/regress_docs_pipeline.py --summary-only
```

CI의 같은 스크립트는 `.github/workflows/quality.yml`에서 `python _tools/regress_docs_pipeline.py`로 실행된다. 명령 이름의 구분은 `TOOL-PY`([README](README.md))가 맡는다. 여섯 검사가 끝나면 종료 코드는 `TOOL-EXIT`([_tools/README.md](_tools/README.md))이다. 기본 실행은 저장소 파일을 수정하지 않는다. 원격 작업 목록은 [GitHub Actions](https://github.com/jeseokmun/dev-docs-rules/actions)에서 해당 커밋으로 연다. 이 페이지는 그 실행이 성공했는지를 대신 적지 않는다.

Mermaid 전체 문법·최소 노드 수·의미, 링크 앵커·외부 URL, 문서 사실성·개인정보 탐지는 수동 검토 범위다. 원본 변경 감지는 모든 외부 편집기를 잠그지 않는다. 실전 적용 검증 전에는 높은 완성도를 확정하지 않는다.
