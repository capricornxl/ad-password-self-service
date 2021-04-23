"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiChatUpdategroupnickRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chatid = None
        self.group_nick = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.chat.updategroupnick'
