"""
Created by auto_sdk on 2020.09.24
"""
from api.base import RestApi


class OapiCrmOrgVirtualcorpidGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.crm.org.virtualcorpid.get'
