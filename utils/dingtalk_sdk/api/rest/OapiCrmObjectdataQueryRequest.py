"""
Created by auto_sdk on 2021.03.11
"""
from api.base import RestApi


class OapiCrmObjectdataQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.current_operator_userid = None
        self.cursor = None
        self.name = None
        self.page_size = None
        self.query_dsl = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.crm.objectdata.query'
