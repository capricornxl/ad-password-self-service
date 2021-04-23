"""
Created by auto_sdk on 2020.07.03
"""
from api.base import RestApi


class OapiRhinoMosExecClothesConditionGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.get_clothes_condition_req = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.mos.exec.clothes.condition.get'
