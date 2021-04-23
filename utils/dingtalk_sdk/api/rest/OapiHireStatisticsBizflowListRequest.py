"""
Created by auto_sdk on 2020.08.21
"""
from api.base import RestApi


class OapiHireStatisticsBizflowListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.hire.statistics.bizflow.list'
