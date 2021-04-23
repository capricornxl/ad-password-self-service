"""
Created by auto_sdk on 2019.12.21
"""
from api.base import RestApi


class OapiPbpInstanceGroupCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.group_param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.pbp.instance.group.create'
