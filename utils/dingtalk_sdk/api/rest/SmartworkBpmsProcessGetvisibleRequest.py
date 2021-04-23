"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class SmartworkBpmsProcessGetvisibleRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.process_code_list = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.smartwork.bpms.process.getvisible'
