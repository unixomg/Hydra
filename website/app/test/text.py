#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
import requests
import json

url = "http://0.0.0.0:5000/api"
headers = {"Content-Type": "application/json"}
data = {
    "id": 12,
    "method": "reboot.test",
    "auth": None,
    "params": {"name": "kane"},
    "jsonrpc": "2.0"

}
r = requests.get(url, headers=headers, data=json.dumps(data))
con = json.loads(r.content)

print(r.status_code)
print (r.content)

