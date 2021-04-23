"""
Created by auto_sdk on 2020.02.26
"""
from api.base import RestApi


class OapiSmartdeviceQrQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.qr_content = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.qr.query'
