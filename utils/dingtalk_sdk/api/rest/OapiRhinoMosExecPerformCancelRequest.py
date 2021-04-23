"""
Created by auto_sdk on 2020.07.03
"""
from api.base import RestApi


class OapiRhinoMosExecPerformCancelRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.context = None
        self.operation_perform_record_ids = None
        self.order_id = None
        self.stop_schedule = None
        self.tenant_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.mos.exec.perform.cancel'
