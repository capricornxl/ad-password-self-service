"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiSmartdeviceFacegroupRemoveallRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.facegroup.removeall'
