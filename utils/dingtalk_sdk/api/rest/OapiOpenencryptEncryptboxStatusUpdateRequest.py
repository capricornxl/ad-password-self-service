"""
Created by auto_sdk on 2020.05.07
"""
from api.base import RestApi


class OapiOpenencryptEncryptboxStatusUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.top_encrypt_box_status = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.openencrypt.encryptbox.status.update'
