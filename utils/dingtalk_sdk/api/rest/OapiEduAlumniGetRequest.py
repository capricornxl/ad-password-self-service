"""
Created by auto_sdk on 2020.05.11
"""
from api.base import RestApi


class OapiEduAlumniGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.alumni.get'
