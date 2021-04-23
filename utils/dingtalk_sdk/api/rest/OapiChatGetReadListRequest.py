"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiChatGetReadListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.messageId = None
        self.size = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.chat.getReadList'
