"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class CorpHealthStepinfoGetuserstatusRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.health.stepinfo.getuserstatus'
