"""
Created by auto_sdk on 2020.03.19
"""
from api.base import RestApi


class OapiPlanetomFeedsTaskinfoRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.task_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.planetom.feeds.taskinfo'
