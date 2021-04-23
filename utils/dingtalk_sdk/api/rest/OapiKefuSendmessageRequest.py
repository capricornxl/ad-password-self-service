"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiKefuSendmessageRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.content = None
        self.customerid = None
        self.msgtype = None
        self.serviceid = None
        self.token = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.kefu.sendmessage'
