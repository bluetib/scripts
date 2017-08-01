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
    branch_name="$1"
else
    branch_name=""
fi

function check_branch_exist()
{
    local branch_name="$1"
    N=$(git branch |sed "s+*++g"|column -t|egrep "^${branch_name}$"|wc -l)
    if [ $N -eq 1 ];then
        echo -e "yes"
    else
        echo -e "no"
    fi
}

function get_default_branch_if_need()
{
    num=$(git branch -a|egrep -v "origin"|egrep '^\*'|sed 's/* //'|column -t|wc -l)
    if [ $num -eq 1 ];then
        default_branch_name=$(git branch -a|egrep -v "remotes"|egrep '^\*'|sed 's/* //'|column -t)
        echo -e "$default_branch_name"
    else
        echo -e "no"
    fi
}

function get_remote_info_by_branch_name()
{
    local branch_name="$1"
    N1=$(git branch -a|egrep "$branch_name" -w|egrep remotes|egrep -v HEAD|wc -l)
    if [ $N1 -gt 1 ];then
        echo -e "+++++"
        git remote -v
        echo -e "+++++"
        return 1
    fi
    remote=$(git branch -a|egrep "$branch_name" -w|egrep remotes|egrep -v HEAD|awk -F'/' '{print $2}')
    echo -e "+++++"
    git remote -v|egrep "^${remote}"
    echo -e "+++++"
}
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

if [ -f "rep_list" ];then
    echo -e "--- OK. I will just use the rep_list file to pull from remote ---"
    sleep 1
    while read line
    do
        rep=$(echo $line|awk -F' ' '{print $1}')
        branchs=$(echo $line|awk -F' ' '{print $2}'|sed 's/,/ /g'|sed 's/"//')
        last_checkout_to_branch=$(echo $line|awk -F' ' '{print $3}')
        if [ ! -d "$rep" ];then
            if [ $color == "yes" ];then
                clr_red " === |||||||||||||| =========== Sorry [$rep] not found ============ |||||||||||||| === "
            else
                echo -e " === |||||||||||||| =========== Sorry [$rep] not found ============ |||||||||||||| === "
            fi
            continue
        fi
        cd $rep
        if [ ! -d ".git" ];then
            cd ..
            if [ $color == "yes" ];then
                clr_red " === |||||||||||||| =========== Sorry [$rep] is not right git rep ============ |||||||||||||| === "
            else
                echo -e " === |||||||||||||| =========== Sorry [$rep] is not right git rep ============ |||||||||||||| === "
            fi
            continue
        fi
        echo -e "========================================== $rep ============================================="
        no_branch_match="yes"
        for i in $branchs
        do
            if [ $(check_branch_exist $i) = "yes" ];then
                no_branch_match="no"
                git checkout $i
                check_if_ahead $i
                git status
                echo -e "------------------"
            else
                echo -e "Continue cause branch [$i] not exist"
                continue
            fi
        done
        if [ "$no_branch_match" == "yes" ];then
            default_branch=$(get_default_branch_if_need)
        fi
        if [ "$default_branch" != "no" ];then
            git checkout $default_branch
            check_if_ahead $i
            git status
            echo -e "-------------------"
        fi
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
        default_branch=$(get_default_branch_if_need)
        check_if_ahead $default_branch
        git status
    fi
    N2=$(git branch -a|egrep -v remote|sed 's/*//'|column -t|egrep -w "dev"|wc -l)
    if [ $N2 -eq 1 ];then
        echo -e " ---- checkout to dev ----"
        git checkout dev
    fi
    cd ..
done

