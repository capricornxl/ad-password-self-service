"""
Created by auto_sdk on 2019.07.04
"""
from api.base import RestApi


class OapiMaterialNewsAddRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.articles = None
        self.unionid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.material.news.add'
