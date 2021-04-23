"""
Created by auto_sdk on 2020.07.14
"""
from api.base import RestApi


class OapiRhinoMosExecClothesBatchUnscrapRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.batch_clothes_perform_req = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.mos.exec.clothes.batch.unscrap'
