#!/bin/bash


branch_tmp_name="tmp_for_check"

if [ $# -ne 2 ];then
	echo -e "Usage:\n\t$0 \"the_branch\" \"the_commit\" "
	exit 1
else
	branch_name="$1"
	commit_id="$2"
fi


N2=$(git branch -a|egrep -v remote|sed 's/*//'|column -t|egrep "^${branch_tmp_name}$"|wc -l)
#echo $N2
if [ $N2 -eq 1 ];then
	git checkout master
	git branch -d $branch_tmp_name
fi

N=$(git branch -a|egrep -v remote|sed 's/*//'|column -t|egrep "^${branch_name}$"|wc -l)
#echo $N
if [ $N -eq 1 ];then
	git checkout $branch_name
else
	echo -e "[ == Sorry. Git Branch $branch_name not exists. I will create it now == ]"
	git checkout -b ${branch_name} origin/${branch_name}
fi

N1=$(git branch -a|egrep -v remote|sed 's/*//'|column -t|egrep "^${branch_tmp_name}$"|wc -l)
#echo $N1
if [ $N1 -lt 1 ];then
	git checkout -b  ${branch_tmp_name} $commit_id
fi

