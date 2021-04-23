"""
Created by auto_sdk on 2019.09.04
"""
from api.base import RestApi


class OapiSmartdeviceFaceFeatureRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.model_type = None
        self.model_version = None
        self.userid_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.face.feature'
