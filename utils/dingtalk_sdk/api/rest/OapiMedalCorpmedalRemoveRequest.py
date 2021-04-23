"""
Created by auto_sdk on 2019.11.19
"""
from api.base import RestApi


class OapiMedalCorpmedalRemoveRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.template_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.medal.corpmedal.remove'
