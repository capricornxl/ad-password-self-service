"""
Created by auto_sdk on 2020.09.16
"""
from api.base import RestApi


class OapiReportTemplateGetbynameRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.template_name = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.report.template.getbyname'
