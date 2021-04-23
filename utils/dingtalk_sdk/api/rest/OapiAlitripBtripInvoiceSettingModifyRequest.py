"""
Created by auto_sdk on 2020.11.30
"""
from api.base import RestApi


class OapiAlitripBtripInvoiceSettingModifyRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.request = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.alitrip.btrip.invoice.setting.modify'
