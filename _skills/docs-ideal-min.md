# docs-ideal-min
DEV-10·30에 보강 힌트를 제공하는 읽기 전용 advisory다. 기본 FAIL은 draft 탈락 조건이 아니다. 기계가 보는 항목과 SKIP인 항목의 목록은 `--print-boundary`가 출력한다. 이 페이지는 그 목록 전체를 옮기지 않는다.

```bash
python _tools/ideal_check_min.py "{docs_root}" --summary-only
python _tools/ideal_check_min.py "{docs_root}" --json
python _tools/ideal_check_min.py --print-boundary
```

명령 이름의 구분은 `TOOL-PY`([README](../README.md))가 맡는다.

| 결과 | 의미 |
|---|---|
| PASS | 제목·경로·명령·언어 힌트의 휴리스틱 충족 |
| FAIL | 사람이 검토할 보강 후보 |
| SKIP | 사실성·제품 범위·자동 테스트 연결 등 수동 판단 |
| missing | DEV-10·30 파일 누락 |

종료 코드는 `TOOL-EXIT`([_tools/README.md](../_tools/README.md))이다. 그 문장에 IDEAL의 기본과 `--strict`가 있다. DOC-CONFIG가 ko 외 언어면 한국어 라벨 검사는 SKIP한다. 한글 유무는 언어 품질이나 전체 Mermaid 문법을 보증하지 않는다.

`--print-boundary`는 docs_root 없이, 기계가 보는 항목과 SKIP인 항목의 목록만 출력하고 0으로 끝난다. `--json`과 `--summary-only`를 같이 주면 2다.

먼저 [docs-lint](docs-lint.md)를 실행한다. IDEAL 결과는 다음 보강 항목으로 보고한다.

예제 명령은 `python3 _tools/ideal_check_min.py demo-docs --summary-only`다.

2026-10-13에 이 트리에서 그 명령을 실행한 요약은 `SUMMARY docs_root=demo-docs PASS=7 FAIL=0 SKIP=6 missing=- draft_gate=no`였다.

같은 실행의 표 한 행은 `| 5 Mermaid 라벨 언어 | PASS | 한글 라벨 감지 |`였다. 이 PASS는 한글이 보였다는 뜻이다.

다이어그램이 맞다거나, 그 명령이 제품 저장소에서 성공했다는 뜻은 아니다. 그 숫자는 2026-10-13 한 번의 출력이다. 문서를 고치면 바뀐다.
