"""
Created by auto_sdk on 2019.08.14
"""
from api.base import RestApi


class CorpDeviceManageQuerylistRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.device_service_id = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.device.manage.querylist'
