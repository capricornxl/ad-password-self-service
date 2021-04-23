"""
Created by auto_sdk on 2020.04.09
"""
from api.base import RestApi


class OapiRhinoMosLayoutOperationdefSaveflowRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.active = None
        self.flow_version = None
        self.operation_defs = None
        self.order_id = None
        self.source = None
        self.tenant_id = None
        self.tmp_save = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.mos.layout.operationdef.saveflow'
