"""
Created by auto_sdk on 2020.03.04
"""
from api.base import RestApi


class OapiRhinoDeviceUniquecodeGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.unique_code = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.device.uniquecode.get'
