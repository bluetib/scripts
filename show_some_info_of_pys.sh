#!/bin/bash

if [ $# -ne 1 ];then
    echo -e "Usage:\n\t $0 \"/path/to/dir\""
    exit 2
else
    the_path="$1"
    if [ ! -d "$the_path" ];then
        echo -e "Sorry..[$the_path] not found..OR [$the_path] need to be a dir"
        exit 2
    fi
fi

function show_info()
{
    local num="$1"
    local message="$2"
    echo -e "\n$num、 --- [$message] ---\n"
    sleep 0.5
}

function show_info_2()
{
    local message="$*"
    echo -e "======================"
    echo -e "$message"
    echo -e "======================\n"
    sleep 0.5
}

function clean()
{
    if [ -d "$t_dir" ];then
        rm -rf $t_dir
    fi
}

#---------------
if [ "$(uname -o|tr 'A-Z' 'a-z'|awk -F'/' '{print $2}')" == "linux" ];then
    echo -e "Only support Linux now"
else
    echo -e "Only support Linux now"
    exit 1
fi
t_dir="/tmp/tib1"
if [ ! -d "$t_dir" ];then
    mkdir -p $t_dir
fi
t_file_1="$t_dir/t_file_1"
t_file_2="$t_dir/t_file_2"
t_file_3="$t_dir/t_file_3"
t_file_4="$t_dir/t_file_4"
#---------------

find $the_path -name "*.py" -type f > $t_file_1
find $the_path -name "*.sh" -type f > $t_file_4
py_file_num=$(cat $t_file_1|wc -l)
sh_file_num=$(cat $t_file_4|wc -l)
show_info_2 "This time I got $py_file_num python files"
show_info_2 "This time I got $sh_file_num shell files"
if [ $py_file_num -ne 0 ];then
    show_info 1 "calculate every python file"
    sum_py=0
    while read line
    do
        N=$(cat "$line"|wc -l)
        sum_py=$((sum_py+N))
        echo -e "$N $line" >> $t_file_2
    done < $t_file_1
    if [ $py_file_num -ge 10000 ];then
        echo -e "So many files.. You sure want to check this ?"
        read -p "[yes/no/y/n]: " choice
        if [ "$choice" == "yes" -o "$choice" == "y" -o "$choice" == "" -o "$choice" == "Y" ];then
            show_info 2 "show every python file info"
            cat $t_file_2|sort -n -k1|egrep -v ^0
        else
            echo -e "OK.No show this time..If you want to see please run script again."
        fi
    else
        show_info 2 "show every python file info"
        cat $t_file_2|sort -n -k1|egrep -v ^0
    fi
else
    sum_py=0
fi
if [ $sh_file_num -ne 0 ];then
    show_info 1 "calculate every shell file"
    sum_sh=0
    while read line
    do
        N=$(cat "$line"|wc -l)
        sum_sh=$((sum_sh+N))
        echo -e "$N $line" >> $t_file_3
    done < $t_file_4
    if [ $sh_file_num -ge 10000 ];then
        echo -e "So many files.. You sure want to check this ?"
        read -p "[yes/no/y/n]: " choice
        if [ "$choice" == "yes" -o "$choice" == "y" -o "$choice" == "" -o "$choice" == "Y" ];then
            show_info 2 "show every shell file info"
            cat $t_file_3|sort -n -k1|egrep -v ^0
        else
            echo -e "OK.No show this time..If you want to see please run script again."
        fi
    else
        show_info 2 "show every shell file info"
        cat $t_file_3|sort -n -k1|egrep -v ^0
    fi
else
    sum_sh=0
fi

show_info_2 "All python code lines is [$sum_py]"
show_info_2 "All shell code lines is [$sum_sh]"

clean
