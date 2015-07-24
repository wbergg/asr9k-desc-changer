#!/usr/bin/python

import paramiko
import time

def main():
    file_input = open('routerrs.txt', 'r')
    device_list = file_input.read()
    device_list = device_list.strip().split("\n")
    username = 'xxx'
    password = 'xxx'
    for device in device_list:
        output = list()
        output2 = list()
        print "Getting configuration from %s" % device
        remote_conn_pre=paramiko.SSHClient()
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_conn_pre.connect(device, username=username, password=password)
        remote_conn = remote_conn_pre.invoke_shell()
        remote_conn.send("terminal length 0\n")
        remote_conn.send("show interface description\n")
        time.sleep(1)
        router_data = remote_conn.recv(5000)
        output.append(router_data)
        for line in output:
            data = line.strip().split("\n")
            for words in data:
                if '"' in words:
                    words = (words.replace('"', ''))
                    output2.append(words.split(None,3))
        for line in output2:
            if 'BE' in line[0]:
                line[0] = (line[0].replace('BE', 'Bundle-Ether'))
        if len(output2) == 0:
            print "No config change required for %s" % device
        else:
            print "Will now send configuration to %s" % device
            remote_conn.send("conf t\n")
            for line in output2:
                remote_conn.send("interface %s\n" % line[0])
                remote_conn.send("description %s\n" % line[3])
                time.sleep(1)
                router_output = remote_conn.recv(5000)
                #For debug purpose, if you want to see what's actually sent
                #print router_output
            remote_conn.send("commit\n")
            router_output = remote_conn.recv(1000)
            if len(router_output) == 39:
                print "Done with %s, everything went OK!" % device
            else:
                print "Something went wrong with the commit in %s" % device
            remote_conn.close()

if __name__ == "__main__":
    main()

