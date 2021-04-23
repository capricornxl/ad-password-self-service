"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class OapiImpaasConversationSendmessageRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chatid = None
        self.content = None
        self.type = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.impaas.conversation.sendmessage'
