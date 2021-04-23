"""
Created by auto_sdk on 2020.06.04
"""
from api.base import RestApi


class OapiCrmObjectmetaContactDescribeRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.crm.objectmeta.contact.describe'
