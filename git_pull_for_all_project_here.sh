#!/bin/bash

for i in `ls -al|egrep ^d|egrep -v '\.$'|awk '{print $NF}'`
do
	date1=$(date +%s)
	cd $i
	if [ ! -d "./.git" ];then
		cd ..
		continue
	fi
	echo -e "======================================= $i ========================================="
	git pull 2>/dev/null
	date2=$(date +%s)
	time_used=$((date2-date1))
	echo -e "===================================== Pull used time seconds: [$time_used] ===========================================\n"
	cd ..
done
