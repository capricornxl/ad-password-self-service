"""
Created by auto_sdk on 2020.10.09
"""
from api.base import RestApi


class OapiCrmObjectdataContactDeleteRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.data_id = None
        self.operator_userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.crm.objectdata.contact.delete'
