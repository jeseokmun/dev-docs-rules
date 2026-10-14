# DEV-32 모듈명세서 — application

| 필드 | 값 |
|---|---|
| 상태 | draft |
| 코드 | DEV-32 |
| 마지막 갱신 | 2026-10-13 |
| 범위 | application 레이어의 책임, 공개 함수 둘, DEV-30이 허용한 의존 |
| 비범위 | 화면 위젯, SQL 문장, `HC-DRIFT-STATE` (`_examples/DEV-50-로컬DB-drift.HabitCheck.md`) |
| 관련 문서 | 아래 관련 문서 표 |

## ＊ 모듈
| 모듈 | 책임 | 입력 | 출력 |
|---|---|---|---|
| application | 하는 일: 유스케이스 순서 조율. 하지 않는 일: UI, SQL 직접 작성 | DEV-35 | CheckInToday의 streak는 `HC-STREAK` (`_examples/DEV-30-구조명세서.HabitCheck.md`). 타입 이름은 미정 |

## ＊ 공개 인터페이스
| 이름 | 종류 | 입력 | 출력 |
|---|---|---|---|
| CheckInToday | 함수 | DEV-35 | streak는 `HC-STREAK` (`_examples/DEV-30-구조명세서.HabitCheck.md`). 이 칸은 그 문장을 다시 쓰지 않는다. 시그니처 타입은 미정 |
| AddHabit | 함수 | DEV-35 | 반환 타입 이름은 미정 |

## ＊ 의존
| 대상 | 방향 | 허용? | 설명 |
|---|---|---|---|
| domain | 이 모듈 → 대상 | 허용 | DEV-30 |
| infrastructure 포트 | 이 모듈 → 대상 | 허용 | DEV-30 |

## ＊ 건드리기 위험
| 구역 | 영향 | 경로(□) |
|---|---|---|
| 날짜 경계를 유스케이스에 하드코딩 | `HC-MIDNIGHT` (`_examples/DEV-70-오늘체크.HabitCheck.md`)와 어긋날 수 있다(DEV-30 위험 구역) | 파일 없음. DEV-30도 경로 후보를 정하지 않았다 |

## ○ 불변조건·실패 시
| 조건 | 실패 시 |
|---|---|
| DEV-22 AC-2 | DEV-22 AC-2 |

## ○ 관련 문서
| 코드 | 경로 |
|---|---|
| DEV-30 | `DEV-30-구조명세서.HabitCheck.md` |
| DEV-70 | `DEV-70-오늘체크.HabitCheck.md` |
| DEV-50 | `DEV-50-로컬DB-drift.HabitCheck.md` |
| DEV-35 | `DEV-35-습관체크인.HabitCheck.md` |
| DEV-22 | `DEV-22-오늘체크.HabitCheck.md` |
## 미결
| ID | 미결 | 다음에 할 일 |
|---|---|---|
| 1 | 포트 인터페이스와 반환 타입의 파일 경로·이름이 없다 | 파일이 생기면 위험 표의 경로와 공개 인터페이스의 출력 칸을 그 이름으로 바꾼다 |
