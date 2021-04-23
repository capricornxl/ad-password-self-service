"""
Created by auto_sdk on 2020.07.03
"""
from api.base import RestApi


class OapiRhinoMosExecPerformConditionalStartRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.device_ids = None
        self.entity_condition = None
        self.operation_uids = None
        self.order_id = None
        self.tenant_id = None
        self.userid = None
        self.work_nos = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.mos.exec.perform.conditional.start'
