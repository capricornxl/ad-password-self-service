"""
Created by auto_sdk on 2020.03.07
"""
from api.base import RestApi


class OapiRhinoMosLayoutOperationdefActiveflowRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.flow_version = None
        self.order_id = None
        self.tenant_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.mos.layout.operationdef.activeflow'
