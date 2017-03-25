#!/usr/bin/env python
# coding:utf-8
import os
import imp
import json
from flask import current_app


class AutoLoad():
    """
        自动加载模块

    """

    def __init__(self):
        # 指定项目自动加载模块的目录
        self.modules_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "modules"))
        current_app.logger.debug("自动加载模块目录为:{}".format(self.modules_dir))
        # idc.get  获取方法
        # 模块名
        self.module_name = ""
        # 函数名
        self.func = ""
        # 已加载的模块
        self.module = None

    def isValidModule(self, module_name):
        """
        验证模块是否可用
        :param module_name: 需要导入的模块名
        :return: True/False
        """
        current_app.logger.debug("验证模块是否可用,模块名为:{}".format(module_name))
        self.module_name = module_name
        return self._load_module()

    def isValidMethod(self, func):
        """
        验证函数是否可用
        :param: 需要带入的函数名
        :return: True/False
        """
        self.func = func
        current_app.logger.debug(
            "验证模块 {} 下的函数是否存在 {} 属性".format(self.module_name, self.func))
        if self.module is None:
            current_app.logger.warning("函数验证失败,没有验证模块")
            return False
        return hasattr(self.module, self.func)

    def getCallMethod(self):
        """
        返回可执行的函数
        :return:
        """
        current_app.logger.debug("获取可执行的函数")
        if hasattr(self.module, self.func):
            return getattr(self.module, self.func)
        return None

    def _load_module(self):
        """
        动态加载模块
        :return: True/False
        """
        ret = False
        # 列出模块下的所有目录   ls modules
        for file_name in os.listdir(self.modules_dir):
            # 遍历模块目录下的所有文件
            if file_name.endswith(".py"):
                # 如果文件名为.py结尾, 从文件名之中取出模块名
                module_name = file_name.rstrip(".py")
                if module_name != self.module_name:
                    # 当前遍历的这个py文件,不是我们想要导入的py
                    continue
                fp, pathname, desc = imp.find_module(
                    module_name, [self.modules_dir])
                if not fp:
                    continue
                try:
                    self.module = imp.load_module(
                        module_name, fp, pathname, desc)
                    ret = True
                    current_app.logger.debug(
                        "加载 {} 模块成功".format(self.module_name))
                except Exception as e:
                    current_app.logger.debug(
                        "加载 {} 模块失败".format(self.module_name))
                    
                finally:
                    fp.close()
                break
        return ret


class Response():

    def __init__(self):
        # 待返回的数据
        self.data = None
        # 执行过程中的错误码
        self.errorCode = 0
        # 错误信息
        self.errorMessage = None


class JsonRpc():

    def __init__(self):
        self.jsonData = None
        self.VERSION = "2.0"
        # 返回的结果
        self._response = {}

    def execute(self):
        current_app.logger.debug("进入API执行体")
        if self.jsonData.get("id", None) is None:
            self.jsonError(-1, 102, "id没有传")
            current_app.logger.error("请求的参数中没有id, 或者id为None")
            return self._response
        if self.validate():
            # 数据验证通过
            current_app.logger.debug("验证json格式成功")
            params = self.jsonData['params']
            auth = self.jsonData['auth']
            module, func = self.jsonData['method'].split(".")
            ret = self.callMethod(module, func, params, auth)
            #[{'status': 1L, 'name': u'YZ', 'user_phone': u'18888888888', 'idc_name': u'\u4ea6\u5e84\u673a\u623f', 'rel_cabinet_num': 50L, 'email': u'unixomg@163.com', 'phone': u'18519237136', 'user_interface': u'kevin', 'address': u'\u4ea6\u5e84\u7ecf\u6d4e\u5f00\u53d1\u533a', 'pact_cabinet_num': 60L, 'id': 1L}]
            #<app.base.Response instance at 0x7f63e03aa518>
            # print ret
            self.processResult(ret)
        return self._response

    def validate(self):
        """
        验证json数据格式
        :return:
        """
        if self.jsonData is None:
            self.jsonError(-1, 101, "没有指定json数据")
            current_app.logger.warning("没有传输json数据")
            return False
        # 验证是否有指定属性, 有五个属性: jsonrpc, method, id, auth, params
        for k in ["jsonrpc", "method", "auth", "params"]:
            if not self.jsonData.has_key(k):
                self.jsonError(self.jsonData["id"], 102, "{}没有传数据".format(k))
                current_app.logger.warning("请求的参数中, {} 没有传输".format(k))
                return False
        if self.jsonData.get("jsonrpc") != "2.0":
            self.jsonError(-1, 107,
                           "jsonrpc版本信息不对, 应该为{}".format(self.VERSION))
            current_app.logger.warning(
                "jsonrpc版本信息不对, 应该为{}".format(self.VERSION))
            return False

        action = self.jsonData.get("method")
        sp = action.split(".")
        if len(sp) != 2:
            self.jsonError(-1, 108, "method格式错误, 应该分隔为两个字符串")
            current_app.logger.warning("method格式错误, 应该分隔为两个字符串")
            return False
        if not sp[0] or not sp[1]:
            self.jsonError(-1, 108, "method格式错误, 方法或者函数不能为空")
            current_app.logger.warning("method格式错误, 方法或者函数不能为空")
            return False
        if not str(self.jsonData['id']).isdigit():
            self.jsonError(-1, 109, "id必须为数字")
            current_app.logger.warning("id必须为数字")
            return False

        if not isinstance(self.jsonData["params"], dict):
            self.jsonError(-1, 110, "params只能为字典")
            current_app.logger.warning("params只能为字典")
            return False

        # jsonrpc的值为2.0
        # method必须有".", 且使用点分隔的只有两个元素, 不能为空
        # id要是一个数字
        # auth 必须要有,可以为None
        # params必须为字典,字典可以为空
        return True

    def jsonError(self, id, errno, errmsg):
        """
        处理错误信息
        :param id:
        :param errno:
        :param errmsg:
        :return:
        """
        current_app.logger.debug("处理jsonError")
        self._response = {
            "jsonrpc": self.VERSION,
            "id": id,
            "error_code": errno,
            "error_message": errmsg,
        }

    def requireAuthentication(self, module, func):
        """
        不需要登陆也可以访问的白名单列表
        :param module:
        :param func:
        :return:True/False
        """
        # b_list = ["user.login", "api.info", "reboot.error","reboot.test", "idc.create"]
        #
        # if "{}.{}".format(module, func) in b_list:
        #     return False
        #
        # return True

        # test
        return False

    def callMethod(self, module, func, params, auth):
        """
        执行api调用
        :param module:
        :param func:
        :param params:
        :param auth:
        :return:
        """
        module_name = module.lower()
        func_name = func.lower()
        response = Response()
        at = AutoLoad()

        if not at.isValidModule(module_name):
            current_app.logger.warning("{} 模块导入失败".format(module))
            response.errorCode = 120
            response.errorMessage = "模块不存在"
            return response

        if not at.isValidMethod(func_name):
            current_app.logger.warning(
                "{} 模块下没有{} 这个方法".format(module_name, func_name))
            response.errorCode = 121
            response.errorMessage = "{} 模块下没有{} 这个方法".format(
                module_name, func_name)
            return response
        if self.requireAuthentication(module_name, func_name):
            # 需要登录/需要验证
            if auth is None:
                current_app.logger.warning(
                    "{}.{} 这个操作需要提供auth".format(module_name, func_name))
                response.errorCode = 122
                response.errorMessage = "这个操作需要提供auth"
                return response
        try:
            called = at.getCallMethod()
            if callable(called):
                response.data = called(**params)
                #print response.data
            else:
                current_app.logger.warning(
                    "{}下的{}方法不能被执行".format(module_name, func_name))
                response.errorCode = 123
                response.errorMessage = "{}下的{}方法不能被执行".format(
                    module_name, func_name)
        except Exception as e:
            current_app.logger.warning("{} 调用方法出错".format(func_name))
            response.errorCode = -1
            response.errorMessage = e.message
        return response

    def processResult(self, response):
        """
        处理返回结果
        :param response:
        :return:
        """
        current_app.logger.debug("处理执行后的结果")
        if response.errorCode != 0:
            self.jsonError(
                self.jsonData["id"], response.errorCode, response.errorMessage)
        else:
            self._response = {
                "jsonrpc": self.VERSION,
                "result": response.data,
                "id": self.jsonData["id"]
            }


if __name__ == "__main__":
    # at = AutoLoad()
    # print at.isValidModule("reboot")
    # print at.isValidMethod("test")
    # func = at.getCallMethod()
    # func()

    # print ret.decode("utf-8")
    data = {
        "id": 12,
        "method": "idc.get",
        "auth": "",
        "params": {"name": "kane"},
        "jsonrpc": "2.0"

    }
    jsondata = JsonRpc()
    jsondata.jsonData = data
    ret = jsondata.execute()
    # print json.dumps(ret, encoding="UTF-8", ensure_ascii=False)
