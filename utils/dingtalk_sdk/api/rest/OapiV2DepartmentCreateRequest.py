"""
Created by auto_sdk on 2020.10.19
"""
from api.base import RestApi


class OapiV2DepartmentCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.create_dept_group = None
        self.dept_permits = None
        self.extension = None
        self.hide_dept = None
        self.name = None
        self.order = None
        self.outer_dept = None
        self.outer_dept_only_self = None
        self.outer_permit_depts = None
        self.outer_permit_users = None
        self.parent_id = None
        self.source_identifier = None
        self.user_permits = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.v2.department.create'
