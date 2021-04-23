"""
Created by auto_sdk on 2020.10.14
"""
from api.base import RestApi


class OapiXiaoxuanTestRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.normal_data = None
        self.system_data = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.xiaoxuan.test'
