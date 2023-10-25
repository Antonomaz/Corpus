#!/usr/bin/env bash

#usage: find_problematic_pb_numbering <dir> <output_path>
SEARCH_PATH="$1/**/*.xml"
OUTPUT_DIR="$2"
OUTPUT_FILE="$OUTPUT_DIR/problematic_numbering.csv"

echo "id,n_start" >"$OUTPUT_FILE"

for f in $SEARCH_PATH; do
    n=$(xmllint --xpath "string(//*[local-name()='pb'][@n]/@n)" "$f")
    if [ "$n" != "1" ]; then
        echo "$(basename "$f" | cut -d. -f1),${n}" >>"$OUTPUT_FILE"
    fi
done
