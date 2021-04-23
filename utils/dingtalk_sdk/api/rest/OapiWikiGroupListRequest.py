"""
Created by auto_sdk on 2020.10.16
"""
from api.base import RestApi


class OapiWikiGroupListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.auth_code = None
        self.cursor = None
        self.group_type = None
        self.role_type = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.wiki.group.list'
