# dumb-fuzzer

Mutation-based Dumb Fuzzer — 범용 바이너리 퍼저

## 소개

바이너리 프로그램의 취약점을 자동으로 탐색하는 Mutation-based Dumb Fuzzer입니다.
시드 파일 또는 랜덤 바이트 데이터를 기반으로 변이를 수행하고, 타겟 프로그램의 비정상 종료(Crash)를 감지합니다.

## 기능

- **이중 퍼징 모드**: 시드 파일 기반 모드 / 랜덤 데이터 기반 모드
- **4가지 Mutation Operator**
  - Byte Flip: 랜덤 위치의 바이트를 무작위 값으로 치환
  - Byte Insert: 랜덤 위치에 무작위 바이트 삽입
  - Byte Delete: 랜덤 위치의 바이트 삭제
  - Byte Duplicate: 랜덤 블록을 복제하여 삽입
- **변이 강도 조절**: 0.1% ~ 20%
- **Crash 탐지**: SIGSEGV / SIGABRT / SIGBUS / SIGILL / SIGFPE
- **자동 로깅**: Crash 발생 시 입력 파일을 `crash/` 폴더에 타임스탬프와 함께 저장
- **무중단 운영**: 예외 처리 및 타임아웃(1초) 적용으로 안정적인 장시간 퍼징 지원

## 사용법

```bash
python3 dumb_fuzzer.py
```

실행 후 아래 항목을 입력합니다.

```
타겟 바이너리 경로: ./target
시드 파일을 사용하시겠습니까? (y/n): y
시드 파일 폴더 경로: ./seeds
시드 파일 확장자 입력 (전체 선택은 엔터):
변이 강도 선택 (1: 0.1%, 2: 1%, 3: 5%, 4: 10%, 5: 20%): 2
```

## 실행 결과 예시

```
[*] Fuzzing 시작 | 타겟: ./target
[*] 실행 횟수: 50회 진행 중...
[!!!] CRASH DETECTED | Signal=SIGSEGV | Saved=./crash/bug_1234567890.crash
```

## 디렉토리 구조

```
dumb-fuzzer/
├── dumb_fuzzer.py   # 퍼저 메인 코드
├── crash/           # Crash 입력 파일 저장 (자동 생성)
└── tmp/             # 임시 파일 저장 (자동 생성)
```

## 요구사항

- Python 3.6 이상
- Linux / WSL 환경
