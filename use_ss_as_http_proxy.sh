#!/bin/bash

if [ $# -ne 2 ];then
    echo -e "Usage:\n\t$0 IP PORT"
    exit 1
fi

export http_proxy="http://${IP}:${PORT}"
export https_proxy="http://${IP}:${PORT}"
