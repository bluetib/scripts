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
    echo -e "$num、 --- [$message] ---\n"
    sleep 1
}

function show_info_2()
{
    local message="$*"
    echo -e "======================"
    echo -e "$message"
    echo -e "======================\n"
    sleep 1
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
#---------------

find $the_path -name "*.py" -type f > $t_file_1
file_num=$(cat $t_file_1|wc -l)
show_info_2 "This time I got $file_num files"
show_info 1 "calculate every file"
sum=0
for i in `cat $t_file_1`
do
    N=$(cat $i|wc -l)
    sum=$((sum+N))
    echo -e "$N $i" >> $t_file_2
done

show_info 2 "show every file info"
cat $t_file_2|sort -n -k1
show_info_2 "All code lines is [$sum]"

clean
