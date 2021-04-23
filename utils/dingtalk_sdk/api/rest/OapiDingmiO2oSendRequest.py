"""
Created by auto_sdk on 2020.09.27
"""
from api.base import RestApi


class OapiDingmiO2oSendRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.msg_key = None
        self.msg_param = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.dingmi.o2o.send'
