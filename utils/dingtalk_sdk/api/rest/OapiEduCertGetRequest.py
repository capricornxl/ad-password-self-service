"""
Created by auto_sdk on 2020.12.24
"""
from api.base import RestApi


class OapiEduCertGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.cert.get'
