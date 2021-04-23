"""
Created by auto_sdk on 2019.10.09
"""
from api.base import RestApi


class OapiOrgOpenencryptRegistekmsRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.top_kms_meta = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.org.openencrypt.registekms'
