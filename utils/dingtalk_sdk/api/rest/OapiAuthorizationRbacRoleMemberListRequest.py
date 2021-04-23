"""
Created by auto_sdk on 2021.01.21
"""
from api.base import RestApi


class OapiAuthorizationRbacRoleMemberListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.cursor = None
        self.open_role_id = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.authorization.rbac.role.member.list'
