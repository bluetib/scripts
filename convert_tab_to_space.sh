#!/bin/bash

if [ $# -ne 1 ];then
    echo -e "Usage:\n\t$0 \"[sh/py]\" "
    exit 1
fi

file_type="$1"

find . -name "*.${file_type}" ! -type d -exec bash -c 'expand -t 4 "$0" > /tmp/e && mv /tmp/e "$0"' {} \;
