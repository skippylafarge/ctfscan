#!/usr/bin/env python3

import argparse

import subprocess

import time


PARSER = argparse.ArgumentParser(description='Run basic enumeration scans on a target.')

PARSER.add_argument('--host', type=str, help='IP or hostname')

ARGS = PARSER.parse_args()

TARGET = str(ARGS.host)


def nmap_tcp_scan() -> list: # TODO - note return file object

    filename = 'nmap-tcp-all-ports'
    tee_file = filename + '.tee'
    nmap_cmd = 'nmap -v -p- -sC -sV -oA ' + filename + ' ' + TARGET
    tee_cmd = 'tee ' + tee_file + '\n'
    stuff_cmd = nmap_cmd + ' | ' + tee_cmd + '\n'
    
    nmap_window = subprocess.run(['screen', '-t', 'nmap_tcp'])
    
    nmap = subprocess.run(['screen', '-p', 'nmap_tcp', '-X', 'stuff', stuff_cmd])

    return open(tee_file, 'r', encoding='utf-8')


def gobuster_scan(http_port: str) -> list: 

    target_with_port = TARGET + ':' + http_port

    gobuster = subprocess.run(['gobuster', 'dir', '-x', 'txt', '-w',
                               '/usr/share/wordlists/seclists/Discovery/Web-Content/common.txt',
                               '-u', target_with_port],
                              capture_output=True)

    return gobuster.stdout.split(b'\n')


def gobuster_scans(http_ports: list) -> list:

    return list(map(lambda port: gobuster_scan(port), http_ports))


def is_open_port(line: bytes) -> bool:
    
    return ('tcp' in line or 'udp' in line) and \
        'open' in line and \
        'Discovered' not in line


def is_http_service(line: bytes) -> bool:
    
    return b'http' in line


def get_port_number(line: bytes) -> str:

    return str(line.split(b'/')[0])


def get_port_numbers(list_of_services: list) -> list:

    return list(map(lambda line: get_port_number(line), list_of_services))


def get_lines_with_open_ports(list_of_lines: list) -> list:

    return list(filter(lambda line: is_open_port(line), list_of_lines))


def get_lines_with_http_services(list_of_services: list) -> list:

    return list(filter(lambda line: is_http_service, list_of_services))


def follow_file(file_obj):

    file_obj.seek(0,2)
    while True:
        line = file_obj.readline()
        if not line:
            time.sleep(0.1)
            continue
        print(line)
        if is_open_port(line):
            print(line)
            continue
        if 'Nmap done' in line:
            break


nmap_tcp_scan_file_obj = nmap_tcp_scan()
follow_file(nmap_tcp_scan_file_obj)
# list_of_services = get_lines_with_open_ports(nmap_tcp_scan_results)
# list_of_http_services = get_lines_with_http_services(list_of_services)
# ports_for_http_services = get_port_numbers(list_of_http_services)


