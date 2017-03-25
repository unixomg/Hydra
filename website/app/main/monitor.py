#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.base.zabbix import Zabbix, get_zabbix_data, zabbix_link_template
from . import main
import json
from app.utils import Treeview
from app.utils.graphite import get_graphite_keys
from app.utils import api_action,get_product
from flask import render_template, request
from app.models import db, GraphiteKeys, GraphiteGroupKey
from flask import render_template, request, current_app


"""
    Graphite性能展示
"""
@main.route("/monitor/performance/product", methods=['GET'])
def monitor_performance_product():

    data = get_product()
    print "性能数据"
    print "--------"
    print data
    """
    [{'item': [{'type': u'si', 'key': u'system.cpu.load1', 'title': u'load1'}, {'type': u'si', 'key': u'system.cpu.load5', 'title': u'load5'}, {'type': u'si', 'key': u'system.cpu.load15', 'title': u'load15'}], 'product': 'MS/APP', 'hostlist': [u'devops', u'ms-web-01']}, {'item': [], 'product': 'MS/Web', 'hostlist': []}]
    """
    return render_template("monitor/monitor_graphite_product.html",
                           data=json.dumps(data), graphite_api="{}render/?".format(current_app.config.get("GRAPHITE_SERVER")),
                           show_performance_product=True,
                           show_monitor=True)




"""
    获取zabbix里 所有的hostgroup
"""


@main.route("/monitor/ajax/get_zabbix_host_groups", methods=['POST'])
def monitor_get_zabbix_host_groups():
    zb = Zabbix()
    data = zb.get_hostgroup()
    return json.dumps(data)


"""
    zabbix 模版绑定
"""


@main.route("/monitor/zabbix", methods=['GET'])
def monitor_zabbix():
    zb = Zabbix()
    templates = zb.zb.template.get(output=["templateid", "name"])
    # [{u'name': u'Template OS Linux', u'templateid': u'10001'},.......]
    #print templates
    templates_data = []

    for temp in templates:
        templates_data.append({"label": temp['name'], "value": temp['templateid']})

    tv = Treeview()
    treeview = tv.get()
    #[{'value': u'10001', 'label': u'Template OS Linux'},.......]
    #print templates_data
    #[{'text': u'ms', 'nodes': [{'text': u'app', 'pid': 1L, 'type': 'product', 'id': 3L}, {'text': u'web', 'pid': 1L, 'type': 'product', 'id': 2L}], 'type': 'service', 'id': 1L}]
    #print treeview
    return render_template("monitor/monitor_zabbix.html",
                           treeview=json.dumps(treeview), 
                           templates=json.dumps(templates_data),
                           show_zabbix=True,
                           show_monitor=True)

"""
    获取zabbix的主机，以及已link的模版
"""


@main.route("/monitor/ajax/get_zabbix_data_by_group", methods=["POST"])
def monitor_get_zabbix_data_by_group():
    if request.method == "POST":
        params = request.form.to_dict()
        # {'server_purpose': u'3', 'service_id': u '1'}
        # 取出响应的server id [{'id': 1L}]

        hosts = api_action("server.get", {"output": ["id"], "where": {"server_purpose": params[
                           "server_purpose"], "service_id": params["service_id"]}})
        print hosts
        #[{'id': 2L}, {'id': 1L}]
        ret = get_zabbix_data(hosts)
        print "获取到zabbix的相关信息"
        print ret
        """
        获取到zabbix的相关信息
[{'templates': [{u'name': u'Template OS Linux', u'templateid': u'10001'}], 'hostname': u'ms-web-01', 'hostid': 10111L}, {'templates': [{u'name': u'Template OS Linux', u'templateid': u'10001'}], 'hostname': u'devops', 'hostid': 10112L}]
        """
        return json.dumps(ret)
    return ""

"""
    zabbix 模版解除绑定
"""


@main.route("/monitor/ajax/unlink_zabbix_template", methods=["POST"])
def monitor_unlink_zabbix_template():
    if request.method == "POST":
        params = request.form.to_dict()
        # print params
        # {'hostid': u'10113', 'templateid': u'10115'}
        zb = Zabbix()
        ret = zb.unlink_template(params['hostid'], params['templateid'])
        if ret:
            return "1"
        else:
            return ret


"""
    zabbix 模版绑定
"""


@main.route("/monitor/ajax/link_zabbix_template", methods=["POST"])
def monitor_link_zabbix_template():
    if request.method == "POST":
        params = request.form.to_dict()
        # {'hostids': u'10113','template_ids': u'10066'}
        templateids = params['template_ids'].split(",")
        hostids = params['hostids'].split(",")
        ret_data = zabbix_link_template(hostids, templateids)
        # [{u'hostids':[u'10113']}]
        # [('Code: -32602, Message: Invalid params., Data: Cannot find host interface on "reboot-ms-wet-01" for item key "ifDescr".',)]
        flag = True
        for ret in ret_data:
            if not isinstance(ret, dict):
                flag = False
        if flag:
            return "1"
        else:
            return json.dumps(ret_data)


@main.route("/monitor/graphite/keys/", methods=['GET'])
def monitor_graphite_keys():
    """ graphite keys 管理
    """
    graphitekey = db.session.query(GraphiteKeys).all()
    print graphitekey
    db.session.close()
    return render_template("monitor/monitor_graphite_keys.html",
                           graphite_keys=graphitekey,
                           show_monitor=True,
                           show_graphite_keys=True)


@main.route("/monitor/graphite/keys/add", methods=['POST'])
def monitor_graphite_key_add():
    """ajax 添加graphite key
    """
    if request.method == "POST":

        data = request.form.to_dict()
        try:
            graphitekey = GraphiteKeys(**data)
            db.session.add(graphitekey)
            db.session.commit()
            return "1"
        except Exception, e:
            return e.args

    return "400"


@main.route("/monitor/ajax/graphite/get/all/keys/", methods=['POST'])
def monitor_graphite_get_all_keys_():
    """ajax 取得所有的graphite key
    """

    keys = get_graphite_keys()
    print "ajax异步请求获取的graphite key列表"
    print keys
    return json.dumps(keys)


@main.route("/monitor/graphite/groups/", methods=['GET'])
def monitor_graphite_groups():
    """graphite key 与 group 关联
    """

    graphitekey = db.session.query(GraphiteKeys).all()
    db.session.close()
    keys = []
    for s in graphitekey:
        keys.append({"value": s.id, "text": s.name})
    tv = Treeview()
    treeview = tv.get()
    #print "打印keys"
    #print keys
    #[{'text': u'system.cpu.load1', 'value': 1L}, {'text': u'system.cpu.load5', 'value': 2L}, {'text': u'system.cpu.load15', 'value': 3L}]
    #print json.dumps(keys)
    #[{"text": "system.cpu.load1", "value": 1}, {"text": "system.cpu.load5", "value": 2}, {"text": "system.cpu.load15", "value": 3}]
    #print "打印treeview"
    #print treeview
    #[{'text': u'MS', 'nodes': [{'text': u'APP', 'pid': 1L, 'type': 'product', 'id': 3L}, {'text': u'Web', 'pid': 1L, 'type': 'product', 'id': 2L}], 'type': 'service', 'id': 1L}]
    #print json.dumps(treeview)
    #[{"text": "MS", "nodes": [{"text": "APP", "pid": 1, "type": "product", "id": 3}, {"text": "Web", "pid": 1, "type": "product", "id": 2}], "type": "service", "id": 1}]
    return render_template("monitor/graphite_group_keys.html",
                           treeview=json.dumps(treeview), hosts=json.dumps(keys),
                           show_monitor=True,
                           show_graphite_groups=True)


@main.route("/monitor/ajax/graphite/group/get_keys", methods=['POST'])
def monitor_graphite_group_get_keys():
    """ajax 添加graphite key
    """

    data = request.form.to_dict()
    print "ajax获取的组key"
    print data
    """
    ajax获取的组key
{'service_id': u'3'}
    """
    group_keys = db.session.query(GraphiteGroupKey).filter_by(**data).all()
    key_ids = [str(group_key.key_id) for group_key in group_keys]
    """
    SELECT graphite_group_key.id AS graphite_group_key_id, graphite_group_key.service_id AS graphite_group_key_service_id, graphite_group_key.key_id AS graphite_group_key_key_id 
FROM graphite_group_key 
WHERE graphite_group_key.service_id = %s
2017-03-21 22:53:03,264 INFO sqlalchemy.engine.base.Engine ('3',)
    print key_ids
"""
    return json.dumps(key_ids)


@main.route("/monitor/ajax/graphite/add/key/group", methods=['POST'])
def monitor_graphite_add_key_to_group():
    """ajax 将graphite key 关联到group上
    """
    data = request.form.to_dict()
    print "关联的grapite key数据"
    print data
    """
    关联的load15
    关联的grapite key数据
{'service_id': u'3', 'key_id': u'3'}
    """
    r = db.session.query(GraphiteGroupKey).filter_by(**data).all()
    if not r:
        try:

            db.session.add(GraphiteGroupKey(**data))
            db.session.commit()
            return "1"
        except Exception, e:
            return e.args

    return "400"


@main.route("/monitor/ajax/graphite/del/key/group", methods=['POST'])
def monitor_graphite_del_key_to_group():
    """ajax 将graphite key 取消关联到group上
    """
    data = request.form.to_dict()
    print "取消关联的graphite key数据"
    print data
    """
    取消关联load15
    取消关联的graphite key数据
{'service_id': u'3', 'key_id': u'3'}
    """
    ret = db.session.query(GraphiteGroupKey).filter_by(**data).delete()
    db.session.commit()
    if ret:
        return str(ret)
    else:
        return "0"


