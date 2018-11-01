#!/bin/bash

if [ $# -ne 1 ];then
    echo -e "Usage:\n\t$0 [start/end]"
    exit 1
elif [ "$1" != "start" -a "$1" != "end" ];then
    echo -e "Usage:\n\t$0 [start/end]"
    exit 1
else
    choice="$1"
fi

if [ ! -d "/etc/iptables_work" ];then
    mkdir -p /etc/iptables_work
fi

if [ "$choice" == "start" ];then
    if [ -f /etc/iptables_work/iptables.save ];then
        echo -e "Maybe you alread saved the iptables rules in [/etc/iptables_work/iptables.save]"
        echo -e "----------------"
        stat /etc/iptables_work/iptables.save
        echo -e "----------------"
        echo -e "If you still need to run.You should remove this file /etc/iptables_work/iptables.save"
        exit 0
    else
        iptables-save -c > /etc/iptables_work/iptables.save
        echo -e "Saved iptables rules to [/etc/iptables_work/iptables.save]"
        N_1=$(cat /etc/crontab |egrep "clear new added iptables rule every 5 minutes"|wc -l)
        if [ $N_1 -ge 1 ];then
            echo -e "Already added crontab task for clear new added iptables rules"
            exit 1
        else
            echo -e "#clear new added iptables rule every 5 minutes" >> /etc/crontab
            echo -e "*/2 * * * * root iptables-restore < /etc/iptables_work/iptables.save" >> /etc/crontab
            echo -e "Added crontab for clear new added iptables rules every 5 minutes"
        fi
    fi
elif [ "$choice" == "end" ];then
    if [ -f /etc/iptables_work/iptables.save ];then
        echo -e "OK.First let me restore rules saved before cause I found [/etc/iptables_work/iptables.save]"
        iptables-restore < /etc/iptables_work/iptables.save
        echo -e "Restore done"
        rm -rf /etc/iptables_work/iptables.save
        echo -e "rm /etc/iptables_work/iptables.save Done"
        cat /etc/crontab |egrep -v "clear new added iptables rule every 5 minutes"|egrep -v "iptables-restore" > /tmp/crontab
        mv /tmp/crontab /etc/crontab
        echo -e "remove crontab task for clear new added rules every 5 minutes Done"
    else
        cat /etc/crontab |egrep -v "clear new added iptables rule every 5 minutes"|egrep -v "iptables-restore" > /tmp/crontab
        mv /tmp/crontab /etc/crontab
        echo -e "remove crontab task for clear new added rules every 5 minutes Done"
    fi
fi
