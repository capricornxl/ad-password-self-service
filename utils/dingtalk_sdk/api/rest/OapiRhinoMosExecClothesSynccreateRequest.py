"""
Created by auto_sdk on 2020.03.23
"""
from api.base import RestApi


class OapiRhinoMosExecClothesSynccreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.additional_operations = None
        self.auto_start = None
        self.biz_type = None
        self.clothes = None
        self.entity_type = None
        self.order_id = None
        self.source = None
        self.tenant_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.mos.exec.clothes.synccreate'
