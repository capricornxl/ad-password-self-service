"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiRoleRemoverolesforempsRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.roleIds = None
        self.userIds = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.role.removerolesforemps'
