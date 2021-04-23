"""
Created by auto_sdk on 2019.09.03
"""
from api.base import RestApi


class CorpSmartdeviceGetfaceRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.smartdevice.getface'
