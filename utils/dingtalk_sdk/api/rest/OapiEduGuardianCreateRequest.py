"""
Created by auto_sdk on 2021.04.15
"""
from api.base import RestApi


class OapiEduGuardianCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_id = None
        self.class_id = None
        self.mobile = None
        self.operator = None
        self.relation = None
        self.stu_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.guardian.create'
