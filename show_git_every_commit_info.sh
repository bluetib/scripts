#!/bin/bash

#set -x

cwd=$(cd `dirname $0` && pwd)
cd $cwd

if [ $# -ne 3 ];then
    echo -e "Usage:\n\t$0 \"repository\" \"branch_name\" \"key_word\""
    exit 12
else
    repository="$1"
    key_word="$3"
    branch="$2"
    if [ ! -d "$repository" ];then
        echo -e "No dir or repository $repository found in this path [$cwd]"
        exit 2
    fi
fi

######################
tmp_file_to_store_commit="/tmp/t_for_git_commit"
lg2="log --color --pretty=format:\"%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset\" --abbrev-commit"
#=====================

cd $repository
git checkout $branch >/dev/null 2>&1
if [ $? -ne 0 ];then
    echo -e "Sorry...Error Happened.."
    exit 2
fi
git lg2 |egrep "$key_word" > $tmp_file_to_store_commit
N=$(cat $tmp_file_to_store_commit|wc -l)
echo -e "----------------------------------------------------------"
if [ "$N" == "0" ];then
    echo -e "Sorry..No result found..It's empty.."
    echo -e "----------------------------------------------------------\n"
    exit 22
else
    cat $tmp_file_to_store_commit
fi
echo -e "----------------------------------------------------------\n"

echo -e "You sure want to check every commit ?"
read -p  "yes or no ? [y/n]: " co8
if [ "$co8" == "yes" -o "$co8" == "" -o "$co8" == "y" ];then
    echo -e  "OK..Let's check and let's go\n"
    sleep 1
else
    echo -e "Oh yeah..EXIT now.."
    exit 2
fi

the_time=$(date +%F_%H:%M)

old="$IFS"
IFS='
'

for line in $(<$tmp_file_to_store_commit)
do
    commit="$(echo -e $line|awk -F'-' '{print $1}'|column -t)"
    commit=$(echo $commit|sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]//g")
    commit_info="$(echo -e $line|awk -F'-' '{print $2}')"
    IFS="$old"
    echo -e "$line\n"
    read -p "Need to check this one? [y/n]: " co0
    if [ "$co0" == "yes" -o "$co0" == "" -o "$co0" == "y" ];then
        echo -e "---- OK check the files changed with this commit [$commit] ----"
        sleep 0.5
        git show --pretty="" --name-only $commit
        echo -e "----- +++++ ------"
        read -p "check every file change now? [y/n] " co1
        if [ "$co1" == "yes" -o "$co1" == "" -o "$co1" == "y" ];then
            echo -e "---- OK check the content changed with this commit [$commit] ----"
            sleep 0.5
            git show $commit
        else
            echo -e "Skip this step [$commit] and We Continue to the next commit..------"
        fi
    else
        echo -e "Skip this step [$commit] and We Continue to the next commit..------"
        sleep 0.1
    echo -e "++++++++++++++++++++++++++++++++++++++++\n"
    fi
done

