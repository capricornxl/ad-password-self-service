"""
Created by auto_sdk on 2019.12.23
"""
from api.base import RestApi


class OapiPbpInstanceCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.active = None
        self.biz_id = None
        self.end_time = None
        self.outer_id = None
        self.start_time = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.pbp.instance.create'
