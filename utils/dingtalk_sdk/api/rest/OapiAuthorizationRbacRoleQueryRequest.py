"""
Created by auto_sdk on 2021.02.01
"""
from api.base import RestApi


class OapiAuthorizationRbacRoleQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.open_role_ids = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.authorization.rbac.role.query'
