"""
Created by auto_sdk on 2020.01.20
"""
from api.base import RestApi


class OapiPbpInstanceGroupMemberListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_id = None
        self.cursor = None
        self.punch_group_id = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.pbp.instance.group.member.list'
