#!/bin/bash


#if [ $# -ne 6 ];then
#	echo -e "Usage:\n\t $0 \"\" \"\"  \"\"  \"\" \"\" "
#	exit 1
#fi

echo -e "1.抓取从eth0来的源主机a.a.a.a 目标端口bbbb 的 UDP数据包，数目10个,并且显示每个包的ASCII,并且不解析IP和PORT"
echo -e "  tcpdump  -i eth0  -nn udp dst port bbbb and src host a.a.a.a -t -X -c 10"
echo -e "2.抓取源网络 192.168.0.0/16 且 目标网络是10.0.0.0/8 或者 172.16.0.0/16"
echo -e "  tcpdump -nvX src net 192.168.0.0/16 and dst net 10.0.0.0/8 or 172.16.0.0/16"
echo -e "3."
echo -e "  tcpdump -nvvXSs 1514 dst 192.168.0.2 and src net and not icmp"
echo -e "4."
echo -e "  tcpdump src 10.0.2.4 and (dst port 3389 or 22)"
echo -e "5."
echo -e "  tcpdump -nnvvS src 10.5.2.3 and dst port 3389"
echo -e "6.抓取小于32 bytes的包"
echo -e "  tcpdump less 32"
echo -e "7.抓取大于128 bytes的包"
echo -e "  tcpdump greater 128"
echo -e "8.显示所有可以监听的interface"
echo -e "  tcpdump -D"
echo -e "9.tcp 端口范围1-1023"
echo -e "  tcpdump -n tcp dst portrange 1-1023"
echo -e "10.Capture 500 bytes of data for each packet rather than the default of 68 bytes"
echo -e "  tcpdump -s 500"
echo -e "11.Capture all bytes of data within the packet"
echo -e "  tcpdump -s 0"
echo -e "12.Capture any packets with destination IP 192.168.1.1 and destination port 80 or 443. Display IP addresses and port numbers"
echo -e "  tcpdump -n \"dst host 192.168.1.1 and (dst port 80 or dst port 443)\""
#echo -e "tcpdump src 10.0.2.4 and (dst port 3389 or 22)"
#echo -e "tcpdump src 10.0.2.4 and (dst port 3389 or 22)"
#echo -e "tcpdump src 10.0.2.4 and (dst port 3389 or 22)"
