#!/bin/bash


if [ $# -ne 1 ];then
    echo -e "Usage:\n\t$0 \"IP Address\""
    exit 1
fi

IP="$1"

mtr -c 20 -i 0.5 -b $IP
