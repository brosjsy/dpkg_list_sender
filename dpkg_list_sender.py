#!/usr/bin/env python
import os
import socket
import json
from datetime import datetime

with open("/etc/os-release") as f:
    dict_os_release = {}
    for line in f:
        k,v = line.rstrip().split("=")
        dict_os_release[k] = v

os_version = (dict_os_release['VERSION_ID']).strip('\"')
host = os.uname()[1]
UDP_IP = "127.0.0.1"
UDP_PORT = 514

lines = os.popen('dpkg -l | grep "^ii"').read().split('\n')[5:-1]
i = 0
while len([l for l in lines[i].split('  ') if l]) != 5:
   i += 1
offsets = [lines[i].index(l) for l in lines[i].split('  ') if len(l)]
pkgs = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for line in lines:
    parsed = []
    for i in range(len(offsets)):
        if len(offsets) == i + 1:
            parsed.append(line[offsets[i]:].strip())
        else:
            parsed.append(line[offsets[i]:offsets[i + 1]].strip())
    my_date = datetime.now()
    pkgs.update({'atime':my_date.isoformat(),'h_name':host,'p_name':parsed[1],'ver':parsed[2],'plat':parsed[3],'os':os_version})
    sock.sendto(json.dumps(pkgs,sort_keys=True).encode(), (UDP_IP, UDP_PORT))
