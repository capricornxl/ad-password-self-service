"""
Created by auto_sdk on 2019.10.18
"""
from api.base import RestApi


class OapiRoleVisibleSetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.role_id = None
        self.visible_role_ids = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.role.visible.set'
