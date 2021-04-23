"""
Created by auto_sdk on 2021.01.20
"""
from api.base import RestApi


class OapiAuthorizationRbacRoleMemberRemoveRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.open_role_id = None
        self.remove_members = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.authorization.rbac.role.member.remove'
