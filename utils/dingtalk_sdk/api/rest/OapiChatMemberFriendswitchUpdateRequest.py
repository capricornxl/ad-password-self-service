"""
Created by auto_sdk on 2020.07.15
"""
from api.base import RestApi


class OapiChatMemberFriendswitchUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chatid = None
        self.is_prohibit = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.chat.member.friendswitch.update'
