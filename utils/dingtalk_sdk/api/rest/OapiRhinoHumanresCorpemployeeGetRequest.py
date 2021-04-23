"""
Created by auto_sdk on 2020.03.06
"""
from api.base import RestApi


class OapiRhinoHumanresCorpemployeeGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.query_corp_employee_param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.humanres.corpemployee.get'
