"""
Created by auto_sdk on 2020.05.09
"""
from api.base import RestApi


class OapiPbpInstanceGroupPositionUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.sync_param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.pbp.instance.group.position.update'
