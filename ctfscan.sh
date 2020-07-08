#!/bin/bash

TARGET=$1

NMAP_TCP_CMD="nmap -v -p- -sC -sV -oA nmap-tcp-all-ports $TARGET
"

screen -t nmap_tcp

wait

screen -p nmap_tcp -X stuff "$NMAP_TCP_CMD"

wait

grep open nmap-tcp-all-ports.nmap > grep-open-tcp-services

wait

grep http grep-open-tcp-services | cut -d '/' -f 1 > open-http-ports

wait

# for http_port in $OPEN_HTTP_PORTS; do
#     gobuster dir -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -u $TARGET:$http_port | tee gobuster-common-port$http_port
# done

