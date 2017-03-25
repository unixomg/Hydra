#!/usr/bin/env python
# -*- coding: utf-8 -*-



from __future__ import print_function
import requests
import json

url = "http://0.0.0.0:8000/api"


def test_api():
    headers = {"Content-Type": "application/json"}
    data = {
        "id": 12,
        "jsonrpc": "2.0",
        "method": "idc.create",
        "auth": None,
        "params": {
            'name':"YZ",
            "idc_name":"亦庄机房",
            "address":"亦庄经济开发区",
            "phone":"18519237136",
            "email":"unixomg@163.com",
            "user_interface":"kevin",
            "user_phone":"18888888888",
            "rel_cabinet_num":50,
            "pact_cabinet_num":60,
           },

    }
    r = requests.get(url, headers=headers, data=json.dumps(data))
    print(r.status_code)
    print(r.content)


# con = json.loads(r.content)
if __name__ == "__main__":
    test_api()
