"""
Created by auto_sdk on 2020.03.30
"""
from api.base import RestApi


class OapiImChatServicegroupMemberQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chat_id = None
        self.include_owner = None
        self.page_num = None
        self.page_size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.servicegroup.member.query'
