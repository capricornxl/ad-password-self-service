"""
Created by auto_sdk on 2020.08.17
"""
from api.base import RestApi


class OapiSmartworkHrmMasterCorpconfigUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.scope_code = None
        self.status = None
        self.tenant_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.master.corpconfig.update'
