# docs-ideal-min
DEV-10·30에 보강 힌트를 제공하는 읽기 전용 advisory다. 기본 FAIL은 draft 탈락 조건이 아니다.

```bash
python _tools/ideal_check_min.py "{docs_root}" --summary-only
python _tools/ideal_check_min.py "{docs_root}" --json
python _tools/ideal_check_min.py --print-boundary
```

| 결과 | 의미 |
|---|---|
| PASS | 제목·경로·명령·언어 힌트의 휴리스틱 충족 |
| FAIL | 사람이 검토할 보강 후보 |
| SKIP | 사실성·제품 범위·자동 테스트 연결 등 수동 판단 |
| missing | DEV-10·30 파일 누락 |

기본 exit 0은 실행 완료를 뜻한다. `--strict`는 FAIL 또는 파일 누락이면 1이다. 사용법/I/O 오류는 2다. DOC-CONFIG가 ko 외 언어면 한국어 라벨 검사는 SKIP한다. 한글 유무는 언어 품질이나 전체 Mermaid 문법을 보증하지 않는다.

먼저 [docs-lint](docs-lint.md)를 실행하고, IDEAL 결과는 다음 보강 항목으로 보고한다. 예제 실행은 `python _tools/ideal_check_min.py demo-docs --json`을 쓴다.