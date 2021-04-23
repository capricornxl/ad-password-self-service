"""
Created by auto_sdk on 2020.11.20
"""
from api.base import RestApi


class OapiEduUseridGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.mobiles = None
        self.operator = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.userid.get'
