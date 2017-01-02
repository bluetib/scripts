#!/bin/bash

if [ $# -ne 1 ];then
	echo -e "Usage:\n\t $0 \"some_key_string_for_name\""
	exit 12
else
	key_string="$1"
fi

ssh-keygen -f ./${key_string} -t rsa -b 2048

echo -e "============================================================"
echo -e "钥匙对的指纹信息："
ssh-keygen -lf ${key_string}
echo -e "============================================================"
