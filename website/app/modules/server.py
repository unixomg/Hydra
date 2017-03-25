#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from app.models import Server
from app import db
from app.utils import check_field_exists,check_output_field,check_order_by,check_limit,process_result,check_update


def create(**kwargs):
    # 1. 获取参数
    # 2. 验证参数是否合法
    check_field_exists(Server, kwargs,field_none=False)
    server = Server(**kwargs)
    db.session.add(server)
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.warning("插入错误: {} ".format(e.message))
        raise Exception("commit error")
    # 3. 插入到数据库
    # 4. 返回插入的状态
    return server.id


def get(**kwargs):
    # 整理条件
    output = kwargs.get("output", [])
    limit = kwargs.get("limit", 10)
    order_by = kwargs.get("order_by", "id desc")
    where = kwargs.get("where", {})

    # 验证
    # 验证output
    check_output_field(Server, output)
    # 验证order_by
    order_by_list=check_order_by(Server, order_by)

    # 验证limit
    check_limit(limit)

    data = db.session.query(Server).filter_by(**where).order_by \
        (getattr(getattr(Server, order_by_list[0]), order_by_list[1])()).limit(limit).all()
    db.session.close()
    ret = process_result(data, output)

    return ret


def update(**kwargs):
    data = kwargs.get("data", {})
    where = kwargs.get("where", {})
    check_update(Server, data, where)
    ret = db.session.query(Server).filter_by(**where).update(data)
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.warning("commit error: {}".format(e.message))
        raise Exception("commit error")
    return ret


