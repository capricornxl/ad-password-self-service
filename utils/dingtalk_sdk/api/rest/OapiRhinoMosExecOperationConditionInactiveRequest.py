"""
Created by auto_sdk on 2020.07.14
"""
from api.base import RestApi


class OapiRhinoMosExecOperationConditionInactiveRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.inactive_operation_req = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.mos.exec.operation.condition.inactive'
