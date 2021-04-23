"""
Created by auto_sdk on 2021.03.10
"""
from api.base import RestApi


class OapiContactRolevisibilityUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.permissions = None
        self.role_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.contact.rolevisibility.update'
