#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
from . import main
from flask import request, current_app,redirect,render_template
from app.base import JsonRpc
import json

@main.route('/', methods=['GET', 'POST'])
def index():
    current_app.logger.debug("访问日志")
    return redirect('/dashboard/')

@main.route('/dashboard/',methods=['GET'])
def dashboard():
    return render_template("public/dashboard.html")





@main.route("/api", methods=["GET", "POST"])
def api():
    # application/json
    # application/json-rpc
    allowed_content = ["application/json", "application/json-rpc"]
    if request.content_type in allowed_content:
        jsonData = request.get_json()
        jsonrpc = JsonRpc()
        jsonrpc.jsonData = jsonData
        ret = jsonrpc.execute()
        #[{'status': 1L, 'name': u'YZ', 'user_phone': u'18888888888', 'idc_name': u'\u4ea6\u5e84\u673a\u623f', 'rel_cabinet_num': 50L, 'email': u'unixomg@163.com', 'phone': u'18519237136', 'user_interface': u'kevin', 'address': u'\u4ea6\u5e84\u7ecf\u6d4e\u5f00\u53d1\u533a', 'pact_cabinet_num': 60L, 'id': 1L}]
        #print ret
        return json.dumps(ret)
    else:
        return "error"
