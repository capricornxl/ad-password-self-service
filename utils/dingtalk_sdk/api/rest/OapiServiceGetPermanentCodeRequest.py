"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiServiceGetPermanentCodeRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.tmp_auth_code = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.service.get_permanent_code'
