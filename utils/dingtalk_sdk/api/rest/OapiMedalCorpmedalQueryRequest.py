"""
Created by auto_sdk on 2020.12.27
"""
from api.base import RestApi


class OapiMedalCorpmedalQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.medal.corpmedal.query'
