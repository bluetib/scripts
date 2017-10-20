#!/bin/bash

now_path=`cd $(dirname $0) && pwd`
cd $now_path

for i in `ls -al|egrep ^d|egrep -v '\.$'|awk '{print $NF}'`
do
	date1=$(date +%s)
	cd $i
	if [ ! -d "./.git" ];then
		cd ..
		continue
	fi
	echo -e "======================================= $i ========================================="
	echo -e "I am git pulling all branch.. Please just wait for a while.. "
	sleep 1
	git pull --all
	echo -e "===================================== Pull used time seconds: [$time_used] ===========================================\n"
	cd ..
done
