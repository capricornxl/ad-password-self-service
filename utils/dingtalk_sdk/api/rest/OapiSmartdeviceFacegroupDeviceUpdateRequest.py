"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiSmartdeviceFacegroupDeviceUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.add_device_ids = None
        self.biz_id = None
        self.del_device_ids = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.facegroup.device.update'
