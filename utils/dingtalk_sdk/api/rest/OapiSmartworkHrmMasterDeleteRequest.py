"""
Created by auto_sdk on 2020.01.06
"""
from api.base import RestApi


class OapiSmartworkHrmMasterDeleteRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_data = None
        self.tenantid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.master.delete'
