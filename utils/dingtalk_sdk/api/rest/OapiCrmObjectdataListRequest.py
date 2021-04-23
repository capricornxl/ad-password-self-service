"""
Created by auto_sdk on 2021.01.28
"""
from api.base import RestApi


class OapiCrmObjectdataListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.current_operator_userid = None
        self.data_id_list = None
        self.name = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.crm.objectdata.list'
