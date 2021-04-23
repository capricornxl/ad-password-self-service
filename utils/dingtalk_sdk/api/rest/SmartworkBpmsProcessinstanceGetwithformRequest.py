"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class SmartworkBpmsProcessinstanceGetwithformRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.process_instance_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.smartwork.bpms.processinstance.getwithform'
