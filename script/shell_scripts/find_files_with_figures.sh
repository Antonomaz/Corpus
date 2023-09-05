#!/usr/bin/env bash

XML_DIR="$1"

for f in "$XML_DIR"/**/*; do
    RES=$(xmllint --xpath "//*[local-name()='figure']" "$f" 2>/dev/null)
    if [ -n "$RES" ]; then
        # Print the filename
        basename "$f"
    fi
done
