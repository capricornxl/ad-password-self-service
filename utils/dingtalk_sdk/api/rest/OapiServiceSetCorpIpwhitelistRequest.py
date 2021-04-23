"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiServiceSetCorpIpwhitelistRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.auth_corpid = None
        self.ip_whitelist = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.service.set_corp_ipwhitelist'
