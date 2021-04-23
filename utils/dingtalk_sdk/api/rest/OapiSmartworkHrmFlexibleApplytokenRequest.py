"""
Created by auto_sdk on 2020.08.11
"""
from api.base import RestApi


class OapiSmartworkHrmFlexibleApplytokenRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agentid = None
        self.opt_user_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.flexible.applytoken'
