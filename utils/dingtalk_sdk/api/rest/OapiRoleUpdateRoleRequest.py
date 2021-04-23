"""
Created by auto_sdk on 2018.07.02
"""
from api.base import RestApi


class OapiRoleUpdateRoleRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.roleId = None
        self.roleName = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.role.update_role'
