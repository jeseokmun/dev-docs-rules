# DEV-70 구현작업명세서 — 오늘체크 유스케이스

| 필드 | 값 |
|---|---|
| 상태 | draft |
| 코드 | DEV-70 |
| 마지막 갱신 | 2026-10-13 |
| 범위 | application의 오늘체크와 도메인 streak를 연결하는 작업. streak는 `HC-STREAK` (`_examples/DEV-30-구조명세서.HabitCheck.md`)다 |
| 비범위 | 화면 픽셀, `HC-DRIFT-STATE` (`_examples/DEV-50-로컬DB-drift.HabitCheck.md`), `HC-PLATFORM` (`_examples/DEV-10-개요서.HabitCheck.md`) |
| 관련 문서 | 아래 관련 표 |

## ＊ 목표 / 비범위
| 구분 | 내용 |
|---|---|
| 목표 | 체크하면 체크인이 저장된다. DEV-10. 상세에 쓸 streak는 `HC-STREAK` (`_examples/DEV-30-구조명세서.HabitCheck.md`). 이 칸은 그 문장을 다시 쓰지 않는다 |
| 비범위 | 화면 위젯 |
| 비범위 | 마이그레이션 파일 작성(DEV-38) |
| 비범위 | 주간 요약 집계(DEV-20 요구 4) |

## ＊ 사실 · 추측 · 미결
| 종류 | 내용 |
|---|---|
| 사실 | DEV-30 |
| 사실 | DEV-20 요구 2·3 |
| 추측 | 날짜를 자르는 시각은 기기 로컬 자정으로 둔다. DEV-30 streak 정의는 이 시각을 확정하지 않았다. DEV-50의 결정도 아니다 |
| 미결 | 없는 사실: 인터페이스만 두고 어댑터를 스텁으로 둘 수 있는지는 스파이크 전이라 정하지 않았다. 다음 행동: DB 상태는 `HC-DRIFT-STATE` (`_examples/DEV-50-로컬DB-drift.HabitCheck.md`). 그 기록을 본 뒤에 이 칸을 고친다 |

## ＊ 완료 조건
| # | 조건 |
|---|---|
| 1 | DEV-22 AC-2 |
| 2 | 반환 streak는 `HC-STREAK` (`_examples/DEV-30-구조명세서.HabitCheck.md`)와 같다 |
| 3 | DEV-30 |

## ＊ 검증
| # | 방법 |
|---|---|
| 1 | 단위 테스트: 같은 날 두 번 호출 → CheckIn 1건 |
| 2 | 단위 테스트: 연속 체크의 streak는 `HC-STREAK` (`_examples/DEV-30-구조명세서.HabitCheck.md`). 시나리오 위치는 DEV-65 |
| 3 | DEV-22 미결 |

## ＊ 금지
| 금지 | 이유 |
|---|---|
| DEV-30 | DEV-30 |
| 계정·동기화 코드 경로 | DEV-10·DEV-20 비범위 |

## ○ 관련
| 종류 | 링크 |
|---|---|
| DEV-22 | `DEV-22-오늘체크.HabitCheck.md` |
| DEV-30 | `DEV-30-구조명세서.HabitCheck.md` |
| DEV-20 | `DEV-20-요구사항.HabitCheck.md` |
| DEV-50 | `DEV-50-로컬DB-drift.HabitCheck.md` |
| DEV-38 | `DEV-38-데이터이전-없음.HabitCheck.md` |
| DEV-65 | `DEV-65-테스트명세서.HabitCheck.md` |
| DEV-10 | `DEV-10-개요서.HabitCheck.md` |
| DEV-45 | `DEV-45-설정명세서.HabitCheck.md` |
| DEV-35 | `DEV-35-습관체크인.HabitCheck.md` |
## 구현 메모
| 항목 | 내용 |
|---|---|
| Clock 포트 | 테스트에서 날짜를 고정한다. DEV-35. DEV-45 `CLOCK_MODE`, DEV-65 |

## 승격
| 대상 | 내용 |
|---|---|
| DEV-50 | 날짜 경계가 확정되면 DEV-50에 근거를 추가 |
| DEV-20 | 요구가 바뀌면 DEV-20을 먼저 수정 |

## 종료
| 항목 | 내용 |
|---|---|
| archive | 작업이 끝나면 `{docs_root}/archive/DEV-70-구현작업명세서/`로 옮긴다 |
