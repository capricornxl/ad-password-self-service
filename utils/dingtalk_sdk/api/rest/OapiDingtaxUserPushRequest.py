"""
Created by auto_sdk on 2021.01.18
"""
from api.base import RestApi


class OapiDingtaxUserPushRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.source_region = None
        self.user_info_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.dingtax.user.push'
