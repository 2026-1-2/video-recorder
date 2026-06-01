import subprocess
import logging
import sys
from utils import camConf

class RTSPRecorder:
    def __init__(self, camConfObj: camConf, video_path: str, ext: list[str] | None = None):
        self.cam_name = camConfObj.cam_name
        self.cam_ipv4 = camConfObj.cam_ip
        self.cam_port = camConfObj.cam_port
        self.cam_path = camConfObj.cam_path
        self.cam_username = camConfObj.username
        self.cam_password = camConfObj.password
        self.output_file_dir = video_path
        self.interval_sec = camConfObj.video_interval_seconds
        self.file_ext = camConfObj.file_ext
        self.avail_ext_list = ext if ext is not None else [".ts"]
        self.logger = logging.getLogger()

        self.process = None
        self.recording = False

    def _check_input(self):
        if (not (self.file_ext in self.avail_ext_list)):
            raise ValueError(f"Unsupported File Extension: {self.file_ext}")
        
        if (self.cam_path[0] == '/'):
            self.cam_path = self.cam_path[1:] if len(self.cam_path) > 1 else ''
        
    def _gen_rtsp_URL(self):
        userinfo = f'{self.cam_username}:{self.cam_password}@' \
                    if (self.cam_username != '' and self.cam_password != '') else ''
        rtsp_URL = f'rtsp://{userinfo}{self.cam_ipv4}:{str(self.cam_port)}/{self.cam_path}'
        return rtsp_URL
    
    def start_recording(self):
        if (self.recording == True):
            return
        
        self._check_input()
        rtsp_URL = self._gen_rtsp_URL()

        mp4_opts = ['-segment_format_options', 'movflags=frag_keyframe+empty_moov+default_base_moof'] \
                   if self.file_ext == 'mp4' else []
        cmd = [
            'ffmpeg',
            '-loglevel', 'error',
            '-fflags', '+genpts',
            '-use_wallclock_as_timestamps', '1',
            '-rtsp_transport', 'tcp',
            '-timeout', '10000000',
            '-i', rtsp_URL,
            '-c', 'copy',
            '-f', 'segment',
            '-segment_time', str(self.interval_sec),
            '-segment_format', self.file_ext,
            *mp4_opts,
            '-strftime', '1',
            f'{self.output_file_dir}/{self.cam_name}/%Y%m%d_%H%M%S.{self.file_ext}'
            ]
        
        self.process = subprocess.Popen(cmd, stderr=sys.stderr)
        self.recording = True
        self.logger.info(f"Start Recording... (Camera Name: {self.cam_name}, Path: {self.output_file_dir}/{self.cam_name})")

    def stop_recording(self):
        if (self.process is not None and self.recording == True):
            self.process.terminate()
            self.process.wait()
            self.recording = False
            self.logger.info(f"Stop Recording... (Camera Name: {self.cam_name})")