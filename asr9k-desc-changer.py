#!/usr/bin/python

def device_list():
    file_input = open('/home/alwa01/scripts/asr9k-desc-change/routers.txt', 'r')
    device_list = file_input.read()
    for line in device_list.splitlines():
        device_list = device_list.strip()
    return device_list

def main():
    device = device_list()
    print device

if __name__ == "__main__":
    main()
