"""
Created by auto_sdk on 2020.07.03
"""
from api.base import RestApi


class OapiRhinoMosExecPerformQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.active_condition = None
        self.entity_ids = None
        self.entity_type = None
        self.operation_uids = None
        self.order_id = None
        self.perform_status_list = None
        self.tenant_id = None
        self.userid = None
        self.workstation_codes = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.mos.exec.perform.query'
