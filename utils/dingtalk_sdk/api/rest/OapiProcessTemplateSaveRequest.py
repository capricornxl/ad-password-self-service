"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiProcessTemplateSaveRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.font = None
        self.process_code = None
        self.vm = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.process.template.save'
