# 패키지 범위
현재 진입점은 [README](README.md), 명령은 [_tools/README](_tools/README.md), 평가 근거는 [QUALITY-REVIEW](QUALITY-REVIEW.md)다.

| 포함 | 범위 |
|---|---|
| 규칙 | 헌법의 34개 DEV 유형과 프로젝트별 DOC-CONFIG. 30종 뒤에 넣은 유형은 DEV-15 용어집, DEV-64 위험및기술부채목록, DEV-66 장애공지, DEV-86 출시준비목록이다. 템플릿 파일명은 아래 목록과 같다 |
| 템플릿 | DEV 34종 + DOC-CONFIG 1종 |
| 문서 명세 | DEV 34종. 파일은 `_schemas/DEV-*.schema.json`이다. 범용 JSON Schema가 아니다 |
| 생성·갱신 | DEV-10·30만 지원 |
| lint | 34종 작성 문서와 light/full 필수 존재 |
| 예제 | 가상 HabitCheck; 실제 제품의 사실·코드 검증 근거가 아님 |
| 에이전트 연동 | CLI 호출 레시피만 이 저장소에 있다. 특정 앱의 설치 로그와 설정 값은 비어 있다. 확인은 그 앱에서 하고, 그 결과를 이 표에 옮겨 적지 않는다 |

카탈로그, 스키마, 템플릿이 서로 한 번씩 맞는지는 `python3 _tools/schema_sync_check.py --summary-only`가 본다.

템플릿 파일은 `_templates/`에 있다. 설정 양식은 `DOC-CONFIG.md`이다.

- `DEV-10-개요서.md`
- `DEV-12-제품로드맵.md`
- `DEV-15-용어집.md`
- `DEV-20-요구사항명세서.md`
- `DEV-22-인수조건명세서.md`
- `DEV-25-화면정의서.md`
- `DEV-28-UI문구명세서.md`
- `DEV-30-구조명세서.md`
- `DEV-32-모듈명세서.md`
- `DEV-35-데이터모델명세서.md`
- `DEV-38-데이터이전명세서.md`
- `DEV-40-API명세서.md`
- `DEV-42-이벤트메시지명세서.md`
- `DEV-45-설정명세서.md`
- `DEV-48-외부SaaS명세서.md`
- `DEV-50-기술결정기록.md`
- `DEV-52-기능플래그명세서.md`
- `DEV-55-보안명세서.md`
- `DEV-58-개인정보처리명세서.md`
- `DEV-60-운영절차서.md`
- `DEV-62-장애대응사례집.md`
- `DEV-64-위험및기술부채목록.md`
- `DEV-65-테스트명세서.md`
- `DEV-66-장애공지.md`
- `DEV-68-성능목표명세서.md`
- `DEV-70-구현작업명세서.md`
- `DEV-72-기술조사보고서.md`
- `DEV-75-코드작성규칙.md`
- `DEV-80-배포및장애절차서.md`
- `DEV-82-관측및알람명세서.md`
- `DEV-85-스토어제출명세서.md`
- `DEV-86-출시준비목록.md`
- `DEV-88-오픈소스라이선스목록.md`
- `DEV-90-릴리즈변경기록.md`

과거 작업일지의 Selection, GatewAI, Studio 상태는 현재 실행 조건이 아니다. 예전 버전 기록은 [과거 변경 이력](_history/VERSION-CHANGELOG-1.3.md)에 보관한다.

그 파일의 A–F 점수, GatewAI, Selection, DAY-SUMMARY, UNBLOCK-DF는 이 패키지가 정의하지 않는다. 그 이름들이 가리키는 파일도 현재 트리에 없다.

패키지는 외부 프로젝트 경로, 계정, 인증 상태를 추정하지 않는다.
