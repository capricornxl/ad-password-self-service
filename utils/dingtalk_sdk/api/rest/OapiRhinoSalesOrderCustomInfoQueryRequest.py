"""
Created by auto_sdk on 2020.08.04
"""
from api.base import RestApi


class OapiRhinoSalesOrderCustomInfoQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.req = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.sales.order.custom.info.query'
