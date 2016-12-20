#!/bin/bash

if [ $# -ne 1 ];then
    echo -e "Usage:\n\t$0 \"path_to_deal_file\""
    exit 1
else
    file="$1"
    if [ ! -f "$file" ];then
        echo -e "Sorry..$file not found.."
        exit 12
    fi
fi

Num=30
sleep_between=1

step_path="/tmp/step_for_salt"
step_1="${step_path}/1.sh"
step_2="${step_path}/2.sh"
step_3="${step_path}/3.sh"
step_4="${step_path}/4.sh"
step_5="${step_path}/5.sh"


function exec_script_step()
{
    local script_path="$1"
    #if [ ! -f "$script_path" ];then
    #   echo -e "No $script_path found"
    #   return
    #fi
    local all_steps=$2
    local step_sleep=$3
    local host=$4
    local N1=0
    while [ $N1 -lt $all_steps ]
    do
        ret_tmp=$(salt "$host" cmd.run "[ -f $script_path ] && bash $script_path")
        echo -e "==================== [in the step function] [`date +%F_%H:%M:%S`] 【$N1】 ======================="
        echo -e "$ret_tmp"
        echo -e "================================================================================================="
        sleep $step_sleep
        N1=$((N1+1))
    done
}

function exec_one_script()
{
    local script_path="$1"
    local need_step="$2"
    echo -e "--- I am going to exec ${script_path} ---"
    sleep 1
    if [ "$need_step" == "yes" ];then
        exec_script_step "${script_path}" $Num $sleep_between $i
    else
        local ret_1=$(salt "$i" cmd.run "[ -f ${script_path} ] && bash ${script_path}")
        echo -e "$ret_1"
    fi
    sleep 2
}

for i in `cat $file`
do
    echo -e "【 I am dealling with server [$i] 】"
    read -p "Let's GO? [y/n]: " co0
    if [ "$co0" == "yes" -o "$co0" == "" ];then
        echo -e "--- OK.Go.. ---"
        sleep 1
        ########################################################
        read -p "[$step_1] Continue?[y/n]: " co1
        if [ "$co1" == "yes" -o "$co1" == "" ];then
            echo -e "--- OK.Go for $step_1.. ---"
            sleep 1
        else
            echo -e "--- Bye. ---"
            sleep 1
            break
        fi
        exec_one_script $step_1

        read -p "[$step_2] Continue?[y/n]: " co2
        if [ "$co2" == "yes" -o "$co2" == "" ];then
            echo -e "--- OK.Go for $step_2.. ---"
            sleep 1
        else
            echo -e "--- Bye. ---"
            sleep 1
            break
        fi
        exec_one_script $step_2 "yes"

        read -p "[$step_3] Continue?[y/n]: " co3
        if [ "$co3" == "yes" -o "$co3" == "" ];then
            echo -e "--- OK.Go for $step_3.. ---"
            sleep 1
        else
            echo -e "--- Bye. ---"
            sleep 1
            break
        fi
        exec_one_script $step_3

        read -p "[$step_4] Continue?[y/n]: " co4
        if [ "$co4" == "yes" -o "$co4" == "" ];then
            echo -e "--- OK.Go for $step_4.. ---"
            sleep 1
        else
            echo -e "--- Bye. ---"
            sleep 1
            break
        fi
        exec_one_script $step_4

        read -p "[$step_5] Continue?[y/n]: " co5
        if [ "$co5" == "yes" -o "$co5" == "" ];then
            echo -e "--- OK.Go for $step_5.. ---"
            sleep 1
        else
            echo -e "--- Bye. ---"
            sleep 1
            break
        fi
        exec_one_script $step_5
        ########################################################

    else
        echo -e "--- Bye. ---"
        sleep 1
        exit 12
    fi
done
