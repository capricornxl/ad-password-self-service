"""
Created by auto_sdk on 2019.12.04
"""
from api.base import RestApi


class OapiSmartworkHrmMasterCheckRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_uk = None
        self.tenantid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.master.check'
