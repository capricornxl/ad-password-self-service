"""
Created by auto_sdk on 2020.02.17
"""
from api.base import RestApi


class OapiServicegroupMessageSendRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.conversation_message = None
        self.order_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.servicegroup.message.send'
