"""
Created by auto_sdk on 2019.10.31
"""
from api.base import RestApi


class OapiMedalCorpmedalGrantRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.template_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.medal.corpmedal.grant'
