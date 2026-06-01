# video-recorder
- CCTV로부터 RTSP 영상을 수신받아 하드디스크에 저장하는 Docker 컨테이너입니다.

## 실행 방법
### 1. Docker Image 빌드
```
docker build -t <container-name>:<tag> .
```
- e.g) docker build -t video-recorder:latest .
  
### 2. 공통 설정값  작성 (Optional)
- video-recorder 프로그램에 대한 환경 설정을 config/recorder.conf 파일에 작성합니다.
- 각 설정값은 반드시 세미콜론(;)으로 끝나야 하며, 값의 종류에 관계없이 작은따옴표(') 및 큰따옴표(")는 사용하지 않습니다.
  
#### [공통 설정파일 옵션 설명 - system block 내부]
- log_path: 본 프로그램의 작동 로그가 저장되는 경로입니다.
- video_path: 카메라로부터 녹화된 영상이 저장되는 경로입니다.
  
#### [공통 설정파일 옵션 설명 - system block 외부]
- 카메라 접속 정보를 담은 설정파일을 include 할 수 있습니다.

### 3. 카메라 연결 정보 작성
- 연결할 카메라의 접속 정보를 config/example.conf 파일에 작성합니다.
- conf 파일 이름은 자유롭게 변경 가능합니다.
- 연결해야 할 카메라가 여러 대인 경우, 카메라 수 만큼 example.conf를 복사하여 사용하는 것을 권장합니다.
- 사용하지 않는 설정 파일은 삭제하여 주십시오.
```
cd config
cp example.conf <Camera Name>.conf
...
rm example.conf
```
#### [카메라 연결 설정파일 옵션 설명]
- cam_name: 카메라 이름 / 각 카메라의 영상을 서로 다른 디렉토리에 저장하는데, 각 디렉토리의 이름은 여기에 설정된 값으로 지정됩니다.
- cam_ip: 카메라 IPv4 주소 / 서버에서 카메라에 접속할 수 있도록 미리 조치하시기 바랍니다.
- cam_port: 카메라에 설정된 RTSP 포트 번호 (기본값 554)
- cam_rtsp_path: 카메라의 RTSP 엔드포인트 주소 / 카메라 제조사별로 상이하므로, 메뉴얼을 통해 엔드포인트 주소를 미리 확인하시기 바랍니다.
- username: 카메라 접근을 위한 계정의 UserName / 카메라 관리 페이지에서 설정한 값을 입력하십시오.
- password: 카메라 접근을 위한 계정의 비밀번호 / 카메라 관리 페이지에서 설정한 값을 입력하십시오.
- video_interval_seconds: 녹화 영상을 분할하기 위한 기준 시간 (단위: "초") / 기본값 3600 (1시간 간격으로 파일을 분할하여 저장)
- file_ext: 녹화 영상의 확장자 / 별도의 이유가 없다면 기본값(.ts) 적용을 권장합니다.
  
### 3. 환경변수 작성 (컨테이너로 배포하는 경우)
```
   cp video-recorder.env.sample .video-recorder.env
```
#### [환경변수명 설명]
- VIDEO_RECORDER_CONT_NAME: 컨테이너 이름
- VIDEO_RECORDER_IMG_NAME: 컨테이너 이미지 이름(경로) / Image 빌드 시 사용하였던 container-name과 tag 사용 (e.g. video-recorder:latest)
- VIDEO_RECORDER_LOG_PATH_ROOT: 본 프로그램의 로그 저장 경로
- VIDEO_RECORDER_CONF_PATH_ROOT: 본 프로그램의 설정 파일 저장 경로 / 입력된 경로는 camera 디렉토리 및 recorder.conf의 상위 디렉토리여야 합니다.
- VIDEO_RECORDER_VIDEO_PATH_ROOT: 녹화 영상 저장 경로
- DISK_CAPACITY_CHECK_INTERVAL: 디스크의 여유 공간을 체크할 간격(초) / 입력된 간격마다 여유 공간을 체크합니다. 여유 공간이 10% 미만인 경우, 여유 공간이 40% 이상 확보될 때 까지 가장 오래된 영상을 삭제합니다. (main.py 및 utils/video_manager.py 참조)
- AVAILABLE_FILE_EXT: 영상 확장자 / 카메라마다 서로 다른 확장자를 사용한다면, 사용되는 모든 확장자를 본 변수에 지정하여야 합니다. (ex. ".mp4, .ts") 별다른 사유가 없다면 .ts 사용을 권장합니다. 반드시 "."을 포함하여 작성해주세요. (ts - X / .ts - O)

### 4. 컨테이너 실행
```
docker compose -f <Compose.yml 경로> --env-file <env경로> up -d
```
- e.g.) docker compose -f video-recorder-docker-compose.yml --env-file .video-recorder.env up -d