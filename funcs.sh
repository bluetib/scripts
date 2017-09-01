#!/bin/bash

cwd_path=$(cd `dirname $0` && pwd)
cd $cwd_path

if [ -f "color.sh" ];then
    . color.sh
elif [ -f "/usr/local/bin/color.sh" ];then
    . /usr/local/bin/color.sh
fi


