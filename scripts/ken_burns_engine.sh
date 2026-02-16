#!/bin/bash
# ken_burns_engine.sh - Deterministic FFmpeg Video Generator
# Purpose: Converts static images into a 3-hour "sleepy" video with motion.

IMG_DIR=$1
OUTPUT_FILE=$2
DURATION_PER_IMG=30 # Seconds per image
TOTAL_IMAGES=$(ls $IMG_DIR/*.png | wc -l)

echo "Starting Deterministic Ken Burns Engine..."

# Create a filter_complex script
# This script applies a slow zoom-in (1.0 to 1.1) to every image in the folder
# and concatenates them without needing heavy orchestration.

FFMPEG_CMD="ffmpeg -y "

# 1. Load Inputs
for img in $IMG_DIR/*.png; do
    FFMPEG_CMD+="-loop 1 -t $DURATION_PER_IMG -i $img "
done

# 2. Apply Deterministic Motion & Concat
FFMPEG_CMD+="-filter_complex \""
for ((i=0; i<$TOTAL_IMAGES; i++)); do
    FFMPEG_CMD+="[$i:v]scale=2560:-1,zoompan=z='min(zoom+0.0005,1.1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$((DURATION_PER_IMG*25)):s=1920x1080[v$i]; "
done

for ((i=0; i<$TOTAL_IMAGES; i++)); do
    FFMPEG_CMD+="[v$i]"
done
FFMPEG_CMD+="concat=n=$TOTAL_IMAGES:v=1:a=0[v]\" "

# 3. Encode for local performance
FFMPEG_CMD+="-map \"[v]\" -c:v libx264 -pix_fmt yuv420p -r 25 $OUTPUT_FILE"

echo "Executing: $FFMPEG_CMD"
# eval $FFMPEG_CMD # Uncomment to run locally
