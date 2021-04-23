"""
Created by auto_sdk on 2020.04.08
"""
from api.base import RestApi


class OapiProcessPrinterInstanceGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.request = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.process.printer.instance.get'
