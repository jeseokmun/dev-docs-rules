# DEV-75 코드작성규칙 — HabitCheck

| 필드 | 값 |
|---|---|
| 상태 | draft |
| 코드 | DEV-75 |
| 마지막 갱신 | 2026-10-13 |
| 범위 | 이 가상 앱의 포맷, 레이어, 비밀, Must의 테스트 근거 |
| 비범위 | 저장소 CI 파일의 실제 경로(아직 없음) |
| 관련 문서 | 아래 관련 문서 표 |

## ＊ 규칙
| 규칙 | 이유 | 예외 |
|---|---|---|
| 미결 1 | 포맷과 정적 분석을 맞춘다 | 없음 |
| Must(DEV-20 요구 1–3)는 요구마다 검증을 남긴다 | DEV-20 완료의 정의가 그렇게 나뉜다 | 없음 |
| DEV-30 | DEV-30 | 없음 |
| SECURITY | DEV-55 | 없음 |

## ○ 디렉터리·네이밍
| 대상 | 규칙 | 예외 |
|---|---|---|
| 레이어 폴더 | DEV-30의 presentation, application, domain, infrastructure 이름을 쓴다. 파일 경로는 아직 없다 | 없음 |

## ○ 관련 문서
| 코드 | 경로 |
|---|---|
| DEV-30 | `DEV-30-구조명세서.HabitCheck.md` |
| DEV-65 | `DEV-65-테스트명세서.HabitCheck.md` |
| DEV-20 | `DEV-20-요구사항.HabitCheck.md` |
| DEV-22 | `DEV-22-오늘체크.HabitCheck.md` |
| DEV-70 | `DEV-70-오늘체크.HabitCheck.md` |
| DEV-55 | `DEV-55-보안명세서.HabitCheck.md` |
| DEV-10 | `DEV-10-개요서.HabitCheck.md` |
## 미결
| ID | 미결 | 다음에 할 일 |
|---|---|---|
| 1 | CI 워크플로 파일 경로가 없다 | 파일이 생기면 포맷 규칙의 이유 칸에 그 잡이 `dart format`과 `flutter analyze`를 실행한다고 적는다. 예외 칸에 잡 이름을 넣지 않는다 |
