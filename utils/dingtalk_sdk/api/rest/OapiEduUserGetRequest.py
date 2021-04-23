"""
Created by auto_sdk on 2020.11.19
"""
from api.base import RestApi


class OapiEduUserGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.class_id = None
        self.role = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.user.get'
