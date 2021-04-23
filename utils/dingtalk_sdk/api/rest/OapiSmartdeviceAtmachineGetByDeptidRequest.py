"""
Created by auto_sdk on 2020.07.01
"""
from api.base import RestApi


class OapiSmartdeviceAtmachineGetByDeptidRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.atmachine.get_by_deptid'
