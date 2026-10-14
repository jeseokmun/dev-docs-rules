# DEV-10 개요서 — HabitCheck

| 필드 | 값 |
|---|---|
| 상태 | draft |
| 코드 | DEV-10 |
| 마지막 갱신 | 2026-10-13 |
| 범위 | 무엇을 만드는지, 누구의 앱인지, 개발·설치 방법, v1에서 하지 않는 것 |
| 비범위 | API 계약(DEV-40), DB 엔진 선정(DEV-50), 화면 문구(DEV-28), 스토어 심사(DEV-85) |
| 관련 문서 | 아래 관련 문서 표 |

## ＊ 한 줄 소개
휴대폰에만 저장되는, 혼자 쓰는 습관 체크 앱이다. streak 계산은 `HC-STREAK` (`_examples/DEV-30-구조명세서.HabitCheck.md`)다.

## ○ 왜 필요한가
| 구분 | 내용 |
|---|---|
| 문제 | 습관 앱이 가입·소셜·광고를 요구하는 경우가 많음 |
| 접근 | 가입 없이 오늘 했는지와 streak만 본다. 계산은 한 줄 소개의 HC-STREAK다 |

## ＊ 누구를 위한가
| 구분 | 내용 |
|---|---|
| 사용자 | 혼자 운동·독서를 기록하려는 개인 |
| 비사용자 | 팀 챌린지·클라우드 동기화가 필요한 사람 |

## ＊ 핵심 기능
| # | 사용자가 하는 일 |
|---|---|
| 1 | 습관을 추가·수정·삭제. DEV-35 |
| 2 | 오늘 날짜에 체크/해제 |
| 3 | 습관별 streak 확인. 계산은 `HC-STREAK` (`_examples/DEV-30-구조명세서.HabitCheck.md`) |
| 4 | 이번 주 체크 횟수 요약 보기 |

## ＊ 실행·설치
| 구분 | 내용 |
|---|---|
| 개발 | HC-REPO |
| 사용자 | 내부 APK `dist/habitcheck-v0.1.0.apk` 를 사이드로드 |
| 환경 | Android 8.0+ · Flutter 3.22+ · Dart 3.4+. 이 숫자는 예제가 적은 하한이다 |

## ＊ 시스템 경계
| 하지 않는 것 | 이유 |
|---|---|
| 계정·클라우드 동기화 | 가입 없이 기기에만 저장하는 것이 접근 방법 |
| 친구·피드 | 사용자는 혼자 쓰는 사람이고, 팀 사용자는 비사용자 |
| iOS 동시 출시 | v1 실행 환경은 `HC-PLATFORM`(이 문서 ＊ 실행·설치의 환경 행)이다 |
| 리마인더 푸시 | DEV-20. DEV-40, DEV-55 |
| Health 연동 | 입력은 사용자의 체크뿐 |

## ○ 성공·검증
| 성공 모습 | 검증 방법 |
|---|---|
| 상세 streak가 `HC-STREAK` (`_examples/DEV-30-구조명세서.HabitCheck.md`)와 같다 | 1) 개발 행으로 실행한다. 2) 습관 하나를 추가한다. 3) DEV-70의 Clock 포트로 날짜를 바꾼다. DEV-35. CheckInToday를 호출한다. 4) 상세 streak와 CheckIn 건수를 그 정의와 비교한다. 휴대폰 시계로 날짜를 기다리는 절차는 아니다 |

## ○ 관련 문서
| 코드 | 경로 |
|---|---|
| DEV-20 | `DEV-20-요구사항.HabitCheck.md` |
| DEV-30 | `DEV-30-구조명세서.HabitCheck.md` |
| DEV-50 | `DEV-50-로컬DB-drift.HabitCheck.md` |
| DEV-65 | `DEV-65-테스트명세서.HabitCheck.md` |
| DEV-40 | `DEV-40-없음-v1.HabitCheck.md` |
| DEV-28 | `DEV-28-UI문구-목록.HabitCheck.md` |
| DEV-85 | `DEV-85-play-내부만.HabitCheck.md` |
| DEV-70 | `DEV-70-오늘체크.HabitCheck.md` |
| DEV-35 | `DEV-35-습관체크인.HabitCheck.md` |
| DEV-88 | `DEV-88-오픈소스라이선스목록.HabitCheck.md` |
| DEV-55 | `DEV-55-보안명세서.HabitCheck.md` |
| DEV-25 | `DEV-25-화면정의서-목록.HabitCheck.md` |

## 미결
| ID | 내용 |
|---|---|
| 1 | 없는 사실: HC-REPO. 다음 행동: 주소를 이 칸에 적지 않는다. |
| 2 | 없는 사실: HC-DRIFT-VER. 다음 행동: 그 번호를 환경 행에 적지 않는다. |
