#!/bin/bash
# 카메라 없이 테스트용 mp4 파일 생성
# 실행: bash make_test_videos.sh

CAM_NAME="CAM-01"
OUTPUT_DIR="./video/${CAM_NAME}"
SEGMENT_SEC=10   # 실제는 3600, 테스트용 10초
COUNT=5          # 생성할 파일 수

mkdir -p "$OUTPUT_DIR"

echo "테스트 영상 생성 중... (${COUNT}개 × ${SEGMENT_SEC}초)"

for i in $(seq 0 $((COUNT - 1))); do
  # i * SEGMENT_SEC 초 전 시각으로 파일명 생성
  TIMESTAMP=$(date -v -$((i * SEGMENT_SEC))S '+%Y%m%d_%H%M%S' 2>/dev/null \
    || date -d "$((i * SEGMENT_SEC)) seconds ago" '+%Y%m%d_%H%M%S')
  OUTFILE="${OUTPUT_DIR}/${TIMESTAMP}.mp4"

  ffmpeg -y -loglevel error \
    -f lavfi -i "testsrc=duration=${SEGMENT_SEC}:size=640x360:rate=25" \
    -f lavfi -i "sine=frequency=440:duration=${SEGMENT_SEC}" \
    -c:v libx264 -preset ultrafast -crf 35 \
    -c:a aac -b:a 64k \
    -movflags +frag_keyframe+empty_moov \
    "$OUTFILE"

  echo "  생성: $OUTFILE"
done

echo ""
echo "완료. 생성된 파일:"
ls -lh "$OUTPUT_DIR"
