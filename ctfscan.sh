#!/bin/bash

TARGET=$1

NMAP_TCP_CMD="nmap -v -p- -sC -sV -oA nmap-tcp-all-ports $TARGET | tee nmap-tcp-all-ports.tee
"

screen -t nmap_tcp
NMAP_TCP_RESULTS=$(screen -p nmap_tcp -X exec $NMAP_TCP_CMD)

OPEN_TCP_SERVICES=$(grep open nmap-tcp-all-ports.nmap | grep tcp)

OPEN_HTTP_PORTS=$(grep "tcp\&open" $NMAP_TCP_RESULTS | cut -d '/' -f 1)

for http_port in $OPEN_HTTP_PORTS; do
    gobuster dir -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -u $TARGET:$http_port | tee gobuster-common-port$http_port
done



    
