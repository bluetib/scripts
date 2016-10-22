#!/bin/bash


git checkout dev
if [ $? -ne 0 ];then
	echo -e "Sorry.You must at dev branch.."
	exit 1
fi
git pull && git push
