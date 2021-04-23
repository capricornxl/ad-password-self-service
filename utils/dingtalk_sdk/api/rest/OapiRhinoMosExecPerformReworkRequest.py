"""
Created by auto_sdk on 2020.07.03
"""
from api.base import RestApi


class OapiRhinoMosExecPerformReworkRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.context = None
        self.order_id = None
        self.rework_start_id = None
        self.tenant_id = None
        self.to_inactive_ids = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.mos.exec.perform.rework'
