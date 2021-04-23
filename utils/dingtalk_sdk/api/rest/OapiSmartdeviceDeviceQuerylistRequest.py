"""
Created by auto_sdk on 2020.02.28
"""
from api.base import RestApi


class OapiSmartdeviceDeviceQuerylistRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.page_query_vo = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.device.querylist'
