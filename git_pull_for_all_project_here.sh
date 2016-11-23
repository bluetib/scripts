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
		N=$(git branch -a|egrep -v remote|sed 's/*//'|column -t|egrep ${branch_name}|wc -l)
		if [ $N -eq 1 ];then
			echo -e "=== checkout to $branch_name to update this branch $branch_name ==="
			git checkout $branch_name
			git br -a
		else
			N1=$(git branch -a|egrep remote|column -t|egrep ${branch_name}|wc -l)
			if [ $N1 -eq 1 ];then
				git checkout -b ${branch_name} origin/${branch_name}
			else
				echo -e "Sorry. no remote branch name match your request [$branch_name]"
				cd ..
				continue
			fi
		fi
	fi
	echo -e "--- git pulling for branch $branch_name ---"
	git pull 2>/dev/null
	date2=$(date +%s)
	time_used=$((date2-date1))
	N2=$(git branch -a|egrep -v remote|sed 's/*//'|column -t|egrep "dev"|wc -l)
	if [ $N2 -eq 1 ];then
		echo -e " ---- checkout to dev ----"
		git checkout dev
	fi
	echo -e "===================================== Pull used time seconds: [$time_used] ===========================================\n"
	cd ..
done
