#!/bin/bash

# --- Configuration ---

# Define the source directory (must exist)
SOURCE_DIR="/home/fruitbat/VM/zenplayer"
DEST_DIR="/home/fruitbat/Repos/zencode/zenplayer"

echo "Starting copy operation..."
# 2. Copy all contents from SOURCE_DIR to DEST_DIR
# The / at the end of the source path ensures contents are copied, not the folder itself.
# -r: Recursive (handles subdirectories, if any)
# -f: Force overwrite (does not prompt before overwriting existing files)
# -v: Verbose (prints details of the files being copied)

cp -rvf "$SOURCE_DIR" "$DEST_DIR"

echo "Building..."
buildozer android debug

echo "Copying back..."
cp -rvf "$DEST_DIR/zenplayer/bin" "$SOURCE_DIR"


echo "Copy completed. All files from $SOURCE_DIR have been copied and overwritten in $DEST_DIR."
