"""
Created by auto_sdk on 2020.09.21
"""
from api.base import RestApi


class OapiSmartworkHrmEmployeeAttachmentUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agentid = None
        self.param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.employee.attachment.update'
