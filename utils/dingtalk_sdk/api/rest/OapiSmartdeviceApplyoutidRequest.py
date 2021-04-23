"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiSmartdeviceApplyoutidRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.dev_serv_id = None
        self.sn = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.applyoutid'
