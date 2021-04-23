"""
Created by auto_sdk on 2019.11.13
"""
from api.base import RestApi


class OapiRoleScopeUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.dept_ids = None
        self.role_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.role.scope.update'
