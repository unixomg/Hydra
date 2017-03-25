#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from app.models import Idc
from app import db
from app.utils import check_field_exists, check_output_field, check_order_by, check_limit, process_result, check_update


def create(**kwargs):
    # 1. 获取参数
    # 2. 验证参数是否合法
    check_field_exists(Idc, kwargs)
    idc = Idc(**kwargs)
    db.session.add(idc)
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.warning("插入错误: {} ".format(e.message))
        raise Exception("commit error")
    # 3. 插入到数据库
    # 4. 返回插入的状态
    return idc.id


def get(**kwargs):
    # 整理条件
    output = kwargs.get("output", [])
    limit = kwargs.get("limit", 10)
    order_by = kwargs.get("order_by", "id desc")
    where = kwargs.get("where", {})

    # 验证
    # 验证output
    check_output_field(Idc, output)
    # 验证order_by
    order_by_list = check_order_by(Idc, order_by)

    # 验证limit
    check_limit(limit)

    data = db.session.query(Idc).filter_by(**where).order_by \
        (getattr(getattr(Idc, order_by_list[0]), order_by_list[1])()).limit(
            limit).all()
    #[ < app.models.Idc object at 0x7fe9ed3eca90 >]
    # print data
    print "sqlachemy Query 结果"
    print data
    #sqlachemy Query 结果
    #[<app.models.Idc object at 0x7f7cd80bec50>]
    db.session.close()
    ret = process_result(data, output)
    #[{'status': 1L, 'name': u'YZ', 'user_phone': u'18888888888', 'idc_name': u'\u4ea6\u5e84\u673a\u623f','rel_cabinet_num': 50L, 'email': u'unixomg@163.com', 'phone': u'18519237136', 'user_interface': u'kevin','address': u'\u4ea6\u5e84\u7ecf\u6d4e\u5f00\u53d1\u533a', 'pact_cabinet_num': 60L, 'id': 1L}]
    # print ret

    return ret


def update(**kwargs):
    data = kwargs.get("data", {})
    where = kwargs.get("where", {})
    check_update(Idc, data, where)
    ret = db.session.query(Idc).filter_by(**where).update(data)
    # 1
    # printinstall ret
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.warning("commit error: {}".format(e.message))
        raise Exception("commit error")
    return ret
