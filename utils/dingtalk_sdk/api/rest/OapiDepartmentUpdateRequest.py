"""
Created by auto_sdk on 2020.05.18
"""
from api.base import RestApi


class OapiDepartmentUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.autoAddUser = None
        self.createDeptGroup = None
        self.deptHiding = None
        self.deptManagerUseridList = None
        self.deptPerimits = None
        self.deptPermits = None
        self.groupContainHiddenDept = None
        self.groupContainOuterDept = None
        self.groupContainSubDept = None
        self.id = None
        self.lang = None
        self.name = None
        self.order = None
        self.orgDeptOwner = None
        self.outerDept = None
        self.outerDeptOnlySelf = None
        self.outerPermitDepts = None
        self.outerPermitUsers = None
        self.parentid = None
        self.sourceIdentifier = None
        self.userPerimits = None
        self.userPermits = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.department.update'
