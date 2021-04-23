"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiCallBackUpdateCallBackRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.aes_key = None
        self.call_back_tag = None
        self.token = None
        self.url = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.call_back.update_call_back'
