#!/bin/bash

now_path=`cd $(dirname $0) && pwd`
cd $now_path

if [ $# -eq 1 ];then
    branch_name="$1"
else
    branch_name=""
fi

if [ -f "/usr/local/bin/funcs.sh" ];then
    . /usr/local/bin/funcs.sh
    color="yes"
else
    color="no"
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
    remote_name=$(git branch -a -vv|egrep -v "remotes"|sed 's|\*||g'|column -t|egrep "^${branch_name}"|egrep -w "${branch_name}"|awk '{print $3}'|sed 's|\[||g'|sed 's|\]||g'|awk -F'/' '{print $1}')
    echo -e "+++++"
    git remote -v|egrep "^${remote_name}"
    echo -e "+++++"
}

if [ -f "rep_list" ];then
    echo -e "--- OK. I will just use the rep_list file to pull from remote ---"
    sleep 1
    while read line
    do
        rep=$(echo $line|awk -F' ' '{print $1}')
        branchs=$(echo $line|awk -F' ' '{print $2}'|sed 's/,/ /g'|sed 's/"//')
        last_checkout_to_branch=$(echo $line|awk -F' ' '{print $3}')
        if [ -d "$rep" ];then
            cd $rep
        else
            if [ $color == "yes" ];then
                clr_red " === |||||||||||||| =========== Sorry [$rep] not found ============ |||||||||||||| === "
            else
                echo -e " === |||||||||||||| =========== Sorry [$rep] not found ============ |||||||||||||| === "
            fi
            continue
        fi
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
                date1=$(date +%s)
                get_remote_info_by_branch_name $i
                if [ "$rep" == "all_sls" ];then
                    git pull --ff 2>/dev/null
                else
                    git pull 2>/dev/null
                fi
                date2=$(date +%s)
                time_used=$((date2-date1))
                echo -e "-------- Pull for branch [$i] used time seconds: [$time_used] ---------\n"
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
            date1=$(date +%s)
            if [ "$rep" == "all_sls" ];then
                git pull --ff 2>/dev/null
            else
                git pull 2>/dev/null
            fi
            date2=$(date +%s)
            time_used=$((date2-date1))
            echo -e "-------- Pull for branch [$default_branch] used time seconds: [$time_used] ---------\n"
        fi
        N2=$(git branch -a|egrep -v remote|sed 's/*//'|column -t|egrep -w "$last_checkout_to_branch"|wc -l)
        if [ $N2 -eq 1 ];then
            echo -e "--- [checkout to $last_checkout_to_branch] ---"
            git checkout $last_checkout_to_branch
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
            git br -a
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
    if [ "$branch_name" = "" ];then
        default_branch=$(get_default_branch_if_need)
        echo -e "--- git pulling for branch default_branch [$default_branch] ---"
        get_remote_info_by_branch_name $default_branch
    else
        echo -e "--- git pulling for branch the_branch [$branch_name] ---"
        get_remote_info_by_branch_name $branch_name
    fi
    git pull 2>/dev/null
    date2=$(date +%s)
    time_used=$((date2-date1))
    N2=$(git branch -a|egrep -v remote|sed 's/*//'|column -t|egrep -w "dev"|wc -l)
    if [ $N2 -eq 1 ];then
        echo -e " ---- checkout to dev ----"
        git checkout dev
    fi
    echo -e "===================================== Pull used time seconds: [$time_used] ===========================================\n"
    cd ..
done

