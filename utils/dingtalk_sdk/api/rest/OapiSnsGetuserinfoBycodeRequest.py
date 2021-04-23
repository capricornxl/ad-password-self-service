"""
Created by auto_sdk on 2019.05.10
"""
from api.base import RestApi


class OapiSnsGetuserinfoBycodeRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.tmp_auth_code = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.sns.getuserinfo_bycode'
