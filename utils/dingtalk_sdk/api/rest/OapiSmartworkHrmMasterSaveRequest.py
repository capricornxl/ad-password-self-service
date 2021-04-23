"""
Created by auto_sdk on 2021.03.25
"""
from api.base import RestApi


class OapiSmartworkHrmMasterSaveRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_data = None
        self.tenant_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.master.save'
