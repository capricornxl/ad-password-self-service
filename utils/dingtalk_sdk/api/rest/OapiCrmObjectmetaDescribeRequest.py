"""
Created by auto_sdk on 2020.06.04
"""
from api.base import RestApi


class OapiCrmObjectmetaDescribeRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.name = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.crm.objectmeta.describe'
