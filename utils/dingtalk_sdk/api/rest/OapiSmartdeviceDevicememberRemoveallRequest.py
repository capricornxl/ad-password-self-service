"""
Created by auto_sdk on 2019.08.08
"""
from api.base import RestApi


class OapiSmartdeviceDevicememberRemoveallRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.device_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.devicemember.removeall'
