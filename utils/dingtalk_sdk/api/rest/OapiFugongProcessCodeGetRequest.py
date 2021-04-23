"""
Created by auto_sdk on 2020.02.17
"""
from api.base import RestApi


class OapiFugongProcessCodeGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.fugong.process_code.get'
