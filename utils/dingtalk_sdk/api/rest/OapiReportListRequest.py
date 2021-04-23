"""
Created by auto_sdk on 2020.08.24
"""
from api.base import RestApi


class OapiReportListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.end_time = None
        self.modified_end_time = None
        self.modified_start_time = None
        self.size = None
        self.start_time = None
        self.template_name = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.report.list'
