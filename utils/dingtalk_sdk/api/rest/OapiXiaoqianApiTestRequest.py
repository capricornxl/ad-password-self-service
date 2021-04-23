"""
Created by auto_sdk on 2021.04.21
"""
from api.base import RestApi


class OapiXiaoqianApiTestRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.id = None
        self.list1 = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.xiaoqian.api.test'
