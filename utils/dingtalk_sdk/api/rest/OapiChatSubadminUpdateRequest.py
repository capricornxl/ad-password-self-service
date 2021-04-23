"""
Created by auto_sdk on 2020.02.27
"""
from api.base import RestApi


class OapiChatSubadminUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chatid = None
        self.role = None
        self.userids = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.chat.subadmin.update'
