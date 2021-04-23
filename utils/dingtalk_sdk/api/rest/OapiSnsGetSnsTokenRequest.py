"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiSnsGetSnsTokenRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.openid = None
        self.persistent_code = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.sns.get_sns_token'
