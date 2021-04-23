"""
Created by auto_sdk on 2020.08.05
"""
from api.base import RestApi


class OapiAiMtTranslateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.query = None
        self.source_language = None
        self.target_language = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ai.mt.translate'
