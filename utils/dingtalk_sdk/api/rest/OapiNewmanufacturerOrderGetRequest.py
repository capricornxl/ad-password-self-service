"""
Created by auto_sdk on 2020.02.17
"""
from api.base import RestApi


class OapiNewmanufacturerOrderGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.number = None
        self.tenant_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.newmanufacturer.order.get'
