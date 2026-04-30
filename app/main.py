import os
import time
import sys
import signal
from core import RTSPRecorder

CAM_NAME = [ 'Cam1A', 'Cam1B', 'Cam2' ]
CAM_ADDR = 
CAM_PORT = 
CAM_PATH = 
CAM_USERNAME = 
CAM_PASSWORD = 
OUTPUT_FILE_DIR = 
INTERVAL_SEC = '60'
FILE_EXT = '.ts'

def __parseConfig():
    pass

def __envSetup():
    for i in range(len(CAM_NAME)):
        targetDir = os.path.join(OUTPUT_FILE_DIR, CAM_NAME[i])
        if (not os.path.exists(targetDir)):
            os.makedirs(name=targetDir, mode=0o750, exist_ok=True)

Recorders = []

def signal_handler(signum, frame):
    print(f"[System] Signal({signum}) received. Stopping all recordings...")
    for recObj in Recorders:
        recObj.stop_recording()
    print("[System] All recordings stopped successfully. exit.")
    sys.exit(0)

if __name__ == '__main__':
    __envSetup()
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    for i in range(len(CAM_NAME)):
        recObj = RTSPRecorder(cam_name=CAM_NAME[i], cam_ipv4=CAM_ADDR[i], cam_port=CAM_PORT[i], cam_path=CAM_PATH[i], cam_username=CAM_USERNAME, cam_password=CAM_PASSWORD[i],
                       output_file_dir=OUTPUT_FILE_DIR, interval_sec=INTERVAL_SEC, file_ext=FILE_EXT)
        recObj.start_recording()
        Recorders.append(recObj)

    while True:
        try:
            for recObj in Recorders:
                if ((recObj.process is not None) and (recObj.process.poll() is not None)):
                    print(f"[Warn] Camera {recObj.cam_name} stopped unexpectedly...")
                    print(f"[Warn] Camera {recObj.cam_name}: Attempting to restart...")

                    recObj.recording = False
                    recObj.start_recording()
                time.sleep(1)
        except Exception as e:
            print(f'[ERROR] Watchdog loop encountered an exception: {e}')
            time.sleep(1)