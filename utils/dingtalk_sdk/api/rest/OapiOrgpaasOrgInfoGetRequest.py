"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiOrgpaasOrgInfoGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.orgpaas.org.info.get'
