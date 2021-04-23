"""
Created by auto_sdk on 2020.02.17
"""
from api.base import RestApi


class OapiRhinoOpenserviceQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.code = None
        self.gmt_create = None
        self.id = None
        self.tenent_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.openservice.query'
