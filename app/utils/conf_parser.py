import crossplane
import os
import glob

def get_conf_data():
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    main_conf_path = os.path.join(base_path, 'config', 'recorder.conf')
    payload = crossplane.parse(main_conf_path)
    return payload

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
