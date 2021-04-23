"""
Created by auto_sdk on 2019.07.09
"""
from api.base import RestApi


class OapiEduPeriodListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.campus_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.period.list'
