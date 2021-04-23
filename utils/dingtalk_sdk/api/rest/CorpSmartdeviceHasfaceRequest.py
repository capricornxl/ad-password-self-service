"""
Created by auto_sdk on 2019.12.17
"""
from api.base import RestApi


class CorpSmartdeviceHasfaceRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.smartdevice.hasface'
