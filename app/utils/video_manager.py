from pathlib import Path
from collections import defaultdict, deque
from datetime import datetime
import shutil
import logging

logger = logging.getLogger()

def disk_usage_percent(video_path: str):
    usage = shutil.disk_usage(video_path)
    return (usage.used / usage.total) * 100.0

def recording_time(path: Path):
    try:
        return datetime.strptime(path.stem, "%Y%m%d_%H%M%S")
    except ValueError:
        return datetime.max

def purge_old_files_until(video_path: str, target_percent: float, extensions: list[str] | None = None):
    if extensions is None:
        extensions = [ ".ts" ]
    camera_files = defaultdict(deque)
    files = []
    for ext in extensions:
        files.extend(Path(video_path).rglob(f"*{ext}"))
    
    files = [f for f in files if f.is_file()]
    
    for f in files:
        camera = f.parent.name
        camera_files[camera].append(f)
    
    for camera in camera_files:
        camera_files[camera] = deque(sorted(camera_files[camera], key=recording_time))
    
    while disk_usage_percent(video_path=video_path) > target_percent:
        deleted = False
        
        for _, file_list in camera_files.items():
            if not file_list:
                continue
            
            oldest = file_list.popleft()
            try:
                size_mb = oldest.stat().st_size / (1024 * 1024)
                oldest.unlink()
                logger.warning("Deleted Recording: %s (%.1f MB)", oldest, size_mb)
                logger.info("Current Disk Usage: %.2f%%", disk_usage_percent(video_path=video_path))
                deleted=True
            except Exception:
                logger.exception("Failed Deleting %s", oldest)
                
        if not deleted:
            break

    
def storage_manager(video_path: str, low_percent: float, high_percent: float, ext: list[str] | None = None):
    if ext is None:
        ext = [ ".ts" ]

    try:
        if disk_usage_percent(video_path) > high_percent: ## ex. 사용량 90% 초과 (High_percent) -> 여유 공간 40% 확보까지, 오래된 영상부터 삭제 (Low_Percent)
            purge_old_files_until(video_path=video_path, target_percent=low_percent, extensions=ext)
    except Exception:
        logger.exception("Storage Manager Error")
