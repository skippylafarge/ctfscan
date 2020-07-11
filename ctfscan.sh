#!/bin/bash

TARGET=$1

NMAP_TCP_PATH=nmap-tcp-all-ports

NMAP_TCP_PATH_TEE=$NMAP_TCP_PATH.tee

GREP_OPEN_HTTP="grep -e 'open.*http' $NMAP_TCP_PATH_TEE"

GOBUSTER_CMD="echo JUST RAN GOBUSTER"

NMAP_TCP_CMD=$"nmap -v -p- -sC -sV -T4 -oA $NMAP_TCP_PATH $TARGET | tee $NMAP_TCP_PATH_TEE\n"

FSWATCH_CMD=$"fswatch -0 -event $NMAP_TCP_PATH_TEE | xargs -0 -n 1 -I {} $GREP_OPEN_HTTP\n"

screen -t nmap_tcp
screen -p nmap_tcp -X stuff "$NMAP_TCP_CMD"
screen -t fswatch
screen -p fswatch -X stuff "$FSWATCH_CMD"

# todo -- run entr command "grep -e "open.*http" nmap-tcp-all-ports.tee | tail -1" on the tee'd nmap output

# for http_port in $OPEN_HTTP_PORTS; do
#     gobuster dir -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -u $TARGET:$http_port | tee gobuster-common-port$http_port
# done

