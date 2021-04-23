"""
Created by auto_sdk on 2020.01.19
"""
from api.base import RestApi


class OapiPbpInstanceEnableRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_id = None
        self.biz_inst_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.pbp.instance.enable'
