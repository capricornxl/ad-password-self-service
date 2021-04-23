"""
Created by auto_sdk on 2020.11.05
"""
from api.base import RestApi


class OapiEduUserAuthGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.language = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.user.auth.get'
