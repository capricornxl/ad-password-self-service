"""
Created by auto_sdk on 2019.07.04
"""
from api.base import RestApi


class OapiMaterialNewsGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.media_id = None
        self.unionid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.material.news.get'
