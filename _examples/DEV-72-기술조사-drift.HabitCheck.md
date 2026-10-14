# DEV-72 기술조사보고서 — drift 적합성

| 필드 | 값 |
|---|---|
| 상태 | draft |
| 코드 | DEV-72 |
| 마지막 갱신 | 2026-10-13 |
| 범위 | HabitCheck 로컬 SQL 조사. 채택 상태는 `HC-DRIFT-STATE` (`_examples/DEV-50-로컬DB-drift.HabitCheck.md`). HC-DRIFT-VER |
| 비범위 | 테이블 정의(DEV-35), 채택 상태는 `HC-DRIFT-STATE` (`_examples/DEV-50-로컬DB-drift.HabitCheck.md`) |
| 관련 문서 | 아래 승격 표 |

이 저장소에는 앱 코드와 `pubspec.lock`이 없다. 호환 사례 개수는 확인하지 않았다. HC-DRIFT-VER.

## ＊ 조사
| 질문 | 조사결과 | 채택/기각 |
|---|---|---|
| 로컬 SQL 후보의 근거로 확인한 것은 무엇인가 | DEV-50의 이유는 컴파일 타임 타입과 마이그레이션 경로다. 환경 하한은 `HC-PLATFORM` (`_examples/DEV-10-개요서.HabitCheck.md`). HC-DRIFT-VER | 추가조사. 채택 상태는 `HC-DRIFT-STATE` (`_examples/DEV-50-로컬DB-drift.HabitCheck.md`). 이 칸은 그 문장을 다시 쓰지 않는다 |

## ＊ 사실 vs 추측
| 종류 | 내용 |
|---|---|
| 사실 | 이 패키지 안에 HabitCheck 구현과 잠금 파일이 없다(DEV-50 맥락) |
| 사실 | DEV-50이 든 채택 이유는 타입과 마이그레이션이지, 측정된 학습 시간이 아니다 |
| 추측 | DEV-50의 되돌리는 조건이 1일을 기준으로 삼았을 뿐, 학습 시간을 재지는 않았다 |

## 승격
| 대상 | 내용 |
|---|---|
| DEV-50 | 상태는 `HC-DRIFT-STATE` (`_examples/DEV-50-로컬DB-drift.HabitCheck.md`). 이 조사는 그 기록의 입력이다 |

## 종료
| 항목 | 내용 |
|---|---|
| archive | 스파이크가 끝나면 `{docs_root}/archive/DEV-72-기술조사보고서/`로 옮기고, 남는 결정은 DEV-50에만 둔다 |

## 관련 문서
| 코드 | 경로 |
|---|---|
| DEV-35 | `DEV-35-습관체크인.HabitCheck.md` |
| DEV-50 | `DEV-50-로컬DB-drift.HabitCheck.md` |
| DEV-10 | `DEV-10-개요서.HabitCheck.md` |

## 미결
| ID | 미결 | 다음에 할 일 |
|---|---|---|
| 1 | 스파이크 날짜는 아직 없다. HC-DRIFT-VER | DEV-50 미결이 닫히면 조사결과의 버전 칸을 그 기록에 맞춘다 |
