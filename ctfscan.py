#!/usr/bin/env python3

import argparse
import subprocess

PARSER = argparse.ArgumentParser(description='Run basic enumeration scans on a target.')

PARSER.add_argument('--host', type=str, help='IP or hostname')

ARGS = PARSER.parse_args()

TARGET = ARGS.host


def nmap_tcp_scan() -> list:

    filename = 'nmap-tcp-all-ports'
    tee_file = filename + '.tee'
    
    # nmap = subprocess.run(['nmap', '-v', '-p-', '-sC', '-sV', '-oA', filename, TARGET],
    nmap = subprocess.run(['nmap', '-v', '-p80,8080,443,8443,8000', '-oA', filename, TARGET],
                          capture_output=True)
    
    return nmap.stdout.split(b'\n')


def nmap_udp_scan() -> list:
    
    nmap = subprocess.run(['nmap', '-v', '-sU', '-sC', '-sV', '-oA', 'nmap-udp-top-1000', TARGET],
                         capture_output=True)
    
    return nmap.stdout.split(b'\n')


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
    
    return (b'tcp' in line or b'udp' in line) and \
        b'open' in line and \
        b'Discovered' not in line


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

def print_lines(lst: list):
    for line in lst:
        print(line)


nmap_tcp_scan_results = nmap_tcp_scan()
list_of_services = get_lines_with_open_ports(nmap_tcp_scan_results)
list_of_http_services = get_lines_with_http_services(list_of_services)
ports_for_http_services = get_port_numbers(list_of_http_services)
gobuster_scan_results = gobuster_scans(ports_for_http_services)

print_lines(gobuster_scan_results)
