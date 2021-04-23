"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiCallBackGetCallBackRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.call_back.get_call_back'
