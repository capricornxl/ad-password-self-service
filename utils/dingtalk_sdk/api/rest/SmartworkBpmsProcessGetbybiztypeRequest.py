"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class SmartworkBpmsProcessGetbybiztypeRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_type = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.smartwork.bpms.process.getbybiztype'
