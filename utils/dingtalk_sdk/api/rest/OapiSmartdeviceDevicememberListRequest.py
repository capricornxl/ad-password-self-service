"""
Created by auto_sdk on 2019.08.08
"""
from api.base import RestApi


class OapiSmartdeviceDevicememberListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.device_id = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.devicemember.list'
