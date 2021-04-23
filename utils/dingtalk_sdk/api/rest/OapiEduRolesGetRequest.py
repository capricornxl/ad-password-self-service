"""
Created by auto_sdk on 2021.04.12
"""
from api.base import RestApi


class OapiEduRolesGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.roles.get'
