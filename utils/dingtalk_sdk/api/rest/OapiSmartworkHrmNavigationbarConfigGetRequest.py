"""
Created by auto_sdk on 2021.01.19
"""
from api.base import RestApi


class OapiSmartworkHrmNavigationbarConfigGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.change_param = None
        self.type = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.navigationbar.config.get'
