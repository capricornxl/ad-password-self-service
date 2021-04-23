"""
Created by auto_sdk on 2020.05.29
"""
from api.base import RestApi


class OapiImChatControlgroupCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.authority_type = None
        self.group_type = None
        self.group_uniq_id = None
        self.member_userids = None
        self.owner_userid = None
        self.title = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.controlgroup.create'
