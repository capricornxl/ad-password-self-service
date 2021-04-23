"""
Created by auto_sdk on 2019.07.04
"""
from api.base import RestApi


class OapiMaterialNewsListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.page_size = None
        self.page_start = None
        self.unionid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.material.news.list'
