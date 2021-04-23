"""
Created by auto_sdk on 2020.01.03
"""
from api.base import RestApi


class OapiCrmAuthGroupPermissionListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.role_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.crm.auth.group.permission.list'
