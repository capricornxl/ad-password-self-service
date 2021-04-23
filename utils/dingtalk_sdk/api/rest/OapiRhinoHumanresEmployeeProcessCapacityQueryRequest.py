"""
Created by auto_sdk on 2020.03.06
"""
from api.base import RestApi


class OapiRhinoHumanresEmployeeProcessCapacityQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.category = None
        self.process_structural_cluster_id_list = None
        self.tenant_id = None
        self.userid = None
        self.work_nos = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.humanres.employee.process.capacity.query'
