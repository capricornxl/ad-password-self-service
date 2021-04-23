"""
Created by auto_sdk on 2019.07.10
"""
from api.base import RestApi


class OapiProcessWorkrecordDeleteRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.request = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.process.workrecord.delete'
