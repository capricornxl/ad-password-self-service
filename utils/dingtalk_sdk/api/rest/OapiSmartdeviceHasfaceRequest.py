"""
Created by auto_sdk on 2020.05.28
"""
from api.base import RestApi


class OapiSmartdeviceHasfaceRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.hasface'
