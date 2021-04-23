"""
Created by auto_sdk on 2020.02.07
"""
from api.base import RestApi


class OapiSmartdeviceDeviceUnbindRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.device_unbind_vo = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.device.unbind'
