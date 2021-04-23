"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class OapiImpaasNewretailSendstaffmessageRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.content = None
        self.msg_type = None
        self.sender = None
        self.userid_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.impaas.newretail.sendstaffmessage'
