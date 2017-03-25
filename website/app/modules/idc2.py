#!/usr/bin/env python
from flask import current_app

from app.models import db, Idc


def create(**kwargs):
    # 1 获取参数
    # 2 检查参数
    for field in kwargs.keys():
        if not hasattr(Idc, field):
            current_app.logger.warning("参数错误.{} 不在idc这张表里".format(field))
            raise Exception("params error:{}".format(field))
        if not kwargs.get(field, None):
            current_app.logger.warning("参数错误.{} 不能为空 ").format(field)
            raise Exception("{}不能为空".format(field))
    # 3 插入数据库
    idc = Idc(**kwargs)
    db.session.add(idc)
    try:
        db.session.commit()
    except Exception, e:
        current_app.logger.warning("commit error:{}".format(e.message))
        raise Exception("commit error")

    return idc.id


def get(**kwargs):
    # 整理条件
    output = kwargs.get("output", [])
    limit = kwargs.get("limit", 10)
    order_by = kwargs.get("order_by", "id desc")
    where = kwargs.get("where", {})

    # 验证
    # 验证output
    if not isinstance(output, list):
        current_app.logger.warning("output 必须为list")
        raise Exception("output 必须为list")
    for field in output:
        if not hasattr(Idc, field):
            current_app.logger.warning("{}这个输出字段不存在".format(field))
            raise Exception("{}这个输出字段不存在".format(field))
    # order "id desc"
    tmp_order_by = order_by.split('.')
    if len(tmp_order_by) != 2:
        current_app.logger.warning("order by 参数不正确")
        raise Exception("order by 参数不正确")
    order_by_list = ["desc", "asc"]
    if tmp_order_by[1].lower() not in order_by_list:
        current_app.logger.warning("排序参数不正确")
        raise Exception("排序参数不正确")
    if not hasattr(Idc, tmp_order_by[0].lower()):
        current_app.logger.warning("排序字段不在表中")
        raise Exception("排序字段不在表中")

    # limit
    if not str(limit).isdigit():
        raise Exception("limit 必须为数字")

    data = db.session.query(Idc), filter(**where)\
        .order_by(getattr(getattr(Idc, tmp_order_by[0]), tmp_order_by[1])()).limit(limit).all
    print "sqlachemy Query 结果"
    print data
    #sqlachemy Query 结果
    #[<app.models.Idc object at 0x7f7cd80bec50>]
    db.session.close()
    ret = []
    for obj in data:
        if output:
            tmp = {}
            for f in output:
                tmp[f] = getattr(obj, f)
                ret.append(tmp)
        else:
            tmp = obj.__dict__
            tmp.pop("_sa_instance_state")
            ret.append(tmp)
    return ret


def update(**kwargs):
    data = kwargs.get("data", {})
    where = kwargs.get("where", {})

    if not data:
        raise Exception("没有需要更新的内容")

    for field in data.keys():
        if not hasattr(Idc, field):
            raise Exception("需要更新的{}这个字段不存在".format(field))

    if not where:
        raise Exception("还需要提供where条件")

    if not where.get("id", None):
        raise Exception("需要提供id作为更新条件")

    if str(where.get("id")).isdigit():
        if int(where.get("id")) <= 0:
            raise Exception("id的值必须为大于0的整数")
        else:
            where = {"id": where.get("id")}
    else:
        raise Exception("id的值必须为大于0的整数")

    ret = db.session.query(Idc).filter_by(**where).update(data)
    try:
        db.session.commit()
    except Exception, e:
        current_app.logger.warning("commit error:{}".format(e.message))
        raise Exception("commit server")
    return ret
