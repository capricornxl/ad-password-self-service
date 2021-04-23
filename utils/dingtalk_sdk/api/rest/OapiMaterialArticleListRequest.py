"""
Created by auto_sdk on 2019.06.28
"""
from api.base import RestApi


class OapiMaterialArticleListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.page_size = None
        self.page_start = None
        self.unionid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.material.article.list'
