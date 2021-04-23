"""
Created by auto_sdk on 2020.03.24
"""
from api.base import RestApi


class OapiRhinoMosExecClothesUnperformedGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.req = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.mos.exec.clothes.unperformed.get'
