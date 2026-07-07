# gong_rc_2026 프로젝트 개요 및 시스템 분석

## 1. 프로젝트 개요

이 코드는 RC카에서 실시간 원격 조작 + 조도센서(CDS) 데이터를 동시에 수집하는 시스템이다. 이전 버전에서 있던 카메라 스트리밍 기능을 완전히 제거하고, 주행 제어와 오도메트리+CDS 로깅에만 집중한 경량화 버전이다.

핵심 목표:
- 트랙을 한 바퀴 주행하면서 동시에 CDS(조도) 값을 위치별로 매핑해서 CSV로 저장

---

## 2. 시스템 구성

### 2.1 하드웨어 구조

```
[웹 브라우저 UI] --HTTP--> [Flask 서버]
                                  ├─ pop.Pilot.AutoCar() → 모터/조향 제어
                                  └─ Arduino Uno (Serial, /dev/ttyUSB1, 9600bps) → CDS 조도값 읽기
```

이 코드는 CDS 센서를 별도의 Arduino Uno가 읽어서 시리얼로 전송하는 방식으로 변경되어 있다. `pop.Cds` 클래스는 주석 처리되어 있고, 대신 `ArduinoUnoCdsFast9600`이라는 커스텀 클래스가 그 역할을 대체한다.

### 2.2 소프트웨어 계층

| 레이어 | 역할 |
|---|---|
| `ArduinoUnoCdsFast9600` | 별도 스레드로 시리얼 포트를 논블로킹(`timeout=0`)으로 계속 폴링, 줄바꿈 단위로 정수값 파싱 |
| `_log_and_odometry_loop` | 0.05초 간격으로 위치 계산 + CDS 값 읽기 + 로그 적재 (별도 스레드) |
| Flask 서버 | `/api/control`, `/api/telemetry`, `/` 세 개 엔드포인트로 UI와 통신 |
| 웹 UI (HTML/JS) | WASD 버튼(마우스+키보드), START/SAVE 버튼, canvas 실시간 궤적 시각화 |

전체적으로 **3개의 스레드**가 동시에 동작한다:
1. Flask 서버 스레드 (`run_server`)
2. Arduino 시리얼 리더 스레드 (`_reader_loop`)
3. 오도메트리+로깅 스레드 (`_log_and_odometry_loop`, START~SAVE 사이에만 존재)

---

## 3. 데이터 수집 방법

### 3.1 주행 제어 흐름

- 브라우저에서 W/A/S/D 버튼을 누르면(`onmousedown` / `ontouchstart`) `startCmd()` → `/api/control`로 POST
- 손을 떼면(`onmouseup`) `stopCmd()` → `command: "stop"` 전송
- 서버는 `car.forward()`, `car.backward()`, `car.steering` 값을 즉시 적용하면서, 동시에 오도메트리 계산용 전역 변수(`current_v_cmd`, `current_steer_rad`)도 갱신

실제 모터 명령과 오도메트리 계산이 같은 변수를 공유하는 구조이므로, 조향각(`STEER_ANGLE_DEG = 20도`)이나 속도(`DRIVE_SPEED = 100`)는 "명령값"이지 실측값이 아니라는 점에 유의해야 한다.

### 3.2 CDS 값 수집

- Arduino가 조도값을 시리얼로 한 줄씩(`\n` 구분) 전송
- `_reader_loop`가 버퍼링하며 파싱 → `self.last_value`에 최신값 저장
- 로깅 루프는 매 샘플마다 `cds.read()`로 최신값을 가져와 위치와 함께 기록

### 3.3 저장 형식

`START` 명령 시 위치 초기화(0, 0, 0) + 로그 초기화, `SAVE` 명령 시 스레드 종료 대기 후 CSV로 저장한다.

CSV 컬럼 구성:
```
timestamp, elapsed_sec, pos_x, pos_y, heading_deg, cds_raw
```

샘플링 주기는 `SAMPLE_INTERVAL = 0.05`초 (20Hz)이다.

### 3.5 실시간 시각화

웹 UI는 100ms마다 `/api/telemetry`를 폴링해서 canvas에 점을 찍는다. CDS 값을 hue(색상)로 매핑(`hue = cds/1024 * 240`)해서 트랙 위 조도 분포를 색깔로 시각화한다.

---

### 4 결론

이번 코드는 카메라 스트리밍을 제거하고 **주행 제어 + 조도 센서 로깅**이라는 핵심 기능에만 집중한 경량화된 데이터 수집 시스템으로, 이전 pywebview 기반 구조에서 Flask 웹서버 기반 구조로 전환하며 환경에 맞게 아키텍처를 재설계하였다.

하지만 다음 세 가지가 해결되어야 한다:

1. **캘리브레이션 상수 실측** — `WHEEL_BASE(0.15m)`와 `SPEED_CONSTANT(0.01)`는 하드코딩된 추정값이므로, 실제 차량의 축거를 자로 측정하고, 알려진 거리를 주행시켜 속도 환산 계수를 역산하는 검증 과정이 필요하다.
2. **CDS 센서 연동 방식 검증** — 기존 `pop.Cds` 클래스 대신 Arduino를 거치는 시리얼 통신 방식으로 변경되었으므로, 조도값이 채널 3번 문제없이 정상적으로 수신·파싱되는지, 특히 값의 변동 폭이 실제 트랙 명암을 잘 반영하는지 별도 확인이 필요하다.
3. **오도메트리 오차 누적 문제** — Dead Reckoning 특성상 주행 시간이 길어질수록 위치 오차가 누적되므로, 짧은 구간 단위로 나눠 주행하거나 랩(lap) 완주 후 시작점 복귀 여부로 오차를 검증하는 방식이 권장된다.

이 세 가지가 보정되면, CSV로 저장된 `(x, y, heading, cds_raw)` 데이터를 활용해 트랙 상의 조도 분포 지도를 만들거나, 향후 라인트레이싱 알고리즘의 기초 데이터로 활용할 수 있을 것으로 기대한다.
