"""
Created by auto_sdk on 2020.11.23
"""
from api.base import RestApi


class OapiProcessinstanceGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.process_instance_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.processinstance.get'
