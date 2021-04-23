"""
Created by auto_sdk on 2020.12.29
"""
from api.base import RestApi


class OapiContactRolevisibilityGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.role_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.contact.rolevisibility.get'
