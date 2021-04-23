"""
Created by auto_sdk on 2020.02.07
"""
from api.base import RestApi


class OapiOcrStructuredRecognizeRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.image_url = None
        self.type = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ocr.structured.recognize'
