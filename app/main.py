import logging
import os
import time
import datetime
import sys
import signal
from core import RTSPRecorder
from utils import get_conf_data, globalConf, camConf

Recorders = []
logger = logging.getLogger()

def parseConfig():
    payload = get_conf_data()
    global_conf = {item['directive']: item['args'][0] for item in payload['config'][0]['parsed'][0]['block'] }
    globalConfObj = globalConf(global_conf)
    camConfObjList = []
    for conf in payload['config'][1:]:
        cam_conf = {item['directive']: item['args'][0] for item in conf['parsed'][0]['block'] }
        camConfObjList.append(camConf(cam_conf))

    return globalConfObj, camConfObjList

def envSetup(globalConfObj: globalConf, camConfObjList: list[camConf]):
    ### Create missins directories ###
    target_dirs = {globalConfObj.log_path} | {globalConfObj.video_path}
    for camConfObj in camConfObjList:
        target_dirs.add(f"{globalConfObj.video_path}/{camConfObj.cam_name}")
    for dir in target_dirs:
        os.makedirs(name=dir, mode=0o750, exist_ok=True)

    ### Redirect stdout to log file ###
    fileNameTime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    generalLogName = f"{globalConfObj.log_path}/general-{fileNameTime}.log"
    errorLogName = f"{globalConfObj.log_path}/error-{fileNameTime}.log"


    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S'
    )

    logger.setLevel(logging.DEBUG)

    general_logger = logging.FileHandler(generalLogName, encoding='utf-8')
    general_logger.setLevel(logging.INFO)
    general_logger.setFormatter(formatter)

    error_file_obj = open(errorLogName, 'w', encoding='utf-8', buffering=1)
    sys.stderr = error_file_obj

    error_logger = logging.StreamHandler(error_file_obj)
    error_logger.setLevel(logging.ERROR)
    error_logger.setFormatter(formatter)

    logger.addHandler(general_logger)
    logger.addHandler(error_logger)


def signal_handler(signum, frame):
    logger.info(f"[System] Signal({signum}) received. Stopping all recordings...")
    for recObj in Recorders:
        recObj.stop_recording()

    logger.info(f"[System] All recordings stopped successfully. exit.\n")
    
    if sys.stderr is not sys.__stderr__:
        sys.stderr.close()
        
    os.system("stty echo")
    sys.exit(0)

if __name__ == '__main__':
    globalConfObj, camConfObjList = parseConfig()
    envSetup(globalConfObj=globalConfObj, camConfObjList=camConfObjList)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    for camConfObj in camConfObjList:
        recObj = RTSPRecorder(camConfObj=camConfObj, video_path=globalConfObj.video_path)
        recObj.start_recording()
        Recorders.append(recObj)

    while True:
        try:
            for recObj in Recorders:
                if ((recObj.process is not None) and (recObj.process.poll() is not None)):
                    logger.error(f"[Warn] Camera {recObj.cam_name} stopped unexpectedly...")
                    logger.error(f"[Warn] Camera {recObj.cam_name}: Attempting to restart...")

                    recObj.recording = False
                    recObj.start_recording()
                time.sleep(1)
        except Exception as e:
            logger.error(f'[ERROR] Watchdog loop encountered an exception: {e}')
            time.sleep(1)