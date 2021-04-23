"""
Created by auto_sdk on 2020.09.13
"""
from api.base import RestApi


class OapiUserListadminRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.user.listadmin'
