"""
Created by auto_sdk on 2020.04.23
"""
from api.base import RestApi


class OapiRhinoMosLayoutOperationdefsListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.flow_version = None
        self.need_assignInfo = None
        self.operation_uids = None
        self.order_id = None
        self.tenant_id = None
        self.tmp_save = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.mos.layout.operationdefs.list'
