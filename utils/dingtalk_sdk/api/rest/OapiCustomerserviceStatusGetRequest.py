"""
Created by auto_sdk on 2020.02.12
"""
from api.base import RestApi


class OapiCustomerserviceStatusGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.customerservice.status.get'
