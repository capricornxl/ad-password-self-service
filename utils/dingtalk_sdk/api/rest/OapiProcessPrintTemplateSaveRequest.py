"""
Created by auto_sdk on 2020.12.31
"""
from api.base import RestApi


class OapiProcessPrintTemplateSaveRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.font = None
        self.open_customize_print = None
        self.process_code = None
        self.vm = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.process.print.template.save'
