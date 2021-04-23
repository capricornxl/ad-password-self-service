"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiSnsGetuserinfoRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.sns_token = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.sns.getuserinfo'
