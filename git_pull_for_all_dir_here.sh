#!/bin/bash

for i in `ls -al|egrep ^d|egrep -v '\.$'|awk '{print $NF}'`
do
	date1=$(date +%s)
	cd $i
	if [ ! -d "./.git" ];then
		continue
	fi
	echo -e "======================================= $i ========================================="
	git pull
	date2=$(date +%s)
	time_used=$((date2-date1))
	echo -e "===================================== Pull used time seconds: [$time_used] ===========================================\n"
	cd ..
done
