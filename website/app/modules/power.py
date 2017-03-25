#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from app.models import Power
from app import db
from app.utils import check_field_exists,check_output_field,check_order_by,check_limit,process_result,check_update


def create(**kwargs):
    # 1. 获取参数
    # 2. 验证参数是否合法
    check_field_exists(Power, kwargs)
    power = Power(**kwargs)
    db.session.add(power)
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.warning("插入错误: {} ".format(e.message))
        raise Exception("commit error")
    # 3. 插入到数据库
    # 4. 返回插入的状态
    return power.id


def get(**kwargs):
    # 整理条件
    output = kwargs.get("output", [])
    limit = kwargs.get("limit", 10)
    order_by = kwargs.get("order_by", "id desc")
    where = kwargs.get("where", {})

    # 验证
    # 验证output
    check_output_field(Power, output)
    # 验证order_by
    order_by_list=check_order_by(Power, order_by)

    # 验证limit
    check_limit(limit)

    data = db.session.query(Power).filter_by(**where).order_by \
        (getattr(getattr(Power, order_by_list[0]), order_by_list[1])()).limit(limit).all()
    db.session.close()
    ret = process_result(data, output)

    return ret


def update(**kwargs):
    data = kwargs.get("data", {})
    where = kwargs.get("where", {})
    check_update(Power, data, where)
    ret = db.session.query(Power).filter_by(**where).update(data)
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.warning("commit error: {}".format(e.message))
        raise Exception("commit error")
    return ret


