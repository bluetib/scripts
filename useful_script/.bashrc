# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples



# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines in the history. See bash(1) for more options
# don't overwrite GNU Midnight Commander's setting of `ignorespace'.
export HISTCONTROL=$HISTCONTROL${HISTCONTROL+,}ignoredups
# ... or force ignoredups and ignorespace
export HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
    # We have color support; assume it's compliant with Ecma-48
    # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
    # a case would tend to support setf rather than setaf.)
    color_prompt=yes
    else
    color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

PS1='\e[31m\u \e[32m@ \e[33m\h \e[36m\w \e[37m\#: \e[31m'
export PS1
# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

#if [ -f ~/.bash_aliases ]; then
#    . ~/.bash_aliases
#fi

# enable color support of ls and also add handy aliases
# some more ls aliases
#alias ll='ls -l'
#alias la='ls -A'
#alias l='ls -CF'
#if [ -x /usr/bin/dircolors ]; then
#    eval "`dircolors -b`"
alias dir='dir --color=auto'
alias ld='ls -Al | grep ^d'
alias lf='ls -Al | grep ^-'
alias ll='ls -Al'
alias vdir='vdir --color=auto'
alias cls='clear'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias size='du -sh'
alias ll='ls -Al'
alias kill='kill -KILL'
alias Mymount='mount |column -t'
alias MyDf='df -ah|column -t'
alias Shit='scp -P 36000 /openwrt/qosv4 root@192.168.2.1:/'
alias Mytmpfs='MyDf|egrep tmpfs'
alias SListen='netstat -an|egrep -i listen'
alias pstree='pstree -anpuh'
alias cman='man -M /usr/share/man/zh_CN'
alias Zhuxiao='gnome-session-save --logout'
alias timeanddate='echo ++++++++++++++++++++++++++++;cal;date;echo +++++++++++++++++++++++++++++'
alias ls3r3w3x='ls -al | grep ^.rwxrwxrwx'
alias English='LANG=en_US:UTF-8;LANGUAGE=en_US:UTF-8'
alias Snet_port='netstat -an|egrep -i listen --col'
alias PS_EFAUX='ps aux'
alias Hanhua='LANG=zh_CN:UTF-8;LANGUAGE=zh_CN:UTF-8'
alias lstargz='ls -al | grep tar.gz$'
alias Snat='iptables -t nat -L -vn'
alias vi='vim'
alias LC='LANG=C'
alias cp='cp -v'
alias mv='mv -v'
alias Sfilter='iptables -t filter -L -vn'
alias Sraw='iptables -t raw -L -vn'
alias Smangle='iptables -t mangle -L -vn'
alias mountnfs='sudo mount 192.168.200.254:/home/share -t nfs /home/share'
alias loginxiyoulinux='ssh -i /home/tiger/.ssh/id_rsa xiyoulinux@192.168.200.254 -p 89'
alias logintiger='ssh -i /home/tiger/.ssh/id_dsa tiger@192.168.200.254 -p 89'
alias Connect_Router="ssh root@192.168.1.1 -p 36000"
alias vi='vim'
alias Mount_utd8='mount -o utf8'
alias zhcon='zhcon --utf8'
alias Snet='netstat -an'
alias lssh='ls -al | grep sh$'
alias myip='ifconfig eth0 | grep inet | grep -v inet6'

alias CDsrc='cd /usr/local/src'
alias CDpython='cd /Users/tib/python'
alias CDshell='cd /Users/tib/shell'
alias CDusrlocal='cd /usr/local/'
alias CDtib='cd /Users/tib/'
alias CDopenwrt="cd /openwrt"
alias CDopenwrt='cd /BackUp/openwrt'
alias CDopenwrt='cd /openwrt'
alias CDIntoLocalMysql="mysql -h192.168.80.10 -utib -pmeimima"
alias CDintoGit="cd ~/git_root/"
alias CDhadoop="cd /usr/local/hadoop/"
alias CDapache="cd /etc/apache2/"
alias Sest='netstat -an|egrep -i established'
alias CDintoPythonLib="cd /usr/lib64/python2.7"
alias CDmySec='cd /usr/local/src/sec'
alias CDgoagent='cd /Users/tib/Software/goagent-3.2.3/local'

alias CDgit='cd ~/git_root/'

alias ssh_aliyun='ssh root@aliyun -p 33331'
alias ssh_aws='ssh -i ~/.ssh/ssh_to_aws.pem root@aws'
alias ssh_bwg='ssh root@bwg -p 26510 -i ~/.ssh/id_rsa'
alias ssh_openwrt_31='ssh root@192.168.31.1 -p 24'
alias CD_myshadowsocks='cd /Users/tib/git_root/shadowsocks_my/shadowsocks'
alias CD_ss='cd /Users/tib/git_root/ss/shadowsocks'
#fi


### for xiaoenai # :)
alias login_jump='ssh -p38390 xiaohu.liu@rdp01.xiaoenai.net'
alias login_dev='ssh root@172.16.1.11'
alias login_container='ssh root@172.17.0.45'
alias ssh_do='ssh root@tib.f3322.net'

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
fi
export LESS_TERMCAP_mb=$'\E[01;31m'

export LESS_TERMCAP_md=$'\E[01;31m'

#export LESS_TERMCAP_me=$'\E[0m'

#export LESS_TERMCAP_se=$'\E[0m'

#export LESS_TERMCAP_so=$'\E[01;44;33m'

#export LESS_TERMCAP_ue=$'\E[0m'

#export LESS_TERMCAP_us=$'\E[01;32m'
#export PS1="\[\e[31;1m\]\u\[\e[0m\]@\[\e[32;1m\]`/sbin/ifconfig en0|egrep -w "inet"|cut -d: -f 2|cut -d" " -f1`\[\e[0m\]:\[\e[35;1m\]\w\[\e[0m\]\\$ "
export PS1="\[\e[31;1m\]\u\[\e[0m\]@\[\e[32;1m\]`ifconfig en0 |egrep -w inet|awk '{print $2}'`\[\e[0m\]:\[\e[35;1m\]\w\[\e[0m\]\\$ "


#export LANG=zh_CN:UTF-8

export PATH=$PATH:/sbin:/usr/sbin/:~/python/:~/shell/
export PYTHONPATH=$PYTHONPATH:/usr/lib64/python2.7/tib/

#export PYTHONSTARTUP=~/.pythonstartup

export CLICOLOR=1
export LSCOLORS=gxfxaxdxcxegedabagacad
#PythonStartup
PYTHONSTARTUP=~/.pythonconf
export PYTHONSTARTUP
if [ -f ~/.git-completion.bash ]; then
	. ~/.git-completion.bash
fi
export PYTHONSTARTUP=$HOME/.pythonrc.py
