"""
Created by auto_sdk on 2020.11.25
"""
from api.base import RestApi


class OapiSmartdeviceBatcheventPostRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.device_event_vos = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.batchevent.post'
