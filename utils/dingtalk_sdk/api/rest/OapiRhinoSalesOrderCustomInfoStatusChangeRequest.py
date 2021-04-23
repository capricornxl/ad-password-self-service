"""
Created by auto_sdk on 2020.08.04
"""
from api.base import RestApi


class OapiRhinoSalesOrderCustomInfoStatusChangeRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.sales_order_custom_info_change_req = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.sales.order.custom.info.status.change'
