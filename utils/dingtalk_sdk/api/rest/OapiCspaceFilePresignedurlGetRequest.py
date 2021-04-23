"""
Created by auto_sdk on 2020.11.18
"""
from api.base import RestApi


class OapiCspaceFilePresignedurlGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.dentryid = None
        self.expire_seconds = None
        self.inner_invoke = None
        self.spaceid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.cspace.file.presignedurl.get'
