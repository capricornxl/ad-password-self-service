"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class OapiHealthStepinfoListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.object_id = None
        self.stat_dates = None
        self.type = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.health.stepinfo.list'
