"""
Created by auto_sdk on 2020.01.03
"""
from api.base import RestApi


class OapiCrmAuthGroupListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.crm.auth.group.list'
