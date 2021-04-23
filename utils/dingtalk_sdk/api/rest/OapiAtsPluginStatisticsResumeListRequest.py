"""
Created by auto_sdk on 2020.07.23
"""
from api.base import RestApi


class OapiAtsPluginStatisticsResumeListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_code = None
        self.cursor = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ats.plugin.statistics.resume.list'
