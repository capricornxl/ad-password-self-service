"""
Created by auto_sdk on 2020.05.19
"""
from api.base import RestApi


class OapiSmartdeviceDeviceQuerybyidRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.device_query_vo = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.device.querybyid'
