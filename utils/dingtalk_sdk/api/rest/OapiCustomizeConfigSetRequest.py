"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiCustomizeConfigSetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.active_id = None
        self.active_type = None
        self.biz = None
        self.rule_name = None
        self.type = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.customize.config.set'
