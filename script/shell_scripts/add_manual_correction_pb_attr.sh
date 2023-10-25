#!/usr/bin/env bash

# usage: cmd <search_dir> <attr> <val>
SEARCH_PATH="$1/**/*.xml"

for f in $SEARCH_PATH; do
    xmlstarlet ed --pf --insert "//*[local-name()='pb'][1]" --type attr -n "$2" -v "$3" "$f" >tmpfile && mv tmpfile "$f"
done
