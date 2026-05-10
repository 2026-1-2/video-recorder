import logging
import os
import time
import sys
import signal
from core import RTSPRecorder
from utils import getConfigAndCamInfo, envSetup
Recorders = []
logger = logging.getLogger()
shutdown_flag = False
signumVar = -1

def signal_handler(signum, frame):
    global shutdown_flag
    global signumVar

    shutdown_flag = True
    signumVar = signum

if __name__ == '__main__':
    globalConfObj, camConfObjList = getConfigAndCamInfo()
    envSetup(globalConfObj=globalConfObj, camConfObjList=camConfObjList)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    for camConfObj in camConfObjList:
        recObj = RTSPRecorder(camConfObj=camConfObj, video_path=globalConfObj.video_path)
        recObj.start_recording()
        Recorders.append(recObj)

    while shutdown_flag == False:
        try:
            for recObj in Recorders:
                if (shutdown_flag == True):
                    break
                if ((recObj.process is not None) and (recObj.process.poll() is not None)):
                    logger.error(f"Camera {recObj.cam_name} stopped unexpectedly...")
                    logger.error(f"Camera {recObj.cam_name}: Attempting to restart...")

                    recObj.recording = False
                    recObj.start_recording()
                time.sleep(1)
        except Exception as e:
            logger.error(f'Watchdog loop encountered an exception: {e}')
            time.sleep(1)

    logger.warning(f"Signal({signumVar}) received. Stopping all recordings...")
    for recObj in Recorders:
        recObj.stop_recording()

    logger.warning(f"All recordings stopped successfully. exit.\n")

    logging.shutdown()
    if sys.stderr is not sys.__stderr__:
        sys.stderr.close()