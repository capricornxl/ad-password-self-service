"""
Created by auto_sdk on 2019.07.17
"""
from api.base import RestApi


class OapiImChatServicegroupUpgradeRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chat_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.servicegroup.upgrade'
