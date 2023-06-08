#!/usr/bin/env bash

#usage: find_keyword_in_dir <keyword> <dir> <extension>
SEARCH_PATH="$2/**/*.$3"

for f in $SEARCH_PATH; do grep "$1" $f && echo $f; done
