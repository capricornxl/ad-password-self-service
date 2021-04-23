"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class CorpExtAddRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.contact = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.ext.add'
