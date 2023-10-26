#!/usr/bin/env bash

offset="$2"
# transform n=x into n=x-<offset>
xmlstarlet ed --inplace -u "//@n" -x "number(translate(., 'n=', '')) - $offset " "$1"
