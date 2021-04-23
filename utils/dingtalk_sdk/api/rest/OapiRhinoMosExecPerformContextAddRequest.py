"""
Created by auto_sdk on 2020.07.22
"""
from api.base import RestApi


class OapiRhinoMosExecPerformContextAddRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.context = None
        self.operation_record_ids = None
        self.order_id = None
        self.tenant_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.mos.exec.perform.context.add'
