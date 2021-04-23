"""
Created by auto_sdk on 2020.06.17
"""
from api.base import RestApi


class OapiChatSendRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.action_card = None
        self.chatid = None
        self.file = None
        self.image = None
        self.link = None
        self.markdown = None
        self.msg = None
        self.msgtype = None
        self.oa = None
        self.text = None
        self.voice = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.chat.send'
