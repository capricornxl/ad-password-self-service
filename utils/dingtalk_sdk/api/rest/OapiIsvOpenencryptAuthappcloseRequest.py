"""
Created by auto_sdk on 2019.12.23
"""
from api.base import RestApi


class OapiIsvOpenencryptAuthappcloseRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.top_auth_micro_app_close = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.isv.openencrypt.authappclose'
