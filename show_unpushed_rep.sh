#!/bin/bash

now_path=`cd $(dirname $0) && pwd`
cd $now_path

if [ -f "/usr/local/bin/funcs.sh" ];then
    . /usr/local/bin/funcs.sh
    color="yes"
else
    color="no"
fi

if [ $# -eq 1 ];then
    branch_name="$1" else
    branch_name=""
fi

function check_if_ahead()
{
    local branch_name="$1"
    ahead_num=$(git status|egrep "is ahead of"|egrep -w -o "[0-9]+"|wc -l)
    if [ $ahead_num -ge 1 ];then
        if [ $color == "yes" ];then
            clr_red "=== |||||||||||||| =========== Please check [Need To Push] ahead of $ahead_num commits ============|||||||||||||| ==="
        else
            echo -e "=== |||||||||||||| =========== Please check [Need To Push] ahead of $ahead_num commits ============|||||||||||||| ==="
        fi
    fi
}

function check_branch_exist()
{
    local branch_name="$1"
    N=$(git branch |sed "s+*++g"|column -t|egrep -w "^${branch_name}$"|wc -l)
    if [ $N -eq 1 ];then
        echo -e "yes"
    else
        echo -e "no"
    fi
}

if [ -f "rep_list" ];then
    echo -e "--- OK. I will just use the rep_list file to pull from remote ---"
    sleep 1
    while read line
    do
        rep=$(echo $line|awk -F' ' '{print $1}')
        branchs=$(echo $line|awk -F' ' '{print $2}'|sed 's/,/ /g'|sed 's/"//')
        last_checkout_to_branch=$(echo $line|awk -F' ' '{print $3}')
        if [ ! -d "$rep" ];then
            continue
        fi
        cd $rep
        if [ ! -d ".git" ];then
            cd ..
            continue
        fi
        echo -e "========================================== $rep ============================================="
        for i in $branchs
        do
            if [ $(check_branch_exist $i) = "yes" ];then
                git checkout $i
                check_if_ahead $i
                git status
                echo -e "------------------"
            else
                echo -e "Continue cause branch [$i] not exist"
                continue
            fi
        done
        N2=$(git branch -a|egrep -v remote|sed 's/*//'|column -t|egrep -w "$last_checkout_to_branch"|wc -l)
        if [ $N2 -eq 1 ];then
            echo -e "--- [checkout to $last_checkout_to_branch] ---"
            git checkout $last_checkout_to_branch
            check_if_ahead $last_checkout_to_branch
        fi
        cd ..
    done < ./rep_list
    exit 12
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
        N=$(git branch -a|egrep -v remote|sed 's/*//'|column -t|egrep -w ${branch_name}|wc -l)
        if [ $N -eq 1 ];then
            echo -e "=== checkout to $branch_name to update this branch $branch_name ==="
            git checkout $branch_name
            git branch -a
        else
            N1=$(git branch -a|egrep remote|column -t|egrep -w ${branch_name}|wc -l)
            if [ $N1 -eq 1 ];then
                git checkout -b ${branch_name} origin/${branch_name}
            else
                echo -e "Sorry. no remote branch name match your request [$branch_name]"
                cd ..
                continue
            fi
        fi
    fi
    if [ "$branch_name" != "" ];then
        check_if_ahead "$branch_name"
        git status
    else
        check_if_ahead "dev"
        git status
    fi
    N2=$(git branch -a|egrep -v remote|sed 's/*//'|column -t|egrep -w "dev"|wc -l)
    if [ $N2 -eq 1 ];then
        echo -e " ---- checkout to dev ----"
        git checkout dev
    fi
    cd ..
done

