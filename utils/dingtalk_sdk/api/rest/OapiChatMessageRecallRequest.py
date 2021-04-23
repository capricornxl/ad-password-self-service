"""
Created by auto_sdk on 2020.03.02
"""
from api.base import RestApi


class OapiChatMessageRecallRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chatid = None
        self.msgid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.chat.message.recall'
