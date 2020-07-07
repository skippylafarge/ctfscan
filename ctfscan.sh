#!/bin/bash



NMAP_TCP_CMD="nmap -v -sC -sV -oA"

run_nmap_tcp() {
    screen -t nmap_tcp
    screen -p nmap_tcp -X exec nmap
}
