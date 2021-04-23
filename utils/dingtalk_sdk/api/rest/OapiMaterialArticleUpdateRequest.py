"""
Created by auto_sdk on 2019.06.28
"""
from api.base import RestApi


class OapiMaterialArticleUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.article = None
        self.unionid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.material.article.update'
