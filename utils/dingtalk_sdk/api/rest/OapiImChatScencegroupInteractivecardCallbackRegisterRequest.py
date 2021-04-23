"""
Created by auto_sdk on 2020.12.23
"""
from api.base import RestApi


class OapiImChatScencegroupInteractivecardCallbackRegisterRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.api_secret = None
        self.callback_url = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.scencegroup.interactivecard.callback.register'
