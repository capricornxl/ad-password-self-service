"""
Created by auto_sdk on 2021.01.22
"""
from api.base import RestApi


class OapiImChatServicegroupDisbandRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chat_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.servicegroup.disband'
