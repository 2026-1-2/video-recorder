# video-recorder 운영/트러블슈팅

> 24시간 연속 녹화(FFmpeg codec copy) 운영 관점 정리.

## 동작 개요
RTSP 입력을 FFmpeg로 받아 트랜스코딩 없이(codec copy) TS 세그먼트로 분할 저장한다.
Python은 영상 데이터를 직접 다루지 않고 FFmpeg 프로세스를 관리한다.

## 자주 발생하는 문제

### 녹화가 시작되지 않음
- RTSP URL/자격증명 확인 (`test_rtsp.py`로 연결 테스트)
- 입력 코덱이 컨테이너(TS)와 호환되는지 확인 (codec copy 전제)

### 세그먼트가 끊김 / 누락
- 카메라 네트워크 단절 → 재연결 로직/재시작 확인
- `ffprobe`로 세그먼트 타임스탬프 연속성 점검

### 프로세스가 죽은 뒤 재개되지 않음
- 프로세스 감시/자동 재시작 동작 확인
- 컨테이너 `restart` 정책 확인

### 디스크가 가득 참
- cleanup(순환 삭제) 임계치/주기 확인
- 자세한 내용: infra/TROUBLESHOOTING.md

## 점검 명령
```bash
python test_rtsp.py              # RTSP 연결 테스트
ffprobe <segment>.ts             # 세그먼트 메타/타임스탬프
docker compose logs video-recorder
```

## 테스트용 영상
- `make_test_videos.sh`로 테스트 스트림/영상 생성 가능 (카메라 없이 파이프라인 점검).
