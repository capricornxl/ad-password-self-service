"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiGetJsapiTicketRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.get_jsapi_ticket'
