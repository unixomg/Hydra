#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

url = "http://192.168.99.14/zabbix/api_jsonrpc.php"


def test_api():

    header = {
        "content-type": "application/json-rpc"
    }
    data = {
        "jsonrpc": "2.0",
        "method": "apiinfo.version",
        "id": 1,
        "auth": None,
        "params": {}
    }
#     POST http://company.com/zabbix/api_jsonrpc.php HTTP/1.1
# Content-Type: application/json-rpc

# {"jsonrpc":"2.0","method":"apiinfo.version","id":1,"auth":null,"params":{}}

    print "======发送正常数据测试zabbix返回执行结果：======"
    r = requests.post(url, headers=header, data=json.dumps(data))
    print json.dumps(data)
    print "response的状态：{}".format(r.status_code)
    print "response的内容：{}".format(r.content)


if __name__ == '__main__':
    test_api()
