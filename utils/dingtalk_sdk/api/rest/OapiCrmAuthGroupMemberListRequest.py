"""
Created by auto_sdk on 2020.01.16
"""
from api.base import RestApi


class OapiCrmAuthGroupMemberListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.role_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.crm.auth.group.member.list'
