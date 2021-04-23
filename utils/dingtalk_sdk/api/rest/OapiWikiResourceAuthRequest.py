"""
Created by auto_sdk on 2020.10.28
"""
from api.base import RestApi


class OapiWikiResourceAuthRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agentid = None
        self.auth_code = None
        self.is_public = None
        self.resource_list = None
        self.resource_type = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.wiki.resource.auth'
