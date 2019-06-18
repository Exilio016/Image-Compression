#!/bin/sh
args= 

while [ "$1" != "" ]; do
    args="$args$1 "
    # Shift all the parameters down by one
    shift

done

python3 src/compression.py $args