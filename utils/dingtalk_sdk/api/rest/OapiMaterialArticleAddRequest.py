"""
Created by auto_sdk on 2019.12.24
"""
from api.base import RestApi


class OapiMaterialArticleAddRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.article = None
        self.unionid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.material.article.add'
