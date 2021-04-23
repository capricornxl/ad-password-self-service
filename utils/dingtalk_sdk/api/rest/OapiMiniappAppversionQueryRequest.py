"""
Created by auto_sdk on 2020.07.28
"""
from api.base import RestApi


class OapiMiniappAppversionQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.model_key = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.miniapp.appversion.query'
