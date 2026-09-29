# dev-docs-rules

AI와 함께 개발할 때 쓰는 **개발 문서 룰(헌법)과 문서 템플릿 모음**이다. 문서는 md(+Mermaid)로 쓰고, 표를 먼저 쓴다.

- 현재 버전: `VERSION` 파일 참고
- 필수 칸 표기: 템플릿에서 반드시 채워야 하는 섹션은 `＊`로 표시한다.
- 모르는 내용은 지어내지 않고 **미결**에 과제로 남긴다.

## 폴더 구성

| 경로 | 내용 |
|---|---|
| `DEV-CONSTITUTION.md` | 문서 헌법. 모든 문서가 따르는 규칙 |
| `DOC-CONFIG.md` | 프로젝트별 설정 양식 (`docs_root`, `required_profile` 등) |
| `_templates/` | 문서 템플릿 30종 + `DOC-CONFIG` 템플릿 (v2.1, 표 우선) |
| `_schemas/` | 템플릿별 JSON 스키마 30종 (템플릿과 1:1) |
| `_tools/` | 초안 생성·렌더·검사용 Python CLI |
| `_skills/` | 에이전트가 문서 초안·갱신·검사를 돌릴 때 쓰는 스킬 실행본 |
| `_examples/` · `demo-docs/` | 가상 앱 HabitCheck로 채운 예시 문서 (참고용, 기준본 아님) |
| `VERSION` · `VERSION-CHANGELOG.md` | 버전 태그와 변경 이력 |
| `PACKAGE-NOTES.md` | 작업 패키지 원본 README (내부 점검 폴더 경로가 남아 있음) |

## 템플릿 목록

`light`는 모든 프로젝트의 기본 필수, `full`은 full 프로필일 때 추가로 필수인 문서다. 나머지는 필요할 때 골라 쓴다.

| 번호 | 문서 | 프로필 | 템플릿 |
|---|---|---|---|
| DEV-10 | 개요서 | light | [`DEV-10-개요서.md`](_templates/DEV-10-개요서.md) |
| DEV-12 | 제품로드맵 | 선택 | [`DEV-12-제품로드맵.md`](_templates/DEV-12-제품로드맵.md) |
| DEV-20 | 요구사항명세서 | full | [`DEV-20-요구사항명세서.md`](_templates/DEV-20-요구사항명세서.md) |
| DEV-22 | 인수조건명세서 | 선택 | [`DEV-22-인수조건명세서.md`](_templates/DEV-22-인수조건명세서.md) |
| DEV-25 | 화면정의서 | 선택 | [`DEV-25-화면정의서.md`](_templates/DEV-25-화면정의서.md) |
| DEV-28 | UI문구명세서 | 선택 | [`DEV-28-UI문구명세서.md`](_templates/DEV-28-UI문구명세서.md) |
| DEV-30 | 구조명세서 | light | [`DEV-30-구조명세서.md`](_templates/DEV-30-구조명세서.md) |
| DEV-32 | 모듈명세서 | 선택 | [`DEV-32-모듈명세서.md`](_templates/DEV-32-모듈명세서.md) |
| DEV-35 | 데이터모델명세서 | 선택 | [`DEV-35-데이터모델명세서.md`](_templates/DEV-35-데이터모델명세서.md) |
| DEV-38 | 데이터이전명세서 | 선택 | [`DEV-38-데이터이전명세서.md`](_templates/DEV-38-데이터이전명세서.md) |
| DEV-40 | API명세서 | 선택 | [`DEV-40-API명세서.md`](_templates/DEV-40-API명세서.md) |
| DEV-42 | 이벤트메시지명세서 | 선택 | [`DEV-42-이벤트메시지명세서.md`](_templates/DEV-42-이벤트메시지명세서.md) |
| DEV-45 | 설정명세서 | 선택 | [`DEV-45-설정명세서.md`](_templates/DEV-45-설정명세서.md) |
| DEV-48 | 외부SaaS명세서 | 선택 | [`DEV-48-외부SaaS명세서.md`](_templates/DEV-48-외부SaaS명세서.md) |
| DEV-50 | 기술결정기록 | full | [`DEV-50-기술결정기록.md`](_templates/DEV-50-기술결정기록.md) |
| DEV-52 | 기능플래그명세서 | 선택 | [`DEV-52-기능플래그명세서.md`](_templates/DEV-52-기능플래그명세서.md) |
| DEV-55 | 보안명세서 | 선택 | [`DEV-55-보안명세서.md`](_templates/DEV-55-보안명세서.md) |
| DEV-58 | 개인정보처리명세서 | 선택 | [`DEV-58-개인정보처리명세서.md`](_templates/DEV-58-개인정보처리명세서.md) |
| DEV-60 | 운영절차서 | 선택 | [`DEV-60-운영절차서.md`](_templates/DEV-60-운영절차서.md) |
| DEV-62 | 장애대응사례집 | 선택 | [`DEV-62-장애대응사례집.md`](_templates/DEV-62-장애대응사례집.md) |
| DEV-65 | 테스트명세서 | 선택 | [`DEV-65-테스트명세서.md`](_templates/DEV-65-테스트명세서.md) |
| DEV-68 | 성능목표명세서 | 선택 | [`DEV-68-성능목표명세서.md`](_templates/DEV-68-성능목표명세서.md) |
| DEV-70 | 구현작업명세서 | 선택 | [`DEV-70-구현작업명세서.md`](_templates/DEV-70-구현작업명세서.md) |
| DEV-72 | 기술조사보고서 | 선택 | [`DEV-72-기술조사보고서.md`](_templates/DEV-72-기술조사보고서.md) |
| DEV-75 | 코드작성규칙 | 선택 | [`DEV-75-코드작성규칙.md`](_templates/DEV-75-코드작성규칙.md) |
| DEV-80 | 배포및장애절차서 | 선택 | [`DEV-80-배포및장애절차서.md`](_templates/DEV-80-배포및장애절차서.md) |
| DEV-82 | 관측및알람명세서 | 선택 | [`DEV-82-관측및알람명세서.md`](_templates/DEV-82-관측및알람명세서.md) |
| DEV-85 | 스토어제출명세서 | 선택 | [`DEV-85-스토어제출명세서.md`](_templates/DEV-85-스토어제출명세서.md) |
| DEV-88 | 오픈소스라이선스목록 | 선택 | [`DEV-88-오픈소스라이선스목록.md`](_templates/DEV-88-오픈소스라이선스목록.md) |
| DEV-90 | 릴리즈변경기록 | full | [`DEV-90-릴리즈변경기록.md`](_templates/DEV-90-릴리즈변경기록.md) |
| — | DOC-CONFIG | 설정 | [`DOC-CONFIG.md`](_templates/DOC-CONFIG.md) |

## 쓰는 법

### 1. 프로젝트에 문서 폴더 만들기

1. 프로젝트 안에 문서 폴더(`docs_root`, 예: `docs/`)를 만든다.
2. `DEV-CONSTITUTION.md`를 복사하고, `_templates/DOC-CONFIG.md`로 `DOC-CONFIG.md`를 만든다.
3. `DOC-CONFIG.md`에 `docs_root`와 `required_profile`(`light` 또는 `full`, 기본 `light`)을 적는다.

### 2. 필수 문서부터 초안 쓰기

1. light면 `DEV-10 개요서`, `DEV-30 구조명세서`부터 쓴다. full이면 `DEV-20`, `DEV-50`, `DEV-90`을 더한다.
2. `_templates/`에서 해당 템플릿을 `docs_root`로 복사한다.
3. 첫 목표는 `＊` 섹션만 채우는 것이다. 처음부터 완벽하게 채울 필요는 없다.
4. 확인하지 않은 사실은 쓰지 않는다. 대신 **미결** 표에 과제로 남긴다.
5. 나머지 템플릿은 필요해질 때 추가한다.

### 3. CLI로 초안 만들고 검사하기 (선택)

Python 3만 있으면 된다. 저장소 루트에서 실행한다.

```bash
# 값(JSON)으로 템플릿을 채워 md 생성
python3 _tools/render_doc.py --help

# DEV-10·30 초안 생성 / 기존 문서 갱신
python3 _tools/docs_draft_cli.py --help
python3 _tools/docs_refresh_cli.py --help

# ＊ 섹션 누락·빈칸·비밀값 의심 문자열 검사
python3 _tools/docs_lint.py docs/ --summary-only

# 템플릿과 스키마가 서로 맞는지 검사
python3 _tools/schema_sync_check.py --summary-only
```

도구별 설명은 `_tools/README.md`에 있다. `quality_regress_check.py`, `regress_docs_pipeline.py`, `plant_light_preflight.py`는 작업 환경의 점검 폴더와 로컬 경로를 기본값으로 쓰는 내부 회귀용이라, 이 저장소만으로는 경로 인자를 직접 넘겨야 한다.

### 4. 규칙 요약

| 규칙 | 내용 |
|---|---|
| 기준본 | `docs_root` 안의 md가 유일한 기준본이다. 값 JSON은 임시이고 저장하지 않는다. |
| 필수 표기 | 필수 칸은 `＊` (★ 쓰지 않음) |
| 성숙도 | 첫 초안은 `＊`만 통과하면 된다. 리뷰에서 보완 요청을 낸다. |
| 모르는 것 | 지어내지 말고 미결로 남긴다. |
| 형식 | md + Mermaid, 표 우선 |

자세한 규칙은 `DEV-CONSTITUTION.md`를 본다.
