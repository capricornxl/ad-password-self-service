"""
Created by auto_sdk on 2019.12.16
"""
from api.base import RestApi


class OapiMessageSendToConversationRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.action_card = None
        self.cid = None
        self.file = None
        self.image = None
        self.link = None
        self.markdown = None
        self.msg = None
        self.msgtype = None
        self.oa = None
        self.sender = None
        self.text = None
        self.voice = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.message.send_to_conversation'
