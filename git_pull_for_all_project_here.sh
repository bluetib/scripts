#!/bin/bash

now_path=`cd $(dirname $0) && pwd`
cd $now_path

if [ $# -eq 1 ];then
	branch_name="$1"
else
	branch_name=""
fi

for i in `ls -al|egrep ^d|egrep -v '\.$'|awk '{print $NF}'`
do
	date1=$(date +%s)
	cd $i
	if [ ! -d "./.git" ];then
		cd ..
		continue
	fi
	echo -e "======================================= $i ========================================="
	if [ "$branch_name" != "" ];then
		N=$(git branch -a|egrep -v remote|egrep ${branch_name}|wc -l)
		if [ $N -eq 1 ];then
			git checkout $branch_name
		else
			git checkout -b ${branch_name} origin/${branch_name}
		fi
	fi
	git pull 2>/dev/null
	date2=$(date +%s)
	time_used=$((date2-date1))
	echo -e "|||| checkout to dev |||||"
	git checkout dev
	echo -e "===================================== Pull used time seconds: [$time_used] ===========================================\n"
	cd ..
done
