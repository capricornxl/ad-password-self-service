"""
Created by auto_sdk on 2020.10.10
"""
from api.base import RestApi


class OapiDepartmentCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.createDeptGroup = None
        self.deptHiding = None
        self.deptPerimits = None
        self.deptPermits = None
        self.id = None
        self.name = None
        self.order = None
        self.outerDept = None
        self.outerDeptOnlySelf = None
        self.outerPermitDepts = None
        self.outerPermitUsers = None
        self.parentBalanceFirst = None
        self.parentid = None
        self.shareBalance = None
        self.sourceIdentifier = None
        self.userPerimits = None
        self.userPermits = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.department.create'
