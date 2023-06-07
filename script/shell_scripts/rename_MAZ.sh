#!/usr/bin/env bash
if [ -d "./logs" ]; then
    LOGFILE="logs/$(date -I)_maz_changelog.txt"
else
    LOGFILE="$(date -I)_maz_changelog.txt"
fi

#TODO: (maybe) - python rewrite

# usage: rename_maz <xml file>
function rename_maz() {
    NEWNAME="$(xmllint --xpath "string(//*[local-name()='relatedItem']/@subtype)" "$1")"
    echo "$1->$NEWNAME" >>"$LOGFILE"
    mv "$1" "$(dirname "$1")"/"$NEWNAME"_MAZ.xml
}

#usage: rename_maz <xml dir>

function rename_maz_dir() {
    if [ -f "$LOGFILE" ]; then
        rm "$LOGFILE"
    fi
    for f in "$1"/*; do
        rename_maz "$f"
    done
}

rename_maz_dir "$1"
