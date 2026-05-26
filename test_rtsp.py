"""
RTSP 연결 사전 확인 스크립트
실행: python3 test_rtsp.py
"""
import subprocess
import sys

CAM_IP       = "HERE_CAMERA_IP"
CAM_PORT     = 554
RTSP_PATH    = "Streaming/Channels/101"
USERNAME     = "admin"
PASSWORD     = "HERE_CAMERA_PASSWORD"

url = f"rtsp://{USERNAME}:{PASSWORD}@{CAM_IP}:{CAM_PORT}/{RTSP_PATH}"
print(f"테스트 URL: rtsp://{USERNAME}:****@{CAM_IP}:{CAM_PORT}/{RTSP_PATH}")

result = subprocess.run(
    ["ffprobe", "-v", "error", "-rtsp_transport", "tcp",
     "-timeout", "5000000", url],
    capture_output=True, text=True, timeout=10
)

if result.returncode == 0:
    print("✅ RTSP 연결 성공 — 녹화 시작 가능")
else:
    print("❌ RTSP 연결 실패")
    print(result.stderr.strip())
    sys.exit(1)
