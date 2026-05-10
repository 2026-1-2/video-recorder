import logging
import crossplane
import os

logger = logging.getLogger()

def _get_common_conf_data(): # Parse "recorder.conf"
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    main_conf_path = os.path.join(base_path, 'config', 'recorder.conf')
    if (not os.path.exists(main_conf_path)):
        logger.error("recorder.conf does not exist.")
        exit(1)
    
    payload = crossplane.parse(main_conf_path)
    return payload

def getConfigAndCamInfo():
    using_DB = os.getenv("CAM_INFO_DB_ACTIVATE", "false")
    payload = _get_common_conf_data()
    global_conf = {item['directive']: item['args'][0] for item in payload['config'][0]['parsed'][0]['block'] }
    globalConfObj = globalConf(global_conf)
    camConfObjList = []

    if (str(using_DB).lower() in ("true", "1", "yes", "y", "on")):
        ## Get the information of camera from DB.
        pass
    else: ## Get the information of camera from disk. (.conf file)
        for conf in payload['config'][1:]:
            cam_conf = {item['directive']: item['args'][0] for item in conf['parsed'][0]['block'] }
            camConfObjList.append(camConf(cam_conf))

    return globalConfObj, camConfObjList

class globalConf:
    def __init__(self, confObj: dict):
        self.log_path = confObj.get('log_path')
        self.video_path = confObj.get('video_path')
    
class camConf:
    def __init__(self, confObj: dict):
        self.cam_name = confObj.get('cam_name')
        self.cam_ip = confObj.get('cam_ip')
        self.cam_port = confObj.get('cam_port')
        self.cam_path = confObj.get('cam_rtsp_path')
        self.username = confObj.get('username')
        self.password = confObj.get('password')
        self.video_interval_seconds = confObj.get('video_interval_seconds')
        self.file_ext = confObj.get('file_ext')
