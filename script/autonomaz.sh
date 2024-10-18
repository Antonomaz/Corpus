#!/usr/bin/env bash

source .env

old_head=$(git rev-parse HEAD)

git pull

IFS=$'\0'

changed_files=()
while IFS= read -r -d $'\0'; do
    changed_files+=("$REPLY")
done < <(git diff --find-renames --name-only -z $old_head HEAD)

unset IFS

for file in "${changed_files[@]}"; do
    if [[ "$file" == *.xml && "$file" == Mazarinades* ]]; then
        echo "Fichier XML Mazarinades modifié: $file"
        echo "Lancement du curl magique"
        file_name=$(basename $file)
        curl -vX PUT -H "Content-Type: application/xml" --data "@$file" $url_anto/$file_name -u $mdp_anto
    fi
done
