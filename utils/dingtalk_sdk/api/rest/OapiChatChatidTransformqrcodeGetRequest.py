"""
Created by auto_sdk on 2020.10.12
"""
from api.base import RestApi


class OapiChatChatidTransformqrcodeGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.group_url = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.chat.chatid.transformqrcode.get'
