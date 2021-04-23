"""
Created by auto_sdk on 2021.01.11
"""
from api.base import RestApi


class OapiHireGuideBeginnertaskFinishRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.task_code = None
        self.task_type = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.hire.guide.beginnertask.finish'
