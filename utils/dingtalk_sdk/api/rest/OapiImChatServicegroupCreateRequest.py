"""
Created by auto_sdk on 2019.08.22
"""
from api.base import RestApi


class OapiImChatServicegroupCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.group_uniq_id = None
        self.org_inner_group = None
        self.owner_userid = None
        self.title = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.servicegroup.create'
