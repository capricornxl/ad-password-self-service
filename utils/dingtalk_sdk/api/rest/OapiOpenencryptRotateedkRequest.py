"""
Created by auto_sdk on 2019.10.09
"""
from api.base import RestApi


class OapiOpenencryptRotateedkRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.top_edk_rotate_manual = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.openencrypt.rotateedk'
