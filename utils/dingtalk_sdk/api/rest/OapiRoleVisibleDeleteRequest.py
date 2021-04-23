"""
Created by auto_sdk on 2019.09.16
"""
from api.base import RestApi


class OapiRoleVisibleDeleteRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.role_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.role.visible.delete'
