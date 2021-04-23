"""
Created by auto_sdk on 2020.03.04
"""
from api.base import RestApi


class OapiRhinoCooperationCarrierGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.carrier_id = None
        self.tenant_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.cooperation.carrier.get'
