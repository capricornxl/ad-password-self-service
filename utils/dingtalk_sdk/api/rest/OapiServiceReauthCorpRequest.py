"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiServiceReauthCorpRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.app_id = None
        self.corpid_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.service.reauth_corp'
