"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiImChatServicegroupMemberUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.action = None
        self.chat_id = None
        self.member_dingtalk_ids = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.servicegroup.member.update'
