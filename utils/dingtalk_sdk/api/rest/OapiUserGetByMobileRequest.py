"""
Created by auto_sdk on 2019.10.11
"""
from api.base import RestApi


class OapiUserGetByMobileRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.mobile = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.user.get_by_mobile'
