"""
Created by auto_sdk on 2020.09.08
"""
from api.base import RestApi


class OapiDingtalkImpaasMessageCrossdomainReadRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.message_read_model = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.dingtalk.impaas.message.crossdomain.read'
