#!/bin/bash

if [ $# -ne 2 ];then
    echo -e "Usage:\n\t $0 \"/file/path\" \"[py|sh]\""
    exit 2
else
    file_path="$1"
    choice="$2"
    if [ ! -f "$file_path" ];then
        echo -e "Sorry..[$file_path] not found."
        exit 3
    fi
    if [ "$choice" != "sh" -a "$choice" != "py" ];then
        echo -e "Sorry. Only py or sh by the second arg"
        exit 4
    fi
fi

cat $file_path|egrep "${choice}$"|sort -k2 -ifb|column  -t|less

