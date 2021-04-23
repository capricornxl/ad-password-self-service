"""
Created by auto_sdk on 2021.01.15
"""
from api.base import RestApi


class OapiSmartworkHrmMasterdataSaveRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_data_fields = None
        self.outer_id = None
        self.scope_code = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartwork.hrm.masterdata.save'
