"""
Created by auto_sdk on 2021.03.18
"""
from api.base import RestApi


class OapiUserGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.user.get'
