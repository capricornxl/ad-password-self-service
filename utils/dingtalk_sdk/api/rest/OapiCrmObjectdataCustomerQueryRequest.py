"""
Created by auto_sdk on 2020.09.27
"""
from api.base import RestApi


class OapiCrmObjectdataCustomerQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.current_operator_userid = None
        self.cursor = None
        self.page_size = None
        self.query_dsl = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.crm.objectdata.customer.query'
