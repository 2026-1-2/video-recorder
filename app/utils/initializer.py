import datetime
import logging
import os
import sys
from .conf_parser import globalConf, camConf

logger = logging.getLogger()

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

    logger.info("Recorder Initialized...")
