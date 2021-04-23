"""
Created by auto_sdk on 2019.12.25
"""
from api.base import RestApi


class OapiSmartdeviceEventPostRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.device_event_vo = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.event.post'
