# HabitCheck 가상 적용

이 폴더는 full 프로필로 배치한 가상 프로젝트다. 제품의 기준본이 아니다.

앱 코드와 `pubspec.lock`은 이 패키지에 없다. HC-REPO, HC-HASH, HC-PKG, HC-LEGAL. 34종 예제와 예제용 세팅은 [_examples/INDEX.md](../_examples/INDEX.md)에 있다. `_templates`와 `DEV-CONSTITUTION.md`를 제외한 `DEV-*.md`의 상태 필드는 `draft`다.

아래 표가 이 폴더에서 읽는 문서의 전부다. full 필수 DEV는 10·20·30·50·90이고, 선택 DEV는 22·35·40·48·70·85다. `DOC-CONFIG.md`는 세팅, `DEV-CONSTITUTION.md`와 `_templates/`는 패키지 복사본이다. archive는 표 밖이며 끝난 DEV-70을 둘 자리다.

| 경로 | 보여주는 것 |
|---|---|
| `DOC-CONFIG.md` | `docs_root`는 `demo-docs`, `required_profile`은 `full` |
| `DEV-10-개요서.md` | light 필수. 무엇·누구·경계·실행 |
| `DEV-30-구조명세서.md` | light 필수. 레이어와 의존 |
| `DEV-20-요구사항명세서.md` | full 추가 필수. 루트 단건 |
| `DEV-50-기술결정기록/DEV-50-로컬DB-drift.md` | full 추가 필수. 기록 1건. 결정 상태의 값은 HC-DRIFT-STATE. 주인은 `DEV-50-기술결정기록/DEV-50-로컬DB-drift.md`다. 「결정 없음」 인덱스가 아니다 |
| `DEV-90-릴리즈변경기록/DEV-90-v0.1.0.md` | full 추가 필수. 내부 APK v0.1.0. HC-HASH |
| `DEV-22-인수조건명세서/DEV-22-오늘체크.md` | 선택. 오늘 체크의 통과·실패 |
| `DEV-35-데이터모델명세서/DEV-35-습관체크인.md` | 선택. Habit·CheckIn |
| `DEV-40-API명세서/DEV-40-없음-v1.md` | 선택. v1 공개 HTTP API 없음 |
| `DEV-48-외부SaaS명세서/DEV-48-없음-v1.md` | 선택. v1 외부 SaaS 없음 |
| `DEV-70-구현작업명세서/DEV-70-001-오늘체크-유스케이스.md` | 선택. 오늘 체크 작업. 끝나면 archive로 옮긴다 |
| `DEV-85-스토어제출명세서/DEV-85-play-내부만.md` | 선택. 제출 결정은 그 파일 |
| `DEV-CONSTITUTION.md`, `_templates/` | 패키지 원본의 복사본 |

`_templates`와 패키지 `_templates`가 같은지는 저장소 루트의 `diff -rq _templates demo-docs/_templates`로 본다. 2026-10-13에 그 명령을 실행했을 때 출력이 없어, 그날은 두 트리가 같았다. 그 다음부터의 일치는 같은 명령을 다시 실행해 본다. 출력이 생기면 패키지 `_templates`를 기준으로 `demo-docs/_templates`를 맞춘다.

읽는 순서는 `DOC-CONFIG.md`에서 프로필, DEV-10에서 경계와 실행, DEV-20에서 Must, DEV-30에서 의존이다. HC-REPO, HC-DRIFT-VER, HC-HASH, HC-PKG, HC-LEGAL, HC-CHANNEL.

저장소 루트에서 검사한다.

```bash
python _tools/docs_lint.py demo-docs --summary-only
```

## 경로 검사에서 빠지는 곳

경로 검사에서 빠지는 위치는 [_schemas/README.md](../_schemas/README.md)와 같다.

| 빠지는 경로 | 이 폴더에서 |
|---|---|
| `archive/` | `archive/DEV-70-구현작업명세서/`는 끝난 DEV-70을 옮길 자리다. 문서는 아직 없다 |
| 이름이 `_`로 시작하는 디렉터리 | `_templates`가 해당한다. `_check`는 두지 않는다 |
| `DEV-CONSTITUTION.md` | 패키지 헌법의 복사본이라 제품 문서 검사에 넣지 않는다 |
