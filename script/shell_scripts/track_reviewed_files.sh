#!/usr/bin/env bash

#usage: cmd <dir> <output_path>
SEARCH_PATH="$1/**/*.xml"
OUTPUT_DIR="$2"
OUTPUT_FILE="$OUTPUT_DIR/reviewed_files.csv"

echo "file,reviewded_status" >"$OUTPUT_FILE"

for f in $SEARCH_PATH; do
    echo "$(basename "$f"), " >>"$OUTPUT_FILE"
done
