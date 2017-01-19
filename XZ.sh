#!/bin/bash

if [ $# -ne 1 ];then
    echo -e "Usage:\n\t$0 \"file_path\""
    exit 12
else
    file="$1"
    if [ ! -f "$file" -a ! -d "$file" ];then
        echo -e "Sorry. File [$file] not found"
        exit 13
    fi
fi

file="$(echo $file|sed 's+/$++')"
export XZ_OPT=-9
tar Jcvf ${file}.tar.xz $file
echo -e "=========================="
du -sh ${file}.tar.xz
echo -e "=========================="
