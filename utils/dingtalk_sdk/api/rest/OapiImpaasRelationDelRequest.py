"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiImpaasRelationDelRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.request = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.impaas.relation.del'
