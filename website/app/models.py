#!/usr/bin/env python
# coding:utf-8
from datetime import datetime

from app import db

class Idc(db.Model):
    __tablename__        = "idc"
    id                   = db.Column(db.Integer, primary_key = True)
    name                 = db.Column(db.String(50), index = True, nullable = False, unique = True)
    idc_name             = db.Column(db.String(50), nullable=False)
    address              = db.Column(db.String(255), nullable=False)
    phone                = db.Column(db.String(20), nullable=False)
    email                = db.Column(db.String(50), nullable=False)
    user_interface       = db.Column(db.String(50), nullable=False)
    user_phone           = db.Column(db.String(20), nullable=False)
    rel_cabinet_num      = db.Column(db.Integer, nullable=False)
    pact_cabinet_num     = db.Column(db.Integer, nullable=False)
    status               = db.Column(db.Integer, index = True, default = 1)

class Status(db.Model):
    __tablename__       = 'status'
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(50), unique=True, nullable=False)

class Manufacturers(db.Model):
    __tablename__       = 'manufacturers'
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(50),unique=True, nullable=False)



class ServerType(db.Model):
    __tablename__       = 'server_type'
    id                  = db.Column(db.Integer, primary_key=True)
    type                = db.Column(db.String(50), nullable=False, default='')
    manufacturers_id    = db.Column(db.Integer, index=True, default=0)


class Product(db.Model):
    __tablename__       = 'product'
    id                  = db.Column(db.Integer, primary_key=True)
    service_name        = db.Column(db.String(50), nullable=False, default='')
    pid                 = db.Column(db.Integer, index=True, nullable=False)
    module_letter       = db.Column(db.String(15), nullable=False, default='')
    dev_interface       = db.Column(db.String(100), nullable=False, default='')
    op_interface        = db.Column(db.String(100), nullable=False, default='')


class Power(db.Model):
    __tablename__       = 'power'
    id                  = db.Column(db.Integer, primary_key=True)
    server_power        = db.Column(db.String(50), unique=True, default='')

class Cabinet(db.Model):
    __tablename__       = 'cabinet'
    id                  = db.Column(db.Integer, primary_key=True,)
    name                = db.Column(db.String(50), nullable=False, unique=True)
    idc_id              = db.Column(db.String(10), index=True, nullable=False)
    power               = db.Column(db.String(10))


class Raid(db.Model):
    __tablename__       = 'raid'
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(50), unique=True, default='')

class RaidType(db.Model):
    __tablename__       = 'raidtype'
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(50), unique=True, default='')


class ManagementCard(db.Model):
    __tablename__       = 'management_card'
    id                  = db.Column(db.Integer, primary_key=True)
    m_type              = db.Column(db.String(50), unique=True, default='')

class Supplier(db.Model):
    __tablename__       = 'supplier'
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(50), unique=True, default='')



class Server(db.Model):
    __tablename__       = 'server'
    id                  = db.Column(db.Integer, primary_key=True)
    supplier            = db.Column(db.String(400), nullable=True, default='')
    manufacturers       = db.Column(db.String(100), nullable=True, default='')
    manufacture_date    = db.Column(db.Date)
    server_type         = db.Column(db.String(50), nullable=True, default='')
    st                  = db.Column(db.String(50), nullable=True, default='')
    assets_no           = db.Column(db.String(50), nullable=True, default='')
    idc_id              = db.Column(db.String(32), nullable=True, index=True, default=0)
    cabinet_id          = db.Column(db.Integer, nullable=True, index=True, default=0)
    uuid                = db.Column(db.String(50), index=True, default='')
    cabinet_pos         = db.Column(db.String(15), nullable=True, default='')
    expire              = db.Column(db.Date)
    ups                 = db.Column(db.Integer, nullable=True, default=0)
    parter              = db.Column(db.String(50), nullable=True)
    parter_type         = db.Column(db.String(50), nullable=True)
    server_up_time      = db.Column(db.Date)
    os                  = db.Column(db.String(50), index=True, nullable=True, default='')
    hostname            = db.Column(db.String(30), index=True, default='')
    inner_ip            = db.Column(db.String(50), index=True, nullable=True, default='')
    mac_address         = db.Column(db.String(50), nullable=True, default='')
    ipinfo              = db.Column(db.String(100), nullable=True, default='')
    server_cpu          = db.Column(db.String(50), nullable=True, default='')
    server_disk         = db.Column(db.String(50), nullable=True, default='')
    server_mem          = db.Column(db.String(50), nullable=True, default='')
    raid                = db.Column(db.String(50), nullable=True, default='')
    raid_card_type      = db.Column(db.String(50), nullable=True, default=0)
    remote_card         = db.Column(db.String(50), nullable=True, default=0)
    remote_cardip       = db.Column(db.String(50), nullable=True, default='')
    status              = db.Column(db.Integer, nullable=True, default=0)
    remark              = db.Column(db.Text, nullable=True, default='')
    last_op_time        = db.Column(db.DateTime, nullable=True,default=datetime.utcnow)
    last_op_people      = db.Column(db.Integer, nullable=True, default=0)
    monitor_mail_group  = db.Column(db.String(50), nullable=True, default='')
    service_id          = db.Column(db.Integer, nullable=True, default=0)
    server_purpose      = db.Column(db.Integer, nullable=True, default=0)
    trouble_resolve     = db.Column(db.Integer, nullable=True, default=0)
    op_interface_other  = db.Column(db.Integer, nullable=True, default=0)
    dev_interface       = db.Column(db.Integer, nullable=True, default=0)
    check_update_time   = db.Column(db.DateTime)
    vm_status           = db.Column(db.Integer, index=True, nullable=True, default=0)
    power               = db.Column(db.String(30), nullable=True, default='')
    host                = db.Column(db.Integer, default=0)


class Zbhost(db.Model):
    __tablename__ = "zbhost"
    id = db.Column(db.Integer, primary_key=True)
    cmdb_hostid = db.Column(db.Integer, index=True, unique=True) #cmdb中的host id
    hostid = db.Column(db.Integer, index=True, unique=True) #通过zabbix api获取的hostid
    host = db.Column(db.String(30))
    ip = db.Column(db.String(30))


class GraphiteKeys(db.Model):
    __tablename__ = "graphite_keys"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    type = db.Column(db.String(30))
    title = db.Column(db.String(30))
    status = db.Column(db.Integer, index=True, default=0)


class GraphiteGroupKey(db.Model):
    __tablename__ = "graphite_group_key"
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, index=True)
    key_id = db.Column(db.Integer)