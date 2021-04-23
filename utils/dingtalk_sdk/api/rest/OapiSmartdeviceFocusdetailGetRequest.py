"""
Created by auto_sdk on 2019.10.24
"""
from api.base import RestApi


class OapiSmartdeviceFocusdetailGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.focusdetail.get'
