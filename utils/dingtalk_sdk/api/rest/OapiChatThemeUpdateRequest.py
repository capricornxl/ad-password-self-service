"""
Created by auto_sdk on 2019.10.31
"""
from api.base import RestApi


class OapiChatThemeUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chatid = None
        self.mediaid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.chat.theme.update'
