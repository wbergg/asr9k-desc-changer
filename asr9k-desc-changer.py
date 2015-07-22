#!/usr/bin/python

import paramiko
import time

def device_list():
    file_input = open('routers.txt', 'r')
    device_list = file_input.read()
    device_list.splitlines()
    for line in device_list.splitlines():
        device_list = device_list.strip()
    return device_list

def get_data(device_list):
    device_list = device_list.split("\n")
    output = []
    username = 'xxx'
    password = 'xxx'
    for device in device_list:
        print "At device: " % device
        remote_conn_pre=paramiko.SSHClient()
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_conn_pre.connect(device, username=username, password=password)
        remote_conn = remote_conn_pre.invoke_shell()
        remote_conn.send("terminal length 0\n")
        remote_conn.send("show interface description\n")
        time.sleep(1)
        router_data = remote_conn.recv(5000)
        output.append(router_data)
    return output

def parse(router_data):
    output = []
    for line in router_data:
        data = line.strip().split("\n")
        for words in data:
            if '"' in words:
                words = (words.replace('"', ''))
                output.append(words.split(None,3))

    for line in output:
        if 'BE' in line[0]:
            line[0] = (line[0].replace('BE', 'Bundle-Ethernet'))
    return output

def main():
    device = device_list()
    router_data = get_data(device)
    mongo = parse(router_data)

if __name__ == "__main__":
    main()
