"""
Created by auto_sdk on 2021.04.13
"""
from api.base import RestApi


class OapiProcessinstanceVariableUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.process_instance_id = None
        self.remark = None
        self.variables = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.processinstance.variable.update'
