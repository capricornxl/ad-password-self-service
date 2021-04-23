"""
Created by auto_sdk on 2020.03.06
"""
from api.base import RestApi


class OapiRhinoHumanresEmployeeProcessBestdeviceQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.available_device_models = None
        self.employee_process_capacity_units = None
        self.tenant_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.humanres.employee.process.bestdevice.query'
