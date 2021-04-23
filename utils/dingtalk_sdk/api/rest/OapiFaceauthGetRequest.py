"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiFaceauthGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.app_biz_id = None
        self.tmp_auth_code = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.faceauth.get'
