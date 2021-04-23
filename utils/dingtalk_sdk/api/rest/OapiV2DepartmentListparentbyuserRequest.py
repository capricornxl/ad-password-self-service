"""
Created by auto_sdk on 2020.10.10
"""
from api.base import RestApi


class OapiV2DepartmentListparentbyuserRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.v2.department.listparentbyuser'
