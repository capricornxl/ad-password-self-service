"""
Created by auto_sdk on 2019.08.13
"""
from api.base import RestApi


class OapiSmartdeviceDevicememberSyncRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.add_userids = None
        self.del_userids = None
        self.device_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.devicemember.sync'
