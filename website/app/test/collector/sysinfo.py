#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
采集机器自身信息

1 主机名
2 内存
3 ip与mac地址
4 cpu信息
5 硬盘分区信息
6 制造商信息
7 出厂日期
8 系统版本
"""

import json
import subprocess
import psutil
import socket
import time
import re
import platform
import requests

device_white = ["eth1", "eth2", "eth3", "bond0", "bond1"]


def get_hostname():
    return socket.gethostname()


def get_meminfo():
    with open('/proc/meminfo') as mem_open:
        a = int(mem_open.readline().split()[1])
        return a / 1024


def get_device_info():
    ret = []
    for device, device_info in psutil.net_if_addrs().iteritems():
        if device in device_white:
            tmp_device = {}
            for snic in device_info:
                if snic.family == 2:
                    tmp_device['ip'] = snic.address
                if snic.family == 17:
                    tmp_device['mac'] = snic.address
            ret.append(tmp_device)
    return ret


def get_cpuinfo():
    ret = {"cpu": '', 'num': 0}
    with open('/proc/cpuinfo') as f:
        for line in f:
            line_list = line.strip().split(':')
            key = line_list[0].rstrip()
            if key == "model name":
                ret['cpu'] = line_list[1].lstrip()
            if key == "processor":
                ret['num'] += 1
    return ret


def get_diskinfo():
    # cmd = """'/sbin/fdisk -l | grep platte|grep -v 'identifier|mapper|Disklabel'"""
    #cmd = """sudo /sbin/fdisk -l|grep Platte|egrep -v 'identifier|mapper|Disklabel'"""

    cmd = """sudo /sbin/fdisk -l|grep Disk|egrep -v 'identifier|mapper|Disklabel'"""
    disk_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    partition_size = []
    for dev in disk_data.stdout.readlines():
        size = int(dev.strip().split(',')[1].split()[0]) / 1024 / 1024 / 1024
        partition_size.append(str(size))
    return " + ".join(partition_size)


def get_Manufacturer():
    cmd = """sudo /usr/sbin/dmidecode | grep -A6 'System Information'"""
    ret = {}
    manufacturer_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in manufacturer_data.stdout.readlines():
        if "Manufacturer" in line:
            ret['manufacturers'] = line.split(': ')[1].strip()
        elif "Product Name" in line:
            ret['server_type'] = line.split(': ')[1].strip()
        elif "Serial Number" in line:
            ret['st'] = line.split(': ')[1].strip().replace(' ', '')
        elif "UUID" in line:
            ret['uuid'] = line.split(': ')[1].strip()
    return ret
    # return manufacturer_data.stdout.readline().split(': ')[1].strip()

# 出厂日期


def get_rel_date():
    cmd = """sudo /usr/sbin/dmidecode | grep -i release"""
    data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    date = data.stdout.readline().split(': ')[1].strip()
    return re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', date)


def get_os_version():
    return " ".join(platform.linux_distribution())



def get_innerIp(ipinfo):
    #[{'ip': '192.168.99.12', 'mac': '08:00:27:31:76:81'}]
    inner_device = ["eth1", "bond0"]
    ret = {}
    interface={}
    for info in ipinfo:
        for device, device_info in psutil.net_if_addrs().iteritems():
            print device,device_info
            if device in inner_device:
                for snic in device_info:
                    if snic.address == info['ip']:
                        interface['device'] = device
                    if info.has_key('ip') and interface['device'] in inner_device:
                        ret['inner_ip'] = info['ip']
                        ret['mac_address'] = info['mac']
                        return ret
    return {}


def run():
    data = {}
    data['hostname'] = get_hostname()
    device_info = get_device_info()
    data.update(get_innerIp(device_info))
    data['ipinfo'] = json.dumps(device_info)

    cpuinfo = get_cpuinfo()
    data['server_cpu'] = "{cpu} {num}".format(**cpuinfo)
    data['server_disk'] = get_diskinfo()
    data['server_mem'] = get_meminfo()
    data.update(get_Manufacturer())
    data['manufacture_date'] = get_rel_date()
    data['os'] = get_os_version()
    # if "VMware" in data['manufacturers']:
    if 'VirtualBox' == data['server_type']:
        data['vm_status'] = 0
    else:
        data['vm_status'] = 1
    send(data)
    # print data
    # return data


def send(data):
    url = "http://192.168.99.10:8000/resources/server/reporting/"
    r = requests.post(url, data=data)
    print data
    print r

if __name__ == '__main__':
    print "======测试get sysinfo:======"
    run()
   
