from datetime import datetime
import subprocess

AVAILABLE_FILE_EXT = ['ts']

class RTSPRecorder:
    def __init__(self, cam_name: str, cam_ipv4: str, cam_port: int = 554, cam_path: str = '', cam_username: str = '', cam_password: str = '',
                 output_file_dir: str = '/var/log/CCTV_monitoring/cam_rec_file', interval_sec: int = 3600, file_ext: str = 'ts'):
        self.cam_name = cam_name
        self.cam_ipv4 = cam_ipv4
        self.cam_port = cam_port
        self.cam_path = cam_path
        self.cam_username = cam_username
        self.cam_password = cam_password
        self.output_file_dir = output_file_dir
        self.interval_sec = interval_sec
        self.file_ext = file_ext

        self.process = None
        self.recording = False

    def __check_input(self):
        if (self.file_ext[0] == '.'):
            self.file_ext = self.file_ext[1:]
        if (not (self.file_ext in AVAILABLE_FILE_EXT)):
            raise ValueError(f"Unsupported File Extension: {self.file_ext}")
        
        if (self.cam_path[0] == '/'):
            self.cam_path = self.cam_path[1:] if len(self.cam_path) > 1 else ''
        
    def __gen_rtsp_URL(self):
        userinfo = f'{self.cam_username}:{self.cam_password}@' \
                    if (self.cam_username != '' and self.cam_password != '') else ''
        rtsp_URL = f'rtsp://{userinfo}{self.cam_ipv4}:{str(self.cam_port)}/{self.cam_path}'
        return rtsp_URL

    def start_recording(self):
        if (self.recording == True):
            return
        
        self.__check_input()
        rtsp_URL = self.__gen_rtsp_URL()

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
            '-segment_format', 'ts',
            '-strftime', '1',
            f'{self.output_file_dir}/{self.cam_name}/%Y%m%d_%H%M%S.{self.file_ext}'
            ]
        
        self.process = subprocess.Popen(cmd)
        self.recording = True
        print(f"Start Recording... (Camera Name: {self.cam_name}, Path: {self.output_file_dir})")

    def stop_recording(self):
        if (self.process is not None and self.recording == True):
            self.process.terminate()
            self.process.wait()
            self.recording = False
            print(f"Stop Recording... (Camera Name: {self.cam_name})")