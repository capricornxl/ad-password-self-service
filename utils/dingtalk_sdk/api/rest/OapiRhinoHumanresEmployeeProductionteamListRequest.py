"""
Created by auto_sdk on 2020.11.13
"""
from api.base import RestApi


class OapiRhinoHumanresEmployeeProductionteamListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.query_employee_production_team_param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.humanres.employee.productionteam.list'
